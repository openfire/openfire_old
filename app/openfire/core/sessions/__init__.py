# -*- coding: utf-8 -*-

# Base Imports
import config as gc

# Webapp2 Imports
import webapp2

from webapp2_extras import sessions
from webapp2_extras import securecookie

# OpenFire Imports
from openfire.models import user
from openfire.core import CoreAPI
from openfire.core.sessions import manager

# AppTools Imports
from apptools.util.debug import AppToolsLogger


class CoreSessionAPI(CoreAPI):

    ''' Manages sessions, backed by NDB and memcache. '''

    # Loader/Factory Management
    store = None
    header = 'X-AppFactory-Session'
    manager = manager.OpenfireSessionManager()
    serializer = securecookie.SecureCookieSerializer(gc.config.get('openfire.sessions').get('salt', '__SALT__'))

    #### ++++ Builtins ++++ ####
    def __init__(self, store):

        ''' Construct Core Sessions API '''

        self.store = store
        return

    #### ++++ Shortcuts ++++ ####
    @webapp2.cached_property
    def config(self):

        ''' Cached shortcut to session config '''

        return gc.config.get('openfire.sessions')

    @webapp2.cached_property
    def logging(self):

        ''' Cached shortcut to named logging pipe '''

        global AppToolsLogger
        return AppToolsLogger(path='openfire.core.sessions', name='CoreSessions')._setcondition(self.config.get('logging', False))

    #### ++++ Internal Methods ++++ ####
    def _generate_sid(self):

        ''' Generate a unique session ID/token pair. '''

        self.logging.info('Generating new session ID/token pair.')
        return self.manager._get_new_sid()

    def _load_session(self, sid):

        ''' Try to load a detected session. '''

        self.logging.info('Loading session from SID "%s".' % sid)
        return self.manager._get_by_sid(sid)

    def _sniff_session(self, request):

        ''' Try to detect an existing session. '''

        if self.config.get('cookieless', False):
            self.logging.info('Sniffing session. Cookieless enabled.')
            if self.header in request.headers:
                return request.headers.get(self.header)

        if self.config.get('frontends', {}).get('cookies').get('enabled', False):

            ttl = self.config.get('frontends', {}).get('cookies', {}).get('ttl', 600)
            name = self.config.get('frontends', {}).get('cookies', {}).get('name', 'ofsession')

            self.logging.info('Cookieless not found. Looking for securecookie at name "%s".' % name)
            cookie = request.cookies.get(name)
            if cookie:
                self.logging.info('SecureCookie found: "%s". Reading with max-age "%s" of type "%s".' % (cookie, ttl, type(ttl)))
                cookie = self.serializer.deserialize(name, cookie, max_age=int(ttl))

                self.logging.info('SecureCookie decoded: "%s".' % cookie)

                if cookie is None:
                    self.logging.info('EWW! Stale cookie. New session needed.')
                    return None
                else:
                    return cookie.get('sid', None)

            self.logging.info('Cookie result: "%s".' % cookie)
            if cookie is not None and 'sid' in cookie:
                return cookie.get('sid', None)

        return None

    #### ++++ External Methods ++++ ####
    def get_session(self, request, max_age=600):

        ''' Create or load an existing user session. '''

        self.logging.info('Sniffing for existing session...')
        self.sid = self._sniff_session(request)
        session = None
        if self.sid is not None:
            self.logging.info('Possibly valid session found at SID "%s".' % self.sid)
            session = self._load_session(self.sid)
        if session is None:
            self.logging.info('Existing session not found or not valid. Starting a new one.')
            session = self.manager.make_session()
            self.sid = session.get('sid')

        return session

    def save_session(self, sid, session, handler):

        ''' Save a user session. '''

        self.logging.info('Storing session.')
        if self.config.get('frontends', {}).get('cookies', {}).get('enabled', False):

            name = self.config['frontends']['cookies']['name']
            self.logging.info('Cookies enabled. Setting secure cookie at name "%s".' % name)
            serialized_cookie = self.serializer.serialize(name, session)
            handler.response.set_cookie(name, serialized_cookie)

        if self.config.get('frontends', {}).get('localstorage', {}).get('enabled', False):

            self.logging.info('LocalStorage enabled. Setting flag header.')
            handler.response.headers['X-AppFactory-LocalStorage'] = 'enabled'

        return self.manager._save_at_sid(sid, session, handler)


class SessionsMixin(object):

    ''' Bridges the Core Sessions API and WebHandler. '''

    __sessions_bridge = None

    def get_session(self, **kwargs):

        ''' Proxy stuff to the Core Sessions API. '''

        if self.__sessions_bridge is None:
            if not hasattr(self, 'session_store'):
                self.session_store = sessions.get_store(request=self.request)
            self.__sessions_bridge = CoreSessionAPI(self.session_store)

        session = self.__sessions_bridge.get_session(self.request, **kwargs)
        self.__session_id = session['sid']

        return session

    def save_session(self):

        ''' Proxy stuff to the Core Sessions API. '''

        self.logging.info('Saving session: "%s"' % self.session)
        return self.__sessions_bridge.save_session(self.__session_id, self.session, self)
