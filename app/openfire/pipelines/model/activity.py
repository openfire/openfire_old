# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


## ActivityPipeline - fired when a put or delete event is dispatched for an Activity entity
class ActivityPipeline(ModelPipeline):

    ''' Processes activity puts/deletes. '''

    _model_binding = 'openfire.models.activity.Activity'


## ActivityPipeline - fired when a put or delete event is dispatched for an ActivityStream entity
class ActivityStreamPipeline(ModelPipeline):

    ''' Processes activity puts/deletes. '''

    _model_binding = 'openfire.models.activity.ActivityStream'
