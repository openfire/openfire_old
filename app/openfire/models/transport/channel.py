# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel


## PushChannel - keeps track of channels opened/closed by openfire
class PushChannel(AppModel):

    ''' Represents an open or closed push channel managed by openfire. '''

    session = ndb.KeyProperty('s', required=True, indexed=True)
    channel = ndb.StringProperty('c', required=True, indexed=True)
    client_id = ndb.StringProperty('i', required=True, indexed=True)
    duration = ndb.IntegerProperty('t', default=120, indexed=False)
    messages = ndb.KeyProperty('m', repeated=True, indexed=False)
    live = ndb.BooleanProperty('live', default=False, indexed=True)
    connected = ndb.DateTimeProperty('e', default=None, indexed=True)
    disconnected = ndb.DateTimeProperty('d', default=None, indexed=True)


## PushSession - keeps track of a push-enabled user session, possibly spanning multiple channels
class PushSession(AppModel):

    ''' Represents an established push session managed by openfire, possbly spanning multiple channels. '''

    sid = ndb.StringProperty('s', required=True, indexed=True)
    channels = ndb.KeyProperty('c', repeated=True, indexed=True)


##  PushMessage - created when a message is pushed to a client through a push channel
class PushMessage(AppModel):

    ''' Represents a message sent to a client through a push channel. '''

    content = ndb.TextProperty('c', required=True, indexed=False)
