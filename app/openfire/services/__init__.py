# -*- coding: utf-8 -*-

# apptools imports
from apptools import BaseService
from apptools.util import debug

# sdk imports
from google.appengine.ext import ndb

# user/permissions
from openfire.models.user import User
from openfire.models.user import Permissions

## core bridge imports
from openfire.core.content import ContentBridge
from openfire.core.sessions import SessionsBridge
from openfire.handlers import NamespaceBridge


class RemoteService(BaseService, SessionsBridge, ContentBridge, NamespaceBridge):

    ''' Abstract parent for all openfire services. '''

    def initialize(self):

        ''' Initialize hook. '''

        # Set up the datastore namespace
        self.prepare_namespace(self.handler.request)

        ## extract the session & csrf headers
        self.session = self.get_session(make=False)

        if self.session is None:
            #logging.warning('Could not resolve user session.')
            pass
        else:
            self.sid = self.session.get('sid')
            #logging.info('Found user session! %s' % self.sid)

            if self.session.get('ukey', None) is not None:
                self.user, self.permissions = tuple(ndb.get_multi([ndb.Key(urlsafe=self.session['ukey']), ndb.Key(Permissions, 'global', parent=ndb.Key(User, self.session['uid']))]))
            else:
                #logging.info('Found user session but failed to load user. Continuing.')
                pass

    def after_request_hook(self):

        ''' Response callback hook. '''
        if hasattr(self, 'session'):
            if self.session:
                self.save_session()
