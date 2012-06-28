# -*- coding: utf-8 -*-
import config

from google.appengine.ext import ndb
from openfire.models import AppModel


######## ======== Session Tracking ======== ########

## UserSession - lightweight session entity that tracks a user session
class Session(AppModel):

    ''' Represents a user session. '''

    _SESSION_TTL = config.config.get('openfire.sessions').get('ttl', 300)

    sid = ndb.StringProperty('s', required=True, indexed=False)
    data = ndb.JsonProperty('d', compressed=True)
    addr = ndb.StringProperty('a', required=True, indexed=True)
    user = ndb.KeyProperty('u', required=False, indexed=True, default=None)
    touched = ndb.DateTimeProperty('t', auto_now=True, indexed=True)


## SessionData - stores an opaque blob of data attached to a user session
class SessionData(AppModel):

    ''' Stores data about a session. (NOT YET IN USE) '''

    session = ndb.KeyProperty('s', required=True, indexed=True)
    csrf = ndb.StringProperty('csrf', repeated=True, indexed=True)
    data = ndb.JsonProperty('d', compressed=True)
    addr = ndb.StringProperty('a', required=True, indexed=True)
    touched = ndb.DateTimeProperty('t', auto_now=True, indexed=True)
    created = ndb.DateTimeProperty('c', auto_now_add=True, indexed=True)
    user = ndb.KeyProperty('u', required=False, indexed=True, default=None)
    authenticated = ndb.BooleanProperty('ath', default=False, indexed=True)
    events = ndb.KeyProperty('e', repeated=True, indexed=True)
    established = ndb.DateTimeProperty('e', auto_now_add=True, indexed=False)
