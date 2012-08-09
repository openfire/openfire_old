# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel

# Model Attachments
from openfire.messages import alerts as messages
from openfire.pipelines.model import alerts as pipelines


## MatcherNamespace - correlates numerous `queries` under a `topic` that represents a scope for prospective queries
class MatcherNamespace(AppModel):

    ''' Represents a registered topic in the GAE Prospective Search API. '''

    _use_cache = True
    _use_memcache = True
    _use_datastore = True

    _message_class = messages.Namespace
    _pipeline_class = pipelines.NamespacePipeline

    kind = ndb.StringProperty('k', repeated=True)
    topic = ndb.StringProperty('t', required=True)


## MatcherQuery - a unique query registered with the prospective search API, whose events can be subscribed to
class MatcherQuery(AppModel):

    ''' A query registered with the Prospective Search API. '''

    _use_cache = True
    _use_memcache = True
    _use_datastore = True

    _message_class = messages.Query
    _pipeline_class = pipelines.QueryPipeline

    query = ndb.StringProperty('q', indexed=True)
    namespace = ndb.KeyProperty('n', indexed=True, required=True)
    subscriber_count = ndb.IntegerProperty('s', indexed=True, default=0)


## MatcherSubscription - represents a user-requested subscription to a unique query
class MatcherSubscription(AppModel):

    ''' A subscription registered with the Prospective Search API. '''

    _use_cache = True
    _use_memcache = True
    _use_datastore = True

    _message_class = messages.Subscription
    _pipeline_class = pipelines.SubscriptionPipeline

    user = ndb.KeyProperty('u', indexed=True, required=True)
    query = ndb.KeyProperty('q', indexed=True, required=True)
    trigger_email = ndb.BooleanProperty('e', indexed=True, default=True)
    trigger_sms = ndb.BooleanProperty('s', indexed=True, default=False)
    trigger_xmpp = ndb.BooleanProperty('x', indexed=True, default=False)
