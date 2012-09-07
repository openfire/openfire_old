# -*- coding: utf-8 -*-
import logging
from openfire.pipelines.model import ModelPipeline


## CategoryPipeline - fired when a Category entity is put/deleted
class CategoryPipeline(ModelPipeline):

    ''' Processes category puts/deletes. '''

    _model_binding = 'openfire.models.project.Category'


## ProposalPipeline - fired when a Proposal entity is put/deleted
class ProposalPipeline(ModelPipeline):

    ''' Processes proposal puts/deletes. '''

    _model_binding = 'openfire.models.project.Proposal'


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


## NextStepPipeline - fired when a NextStep entity is put/deleted
class NextStepPipeline(ModelPipeline):

    ''' Processes next step puts/deletes. '''

    _model_binding = 'openfire.models.project.NextStep'


## FutureGoalPipeline - fired when a FutureGoal entity is put/deleted
class FutureGoalPipeline(ModelPipeline):

    ''' Processes future goal puts/deletes. '''

    _model_binding = 'openfire.models.project.FutureGoal'


## BackerPipeline - fired when a Backer entity is put/deleted
class BackerPipeline(ModelPipeline):

    ''' Processes backer puts/deletes. '''

    _model_binding = 'openfire.models.project.Backer'


## UpdatePipeline - fired when a Update entity is put/deleted
class UpdatePipeline(ModelPipeline):

    ''' Processes update puts/deletes. '''

    _model_binding = 'openfire.models.project.Update'
