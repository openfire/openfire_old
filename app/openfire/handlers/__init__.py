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
import hashlib

## Webapp2 Imports
import webapp2

## AppTools Imports
from apptools.core import BaseHandler

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

        # Construct session store
        self.session = self.get_session()

        try:
            response = super(WebHandler, self).dispatch()

        finally:
            self.save_session()

        return response

    def build_session(self):

        ''' Build an initial session object and create an SID '''

        self.logging.info('Building session...')

        session_id = int(round(random.random() * 1000000000, 0))
        sid_struct = (self.request.environ.get('REMOTE_ADDR'), self.request.headers.get('User-Agent', ''), session_id)

        session_string = '::'.join([unicode(i) for i in sid_struct])

        self.logging.info('Session string: "%s"' % session_string)
        sid = hashlib.sha256(session_string).hexdigest()

        self.logging.info('Session ID: "%s"' % session_id)
        self.logging.info('Encoded SID: "%s"' % sid)

        self.session['sid'] = sid
        self.session['id'] = session_id
        return

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
