# -*- coding: utf-8 -*-
from openfire.models import AppModel


## XMPPChannel - keeps track of a JID that openfire has communicated with before
class XMPPChannel(AppModel):

	''' Represents a JID that openfire has communicated with. '''

	pass


## XMPPSubscription - a user-requested XMPP subscription to an openfire JID
class XMPPSubscription(AppModel):

	''' Represents a user-requested XMPP subscription to an openfire JID. '''

	pass


## XMPPError - an AppEngine-reported XMPP delivery/runtime error
class XMPPError(AppModel):

	''' Represents an error encountered when trying to deliver/handle an XMPP operation. '''

	pass


## XMPPMessage - keeps track of an XMPP message received or sent from/to an openfire JID
class XMPPMessage(AppModel):

	'''  Keeps track of an incoming or outgoing XMPP message. '''

	pass
