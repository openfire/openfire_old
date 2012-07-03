# -*- coding: utf-8 -*-
import logging
from openfire.pipelines.model import ModelPipeline


## CategoryPipeline - fired when a Category entity is put/deleted
class CategoryPipeline(ModelPipeline):

    ''' Processes category puts/deletes. '''

    _model_binding = 'openfire.models.project.Category'

    def put(self, key, category):

        ''' Fired when a category is put. '''

        logging.info('=== FIRED ON PUT ===')
        logging.info('--CategoryPipeline test was hit on method `put`')
        logging.info('--Was passed this key: "%s".' % key)
        logging.info('--Was passed this category: "%s".' % category)
        logging.info('=== FIRED ON PUT ===')
        return

    def delete(self, key):

        ''' Fired when a category is deleted. '''

        logging.info('=== FIRED ON DELETE ===')
        logging.info('--CategoryPipeline test was hit on method `delete`')
        logging.info('--Was passed this key: "%s".' % key)
        logging.info('=== FIRED ON DELETE ===')
        return


## ProposalPipeline - fired when a Proposal entity is put/deleted
class ProposalPipeline(ModelPipeline):

    ''' Processes proposal puts/deletes. '''

    _model_binding = 'openfire.models.project.Proposal'

    def put(self, key, proposal):

        ''' Fired when a proposal is put. '''

        logging.info('=== FIRED ON PUT ===')
        return

    def delete(self, key):

        ''' Fired when a proposal is deleted. '''

        logging.info('=== FIRED ON DELETE ===')
        return


## ProjectPipeline - fired when a Project entity is put/deleted
class ProjectPipeline(ModelPipeline):

    ''' Processes project puts/deletes. '''

    _model_binding = 'openfire.models.project.Project'

    def put(self, key, project):

        ''' Fired when a project is put. '''

        logging.info('=== FIRED ON PUT ===')
        return

    def delete(self, key):

        ''' Fired when a project is deleted. '''

        logging.info('=== FIRED ON DELETE ===')
        return


## GoalPipeline - fired when a Goal entity is put/deleted
class GoalPipeline(ModelPipeline):

    ''' Processes goal puts/deletes. '''

    _model_binding = 'openfire.models.project.Goal'


## TierPipeline - fired when a Tier entity is put/deleted
class TierPipeline(ModelPipeline):

    ''' Processes tier puts/deletes. '''

    _model_binding = 'openfire.models.project.Tier'


## BackerPipeline - fired when a Backer entity is put/deleted
class BackerPipeline(ModelPipeline):

    ''' Processes backer puts/deletes. '''

    _model_binding = 'openfire.models.project.Backer'


## UpdatePipeline - fired when a Update entity is put/deleted
class UpdatePipeline(ModelPipeline):

    ''' Processes update puts/deletes. '''

    _model_binding = 'openfire.models.project.Update'
