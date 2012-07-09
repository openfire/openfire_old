# -*- coding: utf-8 -*-
## Project Services Init
import logging
from apptools import BaseService

from openfire.core.sessions import SessionsMixin


class RemoteService(BaseService, SessionsMixin):

    ''' Abstract parent for all openfire services. '''

    def initialize(self):

        ''' Initialize hook. '''

        ## extract the session & csrf headers
        session, csrf = self.request.headers.get('x-appfactory-session'), self.request.headers.get('x-appfactory-csrf')
        if session and csrf:
            sid = self.get_session(make=False)
            if sid is None:
                logging.warning('Could not resolve user session.')
            else:
                self.session = sid
                self.sid = self.session.get('sid')
                logging.info('Found user session! %s' % sid)

    def after_request_hook(self):

        ''' Response callback hook. '''

        if hasattr(self, 'session'):
            if self.session:
                self.save_session()
