# -*- coding: utf-8 -*-
from openfire.models import user
from openfire.models import assets
from openfire.models import project
from google.appengine.ext import ndb
from openfire.handlers import WebHandler
from openfire.handlers.project import ProjectHome
from openfire.handlers.user import UserProfile


class Landing(WebHandler):

    ''' openfire landing page. '''

    def get(self):

        ''' Render landing.html or landing_noauth.html. '''

        ## fetch projects
        master_key_list = []
        pq = project.Project.query().order(project.Project.name)
        pc = pq.count()

        context = {
        }

        if pc > 0:
            projects = pq.fetch(pq.count(), keys_only=True)

            for pk in projects:

                # append project key and generate subkeys
                master_key_list.append(pk)

            ## prepare media
            avatars = []
            projects = {}
            data = ndb.get_multi(master_key_list, use_cache=True, use_memcache=True, use_datastore=True)
            for key, entity in zip(master_key_list, data):
                projects[key.id()] = entity.to_dict()
                projects[key.id()]['slug'] = entity.get_custom_url()
                avatars.append(entity.avatar.id())

            project_assets = ndb.get_multi(avatars)

            for e_project, asset in zip(project.items(), project_assets):
                key, e_project = e_project
                if asset.url:
                    project['avatar'] = asset.url
                elif asset.blob:
                    extension = asset.mime.split('/')[1]
                    project['avatar'] = self.url_for('serve-blob-filename', action='serve', asset_key=asset.key.urlsafe(), filename='project-avatar-' + entity.get_custom_url() + extension)

            projects = [v for k, v in projects.items()]
            context['projects'] = projects

        if False:
            self.render('main/landing_noauth.html', **context)
        else:
            self.render('main/landing.html', **context)
        return


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
        if not url_object:
            return self.error(404) # Failed to find custom url

        kind = url_object.target.kind()
        context = {}
        handler = None
        if kind not in ('Project', 'User'):
            return self.error(404) # Invalid kind

        elif kind == 'Project':
            handler = self._project_handler_class()
            context['key'] = url_object.target.urlsafe()

        elif kind == 'User':
            handler = self._user_handler_class()
            context['username'] = url_object.target.id()

        if not handler:
            return self.error(500) # Failed to instantiate handler?

        # Initialize the new handler with the current request and response.
        handler.initialize(self.request, self.response)

        # Copy over session, user, permissions
        handler.session = self.session
        handler.user = self.user
        handler.permissions = self.permissions

        return handler.get(**context)
