# -*- coding: utf-8 -*-

'''

Project Handlers

This module is where you put your project's RequestHandlers. WebHandler and MobileHandler
are designed to be extended by your app's handlers. This gives you a chance to inject custom
logic / request handling stuff across your entire app, by putting it here.

-sam (<sam@momentum.io>)

'''

## General Imports
import random
import config
import logging
import hashlib

## Webapp2 Imports
import webapp2

from webapp2_extras import sessions

from webapp2_extras.appengine import sessions_ndb
from webapp2_extras.appengine import sessions_memcache

## AppTools Imports
from apptools.core import BaseHandler

## Openfire Imports
from openfire.models import user
from openfire.core.sessions import SessionsMixin


class WebHandler(BaseHandler, SessionsMixin):

    ''' Handler for desktop web requests. '''

    session = None

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
                return self.redirect(redirect_url)

            # Dispatch method
            response = super(WebHandler, self).dispatch()

        finally:
            self.save_session()

        return response

    def build_session(self):

        ''' Build an initial session object and create an SID '''

        ## build a session no matter what, yo
        self.session = self.get_session()

        if self.session.get('ukey', None) is None:
            u = self.api.users.get_current_user()
            if u is not None:

                ## we have an authenticated user
                self.session['authenticated'] = True

                ## sometimes this returns none (when federated identity auth is enabled), but then the email is a persistent token
                if u.user_id() is not None:
                    self.session['uid'] = u.user_id()
                else:
                    self.session['uid'] = u.email()

                ## try to load the user's session, since they are logged in
                u = user.User.get_by_id(self.session['uid'])
                if u is None:
                    self.session['redirect'] = self.url_for('auth/register')
                    self.session['returnto'] = self.request.url
                    self.session['register'] = True
                else:
                    self.session['ukey'] = u.key.urlsafe()
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
            raise exception

        return self.error(500)

    def _bindRuntimeTemplateContext(self, context):

        ''' Bind in the session '''

        if 'user' not in context:
            context['user'] = {}
        context['user']['session'] = self.session
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
