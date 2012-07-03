# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


## CategoryPipeline - fired when a Category entity is put/deleted
class CategoryPipeline(ModelPipeline):

    ''' Processes category puts/deletes. '''

    _model_binding = 'openfire.models.project.Category'


## ProjectPipeline - fired when a Project entity is put/deleted
class ProjectPipeline(ModelPipeline):

    ''' Processes project puts/deletes. '''

    _model_binding = 'openfire.models.project.Project'


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
