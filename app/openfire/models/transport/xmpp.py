# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models.transport import TransportModel


## XMPPChannel - keeps track of a JID that openfire has communicated with before
class XMPPChannel(TransportModel):

    ''' Represents a JID that openfire has communicated with. '''

    jid = ndb.StringProperty('j', indexed=True, required=True)
    invited = ndb.BooleanProperty('i', indexed=True, default=False)
    accepted = ndb.BooleanProperty('a', indexed=True, default=False)
    denied = ndb.BooleanProperty('d', indexed=True, default=False)
    presence = ndb.StringProperty('p', indexed=True, choices=['available', 'unavailable'], default='unavailable')


## XMPPSubscription - a user-requested XMPP subscription to an openfire JID
class XMPPSubscription(TransportModel):

    ''' Represents a user-requested XMPP subscription to an openfire JID. '''

    jid = ndb.StringProperty('j', indexed=True, required=True)
    from_jid = ndb.StringProperty('f', indexed=True, required=True)
    direction = ndb.StringProperty('d', indexed=True, choices=['egress', 'ingress'], required=True)


## XMPPError - an AppEngine-reported XMPP delivery/runtime error
class XMPPError(TransportModel):

    ''' Represents an error encountered when trying to deliver/handle an XMPP operation. '''

    sender = ndb.StringProperty('j', indexed=True, required=True)
    stanza = ndb.TextProperty('s', indexed=False, required=True)


## XMPPMessage - keeps track of an XMPP message received or sent from/to an openfire JID
class XMPPMessage(TransportModel):

    '''  Keeps track of an incoming or outgoing XMPP message. '''

    direction = ndb.StringProperty('d', indexed=True, choices=['inbound', 'outbound'], required=True)
    jid = ndb.StringProperty('j', indexed=True, required=True)
    channel = ndb.KeyProeprty('c', indexed=True, required=True)
    from_jid = ndb.StringProperty('f', indexed=True, required=True)
    message_type = ndb.StringProperty('t', choices=['chat', 'error', 'group', 'headline', 'normal'], default='normal', indexed=True)
    body = ndb.TextProperty('b', indexed=False, required=True)
    stanza = ndb.TextProperty('s', indexed=False, required=False)
    raw_xml = ndb.BooleanProperty('x', indexed=False, default=False)
