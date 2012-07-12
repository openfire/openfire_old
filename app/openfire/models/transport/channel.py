# -*- coding: utf-8 -*-
from openfire.models import AppModel


## PushChannel - keeps track of channels opened/closed by openfire
class PushChannel(AppModel):

	''' Represents an open or closed push channel managed by openfire. '''

	pass


## PushSession - keeps track of a push-enabled user session, possibly spanning multiple channels
class PushSession(AppModel):

	''' Represents an established push session managed by openfire, possbly spanning multiple channels. '''

	pass


##  PushMessage - created when a message is pushed to a client through a push channel
class PushMessage(AppModel):

	''' Represents a message sent to a client through a push channel. '''

	pass
