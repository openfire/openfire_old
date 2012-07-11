# -*- coding: utf-8 -*-

# Base Imports
import config as gc

# Webapp2 Imports
import base64
import hashlib
import webapp2

from webapp2_extras import sessions
from webapp2_extras import securecookie

# OpenFire Imports
from openfire.models import user
from openfire.core import CoreAPI
from openfire.core.sessions import manager

# AppTools Imports
from apptools.util.debug import AppToolsLogger

try:
    from Crypto.Cipher import AES
    _crypto = AES
except ImportError:
    _crypto = None

_SIMPLE_ENCRYPTION_FLAG = 'b'
_ADVANCED_ENCRYPTION_FLAG = 's'
_ENCRYPTION_PAD_CHARACTER = ':'


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

    def _sniff_session(self, request, headers=True, cookies=True):

        ''' Try to detect an existing session. '''

        # resolve the session cookie TTL and name
        ttl = self.config.get('frontends', {}).get('cookies', {}).get('ttl', 600)
        name = self.config.get('frontends', {}).get('cookies', {}).get('name', 'ofsession')

        # check headers first
        if self.config.get('cookieless', False) and headers:
            self.logging.info('Sniffing session. Cookieless enabled.')

            # check if our session header is there
            if self.header in request.headers:

                self.logging.info('Found session header at configured key "%s".' % self.header)

                # grab value and check for altcookie
                val = request.headers.get(self.header)
                if name in val:

                    name, cookie = tuple(val.replace('"', '').split('='))
                    self.logging.info('Session is an altcookie. Deserializing.')

                    # found altcookie, deserialize
                    altcookie = self.serializer.deserialize(name, cookie.replace('\\075', '='), max_age=int(ttl))
                    if altcookie is None:  # stale cookie
                        self.logging.warning('Altcookie is stale. Ignoring.')
                        return
                    else:
                        # return SID
                        return altcookie.get('sid', None)

                else:
                    self.logging.info('Session is a direct SID. Returning.')

                    # assume it's an SID directly
                    return request.headers.get(self.header)

        if self.config.get('frontends', {}).get('cookies').get('enabled', False) and cookies:

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
    def get_session(self, request, max_age=600, headers=True, cookies=True, create=True):

        ''' Create or load an existing user session. '''

        self.logging.info('Sniffing for existing session...')
        self.sid = self._sniff_session(request, headers=headers, cookies=cookies)
        session = None
        if self.sid is not None:
            self.logging.info('Possibly valid session found at SID "%s".' % self.sid)
            session = self._load_session(self.sid)
        if session is None:
            if create:
                self.logging.info('Existing session not found or not valid. Starting a new one.')
                session = self.manager.make_session()
                self.sid = session.get('sid')
            else:
                self.logging.info('Existing session not found.')

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

    @webapp2.cached_property
    def cipher(self):

        ''' Load AES and return a new cipher object '''

        from Crypto.Cipher import AES
        return AES.new(hashlib.md5(gc.config.get('openfire.sessions').get('salt', '__SALT__')).hexdigest())

    def get_session(self, make=True, cookies=True, headers=True, **kwargs):

        ''' Proxy stuff to the Core Sessions API. '''

        if self.__sessions_bridge is None:
            if not hasattr(self, 'session_store'):
                self.session_store = sessions.get_store(request=self.request)
            self.__sessions_bridge = CoreSessionAPI(self.session_store)

        session = self.__sessions_bridge.get_session(self.request, create=make, cookies=cookies, headers=headers, **kwargs)
        if session is not None:
            self.__session_id = session['sid']

        return session

    def save_session(self):

        ''' Proxy stuff to the Core Sessions API. '''

        self.logging.info('Saving session: "%s"' % self.session)
        return self.__sessions_bridge.save_session(self.__session_id, self.session, self)

    def encrypt(self, subj, simple=True, cipher=True):

        ''' Encrypt some string '''

        if cipher:
            try:
                if (len(subj) % 16) > 0:
                    subj = subj + ''.join([_ENCRYPTION_PAD_CHARACTER for i in range(1, (len(subj) % 16) - 1)])
                preb64 = _ENCRYPTION_PAD_CHARACTER.join([_ADVANCED_ENCRYPTION_FLAG, self.cipher.encrypt(subj)])
            except ImportError, e:
                if cipher and not simple:
                    raise ValueError("Strong encryption requested, but AES could not be loaded. Exception encountered: '%s'." % e)
                preb64 = _ENCRYPTION_PAD_CHARACTER.join([_SIMPLE_ENCRYPTION_FLAG, subj])
        elif simple:
            preb64 = _ENCRYPTION_PAD_CHARACTER.join([_SIMPLE_ENCRYPTION_FLAG, subj])
        else:
            preb64 = subj  # do nothing for some reason

        return base64.b64encode(preb64)

    def decrypt(self, subj):

        ''' Decrypt some string '''

        subj = base64.b64decode(subj).split(_ENCRYPTION_PAD_CHARACTER)
        if subj[0] == _ADVANCED_ENCRYPTION_FLAG:
            if _crypto is not None:
                return self.cipher.decrypt(subj[1])
            else:
                raise ValueError('Failed to decrypt AES-encrypted sequence as AES support is not installed.')
        elif subj[0] == _SIMPLE_ENCRYPTION_FLAG:
            return reduce(lambda x, y: x + y, subj[1:])
        else:
            return ''.join(subj)  # perhaps it's not encrypted?
