# -*- coding: utf-8 -*-
import logging
from openfire.pipelines.model import ModelPipeline


## CommentPipeline - fired when a Comment entity is put/deleted
class CommentPipeline(ModelPipeline):

    ''' Processes comment puts/deletes. '''

    _model_binding = 'openfire.models.social.Comment'

    def put(self, key, comment):

        ''' Fired when a comment is put. '''

        logging.info('=== FIRED ON PUT ===')
        return

    def delete(self, key):

        ''' Fired when a comment is deleted. '''

        logging.info('=== FIRED ON DELETE ===')
        return


## FollowPipeline - fired when a Follow entity is put/deleted
class FollowPipeline(ModelPipeline):

    ''' Processes follow puts/deletes. '''

    _model_binding = 'openfire.models.project.Follow'

    def put(self, key, follow):

        ''' Fired when a follow is put. '''

        logging.info('=== FIRED ON PUT ===')
        return

    def delete(self, key):

        ''' Fired when a follow is deleted. '''

        logging.info('=== FIRED ON DELETE ===')
        return
