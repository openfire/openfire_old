# -*- coding: utf-8 -*-
from openfire.pipelines import AppPipeline


## ModelPipeline - abstract parent for all model-triggered pipelines
class ModelPipeline(AppPipeline):

    ''' Abstract parent for all model-triggered pipelines. '''

    _model_binding = None
