# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


## ContentAreaPipeline - fired when a put or delete event is dispatched for a ContentArea entity
class ContentAreaPipeline(ModelPipeline):

    ''' Fires when a content area is saved or deleted. '''

    _model_binding = 'openfire.models.content.ContentArea'


## ContentSnippetPipeline - fired when a put or delete event is dispatched for a ContentSnippet entity
class ContentSnippetPipeline(ModelPipeline):

    ''' Fires when a content snippet is saved or deleted. '''

    _model_binding = 'openfire.models.content.ContentSnippet'


## ContentSummaryPipeline - fired when a put or delete event is dispatched for a ContentSummary entity
class ContentSummaryPipeline(ModelPipeline):

    ''' Fires when a content summary is saved or deleted. '''

    _model_binding = 'openfire.models.content.ContentSummary'
