# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel

# Model Attachments
from openfire.messages import alerts as messages
from openfire.pipelines.model import alerts as pipelines


class Alert(AppModel):

    ''' Represents an alert (or a set of alerts) sent to a user. '''

    _message_class = messages.Alert
    _pipeline_class = pipelines.AlertPipeline

    user = ndb.KeyProperty('u', indexed=True, required=True)
    has_read = ndb.BooleanProperty('r', default=False, indexed=True)
    subscription = ndb.KeyProperty('s', indexed=True, required=True)
    mode = ndb.StringProperty('m', indexed=True, repeated=True, required=True, choices=['c', 'p', 'e', 'x'])  # channel, push, email, xmpp
