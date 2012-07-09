# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel

# Model Attachments
from openfire.messages import alerts as messages
from openfire.pipelines.model import alerts as pipelines


class Subscription(AppModel):

    ''' A subscription registered with the Prospective Search API. '''

    _message_class = messages.Subscription
    _pipeline_class = pipelines.SubscriptionPipeline

    query = ndb.StringProperty('q', indexed=True)
    trigger_email = ndb.BooleanProperty('e', indexed=True, default=False)
    trigger_sms = ndb.BooleanProperty('s', indexed=True, default=False)
    trigger_xmpp = ndb.BooleanProperty('x', indexed=True, default=False)
