# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


## CommentPipeline - fired when a Comment entity is put/deleted
class CommentPipeline(ModelPipeline):

    ''' Processes comment puts/deletes. '''

    _model_binding = 'openfire.models.social.Comment'


## FollowPipeline - fired when a Follow entity is put/deleted
class FollowPipeline(ModelPipeline):

    ''' Processes follow puts/deletes. '''

    _model_binding = 'openfire.models.project.Follow'
