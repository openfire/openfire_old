# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel


class Subscription(AppModel):

    ''' A subscription registered with the Prospective Search API. '''

    query = ndb.StringProperty('q', indexed=True)
    trigger_email = ndb.BooleanProperty('e', indexed=True, default=False)
    trigger_sms = ndb.BooleanProperty('s', indexed=True, default=False)
    trigger_xmpp = ndb.BooleanProperty('x', indexed=True, default=False)
