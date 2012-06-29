# -*- coding: utf-8 -*-

# Base Imports
import re
import base64
import config
import hashlib
import datetime

# Webapp2 Imports
import webapp2
from webapp2_extras import sessions

# AppTools Imports
from apptools.util import debug

# OpenFire Imports
from openfire.core.sessions import loader

_sessions_config = config.config.get('openfire.sessions')


class OpenfireSessionManager(sessions.CustomBackendSessionFactory):

    ''' SessionManager - mediates between the Core Sessions API and installed session loaders '''

    # Loader Management
    loaders = {}
    callchain = []

    # Session Management
    sid = None
    _sid_re = re.compile(r'(.*)')


    #### ++++ Builtins ++++ ####
    def __init__(self,use_threadcache=_sessions_config.get('backends', {}).get('threadcache', {}).get('enabled', False),
                      use_memcache=_sessions_config.get('backends', {}).get('memcache', {}).get('enabled', False),
                      use_datastore=_sessions_config.get('backends', {}).get('datastore', {}).get('enabled', False)):

        ''' Prepare session loaders. '''

        if not hasattr(self, 'default'):
            self.default = None

            installed_loaders = (

                ('threadcache', use_threadcache, loader.ThreadcacheSessionLoader),
                ('memcache', use_memcache, loader.MemcacheSessionLoader),
                ('datastore', use_datastore, loader.PersistentSessionLoader)

            )

            self._prepare_loaders(reversed(installed_loaders))


    #### ++++ Shortcuts ++++ ####
    @webapp2.cached_property
    def config(self):

        ''' Cached shortcut to config '''

        return config.config.get('openfire.sessions')

    @webapp2.cached_property
    def logging(self):

        ''' Cached shortcut to named logging pipe '''

        return debug.AppToolsLogger(path='openfire.core.sessions.manager', name='SessionManager')._setcondition(self.config.get('logging', False))


    #### ++++ Internal Methods ++++ ####
    def _is_valid_sid(self, sid):

        ''' Validate a potential SID. '''

        return (sid is not None) and sid and self._sid_re.match(sid) is not None

    def _simple_encode(self, cltx):

        ''' Quickly encode a string into a safe one for storage. '''

        return hashlib.md5(base64.b64encode(str(cltx))).hexdigest()

    def _get_by_sid(self, sid):

        ''' Retrieve a session by SID. '''

        valid_session = None
        self.logging.info('Retrieving by SID from loaders.')
        if self._is_valid_sid(sid):
            self.logging.info('SID is valid.')
            callchain = [self.default] + [i for i in self.callchain if i != self.default]
            self.logging.info('Prepared loader callchain: "%s".' % callchain)
            for loader in callchain:
                self.logging.info('Trying loader "%s"...' % loader)
                try:
                    s = loader.get_session(sid)
                    if not isinstance(s, dict):
                        assert s not in frozenset([None, False])
                    else:
                        break

                except AssertionError, e:
                    self.logging.info('Session not found at SID "%s" with loader "%s".' % (sid, loader))

                except Exception, e:
                    self.logging.warning('Exception encountered trying to load session at SID "%s" via session loader "%s". Error: "%s".' % (sid, loader, e))
                    if config.debug:
                        raise
                    continue
        else:
            self.logging.warning('Session ID invalid.')

        if s:
            self.logging.info('Found valid session at SID "%s" using loader "%s".' % (sid, loader))
            self.logging.info('Session contents: "%s".' % s)
            valid_session = s


        return valid_session

    def _get_new_sid(self):

        ''' Generate a random SID. '''

        today = datetime.date.today()
        return ''.join([
                        self._simple_encode(':'.join(
                            [self.config.get('salt', '__SALT__'),
                            ''.join(map(str, [today.day, today.month]))]))[0:5],
                        self._simple_encode(
                            super(OpenfireSessionManager, self)._get_new_sid()
                            )
                        ])

    def _save_at_sid(self, sid, struct, handler):

        ''' Save the session in each of the caches. '''

        saved = False
        if self._is_valid_sid(sid):
            self.logging.info('SID is valid.')
            callchain = [self.default] + [i for i in self.callchain if i != self.default]
            for loader in callchain:
                self.logging.info('Putting session using loader "%s".' % loader)
                try:
                    loader.put_session(sid, struct, handler)

                except:
                    if config.debug:
                        raise
                    else:
                        self.logging.warning('Could not put session using enabled loader "%s".' % loader)
                        continue

                else:
                    saved = True
                    continue
        else:
            self.logging.warning('SID "%s" invalid. No session found.' % sid)

        return saved

    def _prepare_loaders(self, loaders):

        ''' Find and prepare each session loader. '''

        for name, enabled, loader in loaders:
            self.logging.info('Considering loader "%s" at name "%s".' % (loader, name))
            if enabled:
                self.logging.info('Loader enabled.')
                try:
                    loader = self.default = self.loaders[name] = loader()
                    assert self.default is not None
                    self.callchain.append(loader)

                except AssertionError, a:
                    self.logging.warning('Loader "%s" imported successfully, but could not be constructed.' % a)
                    pass

                except ImportError, i:
                    self.logging.error('Loader "%s" is specified in config, but could not be imported.' % i)
                    if config.debug:
                        raise
                    else:
                        pass

                except Exception, e:
                    self.logging.error('Loader construction for "%s" session loader generated unhandled exception.' % e)
                    self.logging.error(str(e))

                    if config.debug:
                        raise
                    else:
                        pass
            else:
                self.logging.info('Loader disabled.')

        # Check loaders
        if self.default is not None:
            return  # job done

        elif len(self.loaders) > 0:
            self.default = self.loaders[0]
            return

        else:
            self.logging.error('Failed to import and construct any valid session loaders.')
            return


    #### ++++ External Methods ++++ ####
    def make_session(self):

        ''' Return a struct suitable for use as a session starting point '''

        return {'sid': self._get_new_sid(), 'timestamp': str(datetime.datetime.now())}


