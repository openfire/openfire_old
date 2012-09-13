# -*- coding: utf-8 -*-
import base64
import webapp2
import hashlib
import config as cfg
from config import config
from apptools.util import debug
from openfire.models import user
from openfire.models import assets
from openfire.models import project as p
from openfire.models import activity as a
from google.appengine.ext import ndb
from openfire.handlers import WebHandler
from openfire.handlers.project import ProjectHome
from openfire.handlers.user import UserProfile
from webapp2_extras.security import generate_random_string


class Placeholder(WebHandler):

    ''' openfire placeholder! '''

    template = 'main/placeholder.html'
    should_cache = True
    transport = {
        'secure': True,
        'endpoint': 'beta.openfi.re',
        'consumer': 'ofplaceholder'
    }

    @webapp2.cached_property
    def config(self):

        ''' Named config pipe. '''

        return config.get('openfire.placeholder')

    @webapp2.cached_property
    def logging(self):

        ''' Named logging pipe. '''

        return debug.AppToolsLogger(path='openfire.handlers.main', name='Placeholder')._setcondition(self.config.get('debug', True))

    def _make_services_object(self, services):

        ''' Return only the beta signup method/service. '''

        return [['beta', ['signup'], {'caching': False}]]

    def get(self, **kwargs):

        ''' Return a rendered submission form. '''

        self.force_hostname = "beta.openfi.re"
        self.force_https_assets = True

        args = {
            'state': self.request.GET.get('st'),
            'reason': self.request.GET.get('r'),
            'exception': self.request.GET.get('xc')
        }

        args.update(kwargs)

        if self.should_cache:
            cache_key = '::'.join(['of', 'pagecache', 'placeholder'] + [','.join([':'.join([str(k), str(v)]) for k, v in args.items() if v != None])])
            self.logging.info('Pagecache enabled. Looking for placeholder content in cache key "%s".' % cache_key)

            cached = self.api.memcache.get(cache_key)
            if cached is None:
                self.logging.info('No cached copy found. Rendering.')
                rendered = self.render('main/placeholder.html', flags=args, csrf=base64.b64encode(hashlib.sha512(generate_random_string(32)).hexdigest()))
                self.api.memcache.set(cache_key, rendered)
                return rendered
            self.logging.info('Cached copy found. Returning cached page.')
        return cached

    def post(self):

        ''' Handle a signup, when the JS mechanism for registering either fails or is not supported by the client. '''

        #import pdb; pdb.set_trace()

        ## check for the appropriate action
        if self.request.POST.get('action', False) == 'of.beta.placeholder.registerSignup':
            self.logging.info('Received POSTed beta signup form.')

            ## check for our fakie CSRF token
            if self.request.POST.get('csrf', None) not in ['', None]:

                self.logging.info('Batch CSRF present: "%s".' % self.request.POST.get('csrf'))

                ## import service + request message
                from openfire.messages.beta import BetaSignup
                from openfire.services.beta import BetaService

                ## invoke remote method, taking care to handle exceptions
                try:
                    self.logging.info('Submitting signup with name "%s" and email "%s".' % (self.request.POST.get('name'), self.request.POST.get('email')))
                    r = BetaService().signup(BetaSignup(**{
                        'name': self.request.POST.get('name'),
                        'email': self.request.POST.get('email')
                    }))

                    self.logging.info('Signup result: "%s".' % str(r))

                except BetaService.BetaServiceException, e:

                    ## render with specific error message
                    # return self.redirect_to('landing', st='error', xc=e.__class__, ms=str(e))

                    self.logging.error('Encountered known BetaServiceException.')
                    self.logging.error('Exception class: "%s".' % str(e.__class__))
                    self.logging.error('Exception str: "%s".' % str(e))
                    self.logging.info('Rendering known error.')
                    return self.get(state='error', reason=str(e), exception=e.__class__)

                except Exception, e:

                    ## redirect to generic error message
                    # return self.redirect_to('landing', st='error', r='generic')

                    self.logging.error('Encountered unknown exception.')
                    self.logging.error('Exception class: "%s".' % str(e.__class__))
                    self.logging.error('Exception str: "%s".' % str(e))
                    self.logging.info('Rendering generic error.')
                    return self.get(state='error', r='generic')

                else:

                    ## redirect to success
                    # return self.redirect_to('landing', st='success')
                    self.logging.info('Signup success! Rendering generic success.')
                    return self.get(state='success')

        ## render to generic error
        # return self.redirect_to('landing', st='error', r='generic')
        self.logging.error('Unknown POST form action encountered: "%s". Rendering generic error. ' % self.request.POST.get('action'))
        return self.get(state='error', reason='generic')


class Landing(WebHandler):

    ''' openfire landing page. '''

    template = 'main/landing.html'
    projects_per_page = 6
    activity_per_page = 10

    def get(self):

        ''' Render landing.html or landing_noauth.html. '''

        ## consider placeholder
        if config.get('openfire.placeholder').get('enabled') == True:

            ## consider placeholder `force` flag
            if (self.user is None and self.permissions is None) or (self.user is not None and config.get('openfire.placeholder').get('force') == True):
                return Placeholder(self.request, self.response).get()

        ## fully cached page context
        context = self.api.memcache.get('landing_page_context')
        if not context:

            ## fetch projects
            pq = p.Project.query().order(p.Project.name)
            aq = a.Activity.query().order(a.Activity.modified)

            ## resolve project limit
            if not self.projects_per_page:
                pc = pq.count()
            else:
                pc = self.projects_per_page

            ## resolve activity limit
            if not self.activity_per_page:
                ac = aq.count()
            else:
                ac = self.activity_per_page

            ## start the new context
            context = {}

            ## pull projects if there's more than one to pull
            if pc > 0:
                k_projects = pq.fetch(pc, keys_only=True)

                ## prepare media (fetch avatars, videos + assets for both)
                _assets, avatars, videos, projects = [], [], [], {}
                data = ndb.get_multi(k_projects, use_cache=True, use_memcache=True, use_datastore=True)
                for key, entity in ((entity.key, entity) for entity in data if entity is not None):

                    # create the project context entry
                    projects[key.id()] = entity.to_dict()
                    projects[key.id()]['model'] = entity
                    projects[key.id()]['slug'] = entity.get_custom_url()

                    # build a list of keys to pull, for avatars, videos, and assets
                    avatars.append(entity.avatar)
                    videos.append(entity.video)
                    if entity.avatar:
                        _assets.append(ndb.Key(urlsafe=entity.avatar.id()))

                ## batch pull media
                asset_keys = [k for k in (avatars + _assets + videos) if isinstance(k, (ndb.Key, ndb.Model))]
                project_assets = ndb.get_multi(asset_keys, use_cache=True, use_memcache=True, use_datastore=True)

                ## parse out query results
                _assets = {}
                for _key, _asset in zip(asset_keys, project_assets):
                    if _asset is None:
                        continue
                    else:
                        if isinstance(_asset, assets.Asset):
                            _assets[_key.urlsafe()] = _asset
                        elif isinstance(_asset, assets.Avatar):
                            projects[_asset.key.parent().id()]['avatar'] = _asset.to_dict()
                            projects[_asset.key.parent().id()]['avatar']['model'] = _asset
                        elif isinstance(_asset, assets.Video):
                            projects[_asset.key.parent().id()]['video'] = _asset

                ## build project structs
                for key_id, project in projects.items():

                    # copy over avatar assets
                    if project.get('avatar'):
                        if project.get('avatar').get('model'):
                            asset_id = project.get('avatar').get('model').key.id()
                        elif isinstance(project.get('avatar'), ndb.Key):
                            asset_id = project.get('avatar').id()

                        # find the asset first
                        project['avatar']['asset'] = _assets[asset_id]

                        # if the avatar record has a URL on it, use that
                        if project['avatar'].get('url'):
                            project['avatar']['location'] = project['avatar'].get('url')

                        # fallback to an asset URL next
                        elif project['avatar']['asset'] and project['avatar']['asset'].url:
                            project['avatar']['location'] = project['avatar']['asset'].url

                        # finally, if it's just a blob link with no URL, calculate the serving URL
                        elif project['avatar']['asset'].get('blob'):
                            extension = project['avatar']['asset'].get('mime').split('/')[1]
                            project['avatar']['location'] = self.url_for('serve-blob-filename', action='serve',
                                    asset_key=project['avatar']['asset']['key'].urlsafe(),
                                    filename='project-avatar-' + project['model'].get_custom_url() + '.' + extension)

                ## copy projects over to page context
                context['projects'] = projects.values()

            ## pull activity if there's more than one item to pull
            if ac > 0:
                pass

            ## cache in memcache if we have items at all
            if pc > 0 or ac > 0:
                ## set cached page context
                self.api.memcache.set('landing_page_context', context)

        return self.render('main/landing.html', **context)

    def post(self):

        ''' Redirect to the landing placeholder, if enabled. '''

        if 'placeholder' in self.request.POST.get('action', 'nope'):
            return Placeholder(self.request, self.response).post()


class VerifyURL(WebHandler):

    ''' Test URL for blitz.io. '''

    def get(self):
        self.response.write('42')  # that's it folks
        return


class CustomUrlHandler(WebHandler):

    ''' openfire custom url handling. '''

    # For now we only support projects and user profiles.
    _project_handler_class = ProjectHome
    _user_handler_class = UserProfile

    def get(self, customurl):

        ''' Render the class defined by the target object, or a 404 page. '''

        url_key = ndb.Key('CustomURL', customurl)
        url_object = url_key.get()
        url_target = url_object.target.get()
        if not url_object:
            return self.error(404)  # Failed to find custom url
        if not url_target:
            return self.error(404)  # Custom URL exists, but parent doesn't

        kind = url_object.target.kind()
        context = {}
        handler = None
        if kind not in ('Project', 'User'):
            return self.error(404)  # Invalid kind

        elif kind == 'Project':
            handler = self._project_handler_class(self.request, self.response)
            context['key'] = url_object.target.urlsafe()

        elif kind == 'User':
            handler = self._user_handler_class(self.request, self.response)
            context['username'] = url_target.username
            context['key'] = url_object.target.urlsafe()

        if not handler:
            return self.error(500)  # Failed to instantiate handler?

        # Initialize the new handler with the current request and response.
        #handler.initialize(self.request, self.response)  # commented out by sam and moved to handler construction

        # Copy over session, user, permissions
        handler.session = self.session
        handler.user = self.user
        handler.permissions = self.permissions

        return handler.get(**context)
