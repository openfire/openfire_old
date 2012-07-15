# -*- coding: utf-8 -*-

'''

Project Handlers

This module is where you put your project's RequestHandlers. WebHandler and MobileHandler
are designed to be extended by your app's handlers. This gives you a chance to inject custom
logic / request handling stuff across your entire app, by putting it here.

-sam (<sam@momentum.io>)

'''

## General Imports
import config
import hashlib

## Webapp2 Imports
import webapp2

## Google Imports
from google.appengine.ext import ndb

## AppTools Imports
from apptools.core import BaseHandler

## Openfire Imports
from openfire.models.user import User
from openfire.models.user import Permissions
from openfire.core.sessions import SessionsMixin


class WebHandler(BaseHandler, SessionsMixin):

    ''' Handler for desktop web requests. '''

    user = None
    scope = None
    session = None
    permissions = None
    force_session = True
    authenticated = False
    auth_provider = False

    channel_id = None
    channel_token = None
    channel_timeout = 120

    ## ++ Internal Shortcuts ++ ##
    @webapp2.cached_property
    def logging(self):

        ''' Cached access to this handler's logging pipe '''

        return super(WebHandler, self).logging.extend('WebHandler', self.__class__.__name__)._setcondition(self.config.get('logging', False))

    ## ++ Internal Methods ++ ##
    def dispatch(self):

        ''' Retrieve session + dispatch '''

        # Resolve user session
        self.session = self.build_session()

        try:

            # If we detect a triggered redirect, do it and remove the trigger (CRUCIAL.)
            if self.session.get('redirect') is not None:
                redirect_url = self.session.get('redirect')
                del self.session['redirect']
                response = self.redirect(redirect_url)

            else:
                # Find super
                _super = super(WebHandler, self)

                # Dispatch method
                response = _super.dispatch()

        finally:
            self.save_session()

        return response

    def _format_as_currency(self, number, isPercent):

        #truncates the 'number' variable to the 100's place
        base = int(number)
        remain = number - base

        decStep = remain * 100

        decimal = int(decStep)
        decimal = float(decimal)
        decimal = decimal / 100

        money = base + decimal
        money = str(money)

        #conditional that adds an additonal '0' to the number if the decimal
        # only goes to  the 10's place
        zeroChk = remain * 10
        if zeroChk == int(zeroChk):
            money = money + "0"

        #conditional that will put in a dollar sign '$' if requested by making
        # isPercent equal to zero, and insert a '%' if isPercent equals 1
        if isPercent == 0:
            #money = str(money)
            money = "$" + money

        elif isPercent == 1:
            #money = str(money)
            money = money + "%"
        return money

    def build_session2(self):

        ''' Build an initial session object and create an SID, if needed '''

        if hasattr(self, 'session') and self.session is not None and len(self.session) > 0:
            return self.session  # somehow we already have a session, wtf?

        else:
            self.session = self.get_session()

            if self.session.get('authenticated', False):

                ## we've authenticated
                self.authenticated = True

                if self.session.get('ukey'):
                    try:
                        self.user, self.permissions = tuple(ndb.get_multi([
                                ndb.Key(urlsafe=self.session.get('ukey')),
                                ndb.Key(Permissions, 'global', parent=ndb.Key(User, self.session['uid']))],
                                use_cache=True, use_memcache=True, use_datastore=True))

                    except:

                        ## UKEY IS BAD, send them to register again
                        self.user = None

                    # user not found/bad key
                    if self.user is None:

                        # if they have a continue url, use it
                        if self.session.get('continue_url'):
                            registration_url = self.url_for('auth/register', go=self.session.get('continue_url'))

                        # otherwise bring them back here afterwards
                        else:
                            registration_url = self.url_for('auth/register', go=self.request.path_qs)

                        return self.redirect(registration_url)

                    # user found!
                    else:
                        pass

        # for now @(TODO): START BACK HERE ON AUTH
        return self.session

    def build_session(self):

        ''' Build an initial session object and create an SID '''

        if hasattr(self, 'force_session') and self.force_session:
            ## build a session no matter what, yo
            self.session = self.get_session()

            if self.session.get('ukey', None) is None:
                u = self.api.users.get_current_user()
                if u is not None:

                    ## we have an authenticated user
                    self.session['authenticated'] = True
                    self.authenticated = True

                    ## sometimes this returns none (when federated identity auth is enabled), but then the email is a persistent token
                    self.session['uid'] = u.email()

                    user, permissions = tuple(ndb.get_multi([ndb.Key(User, self.session['uid']), ndb.Key(Permissions, 'global', parent=ndb.Key(User, self.session['uid']))]))
                    if user is None:
                        self.session['redirect'] = self.url_for('auth/register')
                        self.session['returnto'] = self.request.url
                        self.session['register'] = True
                    else:
                        self.user = user
                        self.permissions = permissions
                        self.session['ukey'] = user.key.urlsafe()
                        self.session['email'] = u.email()
                        self.session['nickname'] = u.nickname()
                        if self.api.users.is_current_user_admin():
                            self.session['root'] = True
            else:
                self.user = ndb.Key(urlsafe=self.session['ukey'])
                self.permissions = ndb.Key(Permissions, 'global', parent=ndb.Key(User, self.session['uid']))
                self.user, self.permissions = tuple(ndb.get_multi([self.user, self.permissions]))
        return self.session

    def handle_exception2(self, exception, debug):

        ''' Handle an unhandled exception '''

        self.logging.critical('Unhandled exception encountered.')
        self.logging.critical(str(exception))

        if not config.debug:
            self.response.write('Woops! Error.<br />')
        else:
            self.response.write('<b>Unhandled exception encountered:</b><br />')
            self.response.write(str(exception))
            self.response.write('<h2>quick, get the developers</h2>')
            raise exception

        return self.error(500)

    def _bindRuntimeTemplateContext(self, context):

        ''' Bind in the session '''

        if 'user' not in context:
            context['user'] = {}
        context['user']['session'] = self.session

        # install meta config
        context['_meta'] = config.config.get('openfire.meta')
        context['_opengraph'] = context['_meta'].get('opengraph', {})
        context['_location'] = context['_opengraph'].get('location', {})

        # install encryption shim
        context['encrypt'] = lambda x: self.encrypt(x)
        context['decrypt'] = lambda x: self.decrypt(x)

        # install currency + percentage formatters
        context['currency'] = lambda x: self._format_as_currency(x, False)
        context['percentage'] = lambda x: self._format_as_currency(x, True)

        # converts an email address into a gravatar img src url
        context['gravatarify'] = lambda x, y, z: ''.join(['http://www.gravatar.com/avatar/', hashlib.md5(x).hexdigest(), '.%s?s=%s&d=http://placehold.it/%s/ffffff.png' % (y, z, z)])

        # retrieves current user model + permissions
        context['security'] = {
            'permissions': self.permissions,
            'current_user': self.user,
            'session': self.session
        }

        # setup transport config
        context['transport'] = {
            
            ## services config
            'services': {
                'secure': False,
                'endpoint': self.request.environ.get('HTTP_HOST'),
                'consumer': 'ofapp',
                'scope': 'readonly'
            },

            ## push config
            'realtime': {
                'enabled': False,
                'channel': self.channel_token,
                'timeout': self.channel_timeout
            }

        }

        return super(WebHandler, self)._bindRuntimeTemplateContext(context)

    ## ++ HTTP Methods ++ ##
    def head(self):

        ''' Run GET, if defined, and return the headers only. '''

        if hasattr(self, 'get'):
            self.get()
        return

    def options(self):

        ''' Return available methods '''

        return


class MobileHandler(BaseHandler):

    ''' Handler for mobile web requests. '''
