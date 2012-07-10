# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


## ContributionPipeline - fired when a Contribution record is put/deleted
class ContributionPipeline(ModelPipeline):

    ''' Fires when a Contribution is put or deleted. '''

    _model_binding = 'openfire.models.contribution.Contribution'


## ContributionTypePipeline - fired when a ContributionType is put/deleted
class ContributionTypePipeline(ModelPipeline):

    ''' Fires when a ContributionType is put or deleted. '''

    _model_binding = 'openfire.models.contribution.ContributionType'
