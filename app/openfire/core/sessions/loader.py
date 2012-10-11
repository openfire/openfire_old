# -*- coding: utf-8 -*-

# Base Imports
import base64
import config
import hashlib

# Webapp2 Imports
import webapp2

# AppTools Imports
from apptools.util import debug

# OpenFire Imports
from openfire.models import sessions

# AppEngine Imports
from google.appengine.ext import ndb
from google.appengine.api import memcache


## OpenfireSessionLoader
# Abstract parent to all openfire session loader classes.
class OpenfireSessionLoader(object):

    ''' Abstract parent to openfire session loaders '''

    #### ++++ Shortcuts ++++ ####
    @webapp2.cached_property
    def config(self):

        ''' Cached shortcut to config. '''

        return config.config.get('openfire.sessions')

    @webapp2.cached_property
    def logging(self):

        ''' Cached access to named logging pipe. '''

        return debug.AppToolsLogger(path='openfire.core.sessions.loader', name=self.__class__.__name__)._setcondition(self.config.get('logging', False))

    #### ++++ Internal Methods ++++ ####
    def _str(self, subj):

        ''' String coercion. '''

        if not isinstance(subj, basestring):
            if isinstance(subj, ndb.Key):
                return subj.urlsafe()
            elif isinstance(subj, ndb.Model):
                return subj.key.urlsafe()
        return str(subj)

    def _en(self, cltx):

        ''' Opaque string encode. '''

        return hashlib.sha256(base64.b64encode(self._str(cltx))).hexdigest()

    #### ++++ External Methods ++++ ####
    def get_session(self, id):

        ''' Retrieve a session (must be overridden by child classes) '''

        raise NotImplemented

    def put_session(self, id, struct, handler):

        ''' Save a session (must be overridden by child classes) '''

        raise NotImplemented


## ThreadcacheSessionLoader
# Manages storage and retrieval of session data from instance memory.
class ThreadcacheSessionLoader(OpenfireSessionLoader):

    ''' Session loader that loads and saves sessions with local threadcache '''

    def get_session(self, id):

        ''' Returns a session from threadcache, given a session ID. '''

        raise NotImplemented  # @TODO

    def put_session(self, id, struct, handler):

        ''' Saves a session to threadcache, from a generated response. '''

        raise NotImplemented  # @TODO


## MemcacheSessionLoader
# Manages storage and retrieval of session data from memcache.
class MemcacheSessionLoader(OpenfireSessionLoader):

    ''' Session loader that loads and saves sessions with memcache '''

    def get_session(self, id):

        ''' Returns a session from memcache, given a session ID. '''

        self.logging.info('Looking in memcache for session at ID: "%s".' % id)
        self.logging.info('Looking in memcache for encoded session ID: "%s"' % self._en(id))

        session = memcache.get(self._en(id))

        self.logging.info('Memcache result: "%s"' % session)
        return session

    def put_session(self, id, struct, handler):

        ''' Saves a session to memcache, from a generated response. '''

        self.logging.info('Saving session in memcache at ID: "%s"' % id)
        self.logging.info('Saving session in memcache at encoded ID: "%s"' % self._en(id))

        if struct.get('destroy', False) == True:
            self.logging.info('Memcache loader received destroy signal...')
            memcache.delete(self._en(id))
            return

        timeout = self.config.get('backends', {}).get('memcache', {}).get('ttl', self.config.get('ttl', 1200))

        self.logging.info('Timeout set to: "%s".' % timeout)

        memcache.set(self._en(id), struct.__json__(), int(timeout))

        self.logging.info('Struct saved TTL(%s): "%s"' % (timeout, struct))
        return


## PersistentSessionLoader
# Manages storage and retrieval of session data from the datastore.
class PersistentSessionLoader(OpenfireSessionLoader):

    ''' Session loader that loads and saves sessions with NDB and the AppEngine Datastore '''

    def get_session(self, id):

        ''' Returns a session from the datastore, given a session ID. '''

        try:
            session = ndb.Key(sessions.Session, self._en(id)).get()
            assert session != None

        except AssertionError:
            self.logging.info('Session not found at encoded ID "%s".' % id)
            pass

        except Exception:
            self.logging.error('Error encountered building datastore key for session at encoded ID "%s".' % id)
            if config.debug:
                raise

        else:
            return session.data
        return None

    def put_session(self, id, struct, handler):

        ''' Saves a session to the datastore, from a generated response. '''

        self.logging.info('Saving session in datastore at ID: "%s"' % id)

        if struct.get('destroy', False) == True:
            self.logging.info('Datastore loader received destroy signal...')
            try:
                skey = ndb.Key(sessions.Session, id)
                skey.delete()
            except Exception, e:
                self.logging.error('Encountered unknown exception trying to destroy session at ID "%s". The uncaught exception was: "%s".' % (id, e))
                if gc.debug:
                    raise
                else:
                    return {}
            else:
                self.logging.info('Session destroyed successfully.')
                return {}

        if not self.config.get('backends', {}).get('datastore', {}).get('authenticated', False) or struct.get('authenticated') != None and struct.get('ukey') != None:

            self.logging.debug('Authenticated datastore session storage off or the user is authenticated.')

            skey = ndb.Key(sessions.Session, id)
            session_params = {
                'key': ndb.Key(sessions.Session, id),
                'sid': id,
                'data': struct.__json__(),
                'mode': struct.get('mode'),
                'provider': struct.get('provider'),
                'addr': handler.request.environ.get('REMOTE_ADDR', None) if not handler.force_remoteip else getattr(handler, 'force_remoteip'),
                'user': None if not (hasattr(handler, 'user') and getattr(handler, 'user') != None) else getattr(getattr(handler, 'user'), 'key'),
                'agent': handler.request.headers.get('User-Agent', None) if not handler.uagent.get('original', False) else handler.uagent.get('original')
            }
            session_o = sessions.Session(**session_params)
            session_key = session_o.put(use_cache=True, use_memcache=True, use_datastore=True)

            self.logging.info('Session stored at key: "%s"' % session_key.urlsafe())
            return session_o.data  # @TODO: Fix user bridge

        else:

            self.logging.debug('Authenticated datastore session storage on, and the user is not logged in. Continuing.')
            return {}
