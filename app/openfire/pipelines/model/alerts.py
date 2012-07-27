# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


## NamespacePipeline - fired when a Namespace entity is put/deleted
class NamespacePipeline(ModelPipeline):

    ''' Processes subscription namespace puts/deletes. '''

    _model_binding = 'openfire.models.matcher.MatcherNamespace'


## QueryPipeline - fired when a MatcherQuery entity is put/deleted
class QueryPipeline(ModelPipeline):

    ''' Processes registered query puts/deletes. '''

    _model_binding = 'openfire.models.matcher.MatcherQuery'


## SubscriptionPipeline - fired when a Subscription entity is put/deleted
class SubscriptionPipeline(ModelPipeline):

    ''' Processes subscription puts/deletes. '''

    _model_binding = 'openfire.models.matcher.MatcherSubscription'


## AlertPipeline - fired when a Alert entity is put/deleted
class AlertPipeline(ModelPipeline):

    ''' Processes subscription puts/deletes. '''

    _model_binding = 'openfire.models.alerts.Alert'
