# -*- coding: utf-8 -*-
from openfire.models import AppModel


## OutgoingEmail - created for each email sent from openfire
class OutgoingEmail(AppModel):

	''' Represents a queued (and possibly, sent) outgoing email. '''

	pass


## IncomingEmail - created for each email received by openfire
class IncomingEmail(AppModel):

	''' Represents a queued (and possibly, processed) incoming email. '''

	pass
