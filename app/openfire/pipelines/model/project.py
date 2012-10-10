# -*- coding: utf-8 -*-
import logging
from openfire.pipelines.model import ModelPipeline
from openfire.pipelines.primitive.transport.mail import SendAdminsEmail

PROPOSAL_SUBMITTED_TEXT = """
Hi guys,
    This %(objtype)s has been submitted for our approval.
    %(url)s

    Yours Truely,
        Codebot.
"""

## CategoryPipeline - fired when a Category entity is put/deleted
class CategoryPipeline(ModelPipeline):

    ''' Processes category puts/deletes. '''

    _model_binding = 'openfire.models.project.Category'


## ProposalPipeline - fired when a Proposal entity is put/deleted
class ProposalPipeline(ModelPipeline):

    ''' Processes proposal puts/deletes. '''

    _model_binding = 'openfire.models.project.Proposal'

    def put(self, key, model):

        # Send admins an email when a proposal is submitted for approval.
        if model.status == 's':
            subject = "Proposal waiting for approval: %s" % model.name
            url = 'https://staging.openfi.re/proposal/%s' % key
            body = PROPOSAL_SUBMITTED_TEXT % {'url': url, 'objtype': 'Proposal'}
            pipeline = SendAdminsEmail('codebot@openfi.re', subject, body)
            pipeline.start(queue_name='mail')


## ProjectPipeline - fired when a Project entity is put/deleted
class ProjectPipeline(ModelPipeline):

    ''' Processes project puts/deletes. '''

    _model_binding = 'openfire.models.project.Project'


## GoalPipeline - fired when a Goal entity is put/deleted
class GoalPipeline(ModelPipeline):

    ''' Processes goal puts/deletes. '''

    _model_binding = 'openfire.models.project.Goal'

    def put(self, key, model):

        # Send admins an email when a goal is submitted for approval.
        if model.status == 's':
            project = model.key.parent().get()
            subject = "Project Goal waiting for approval for project: %s" % project.name
            url = 'https://staging.openfi.re/project/%s' % project.key.urlsafe()
            body = PROPOSAL_SUBMITTED_TEXT % {'url': url, 'objtype': 'Project Goal'}
            pipeline = SendAdminsEmail('codebot@openfi.re', subject, body)
            pipeline.start(queue_name='mail')


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
