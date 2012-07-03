# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


## SubscriptionPipeline - fired when a Subscription entity is put/deleted
class SubscriptionPipeline(ModelPipeline):

    ''' Processes subscription puts/deletes. '''

    _model_binding = 'openfire.models.matcher.Subscription'


## AlertPipeline - fired when a Alert entity is put/deleted
class AlertPipeline(ModelPipeline):

    ''' Processes subscription puts/deletes. '''

    _model_binding = 'openfire.models.alerts.Alert'
