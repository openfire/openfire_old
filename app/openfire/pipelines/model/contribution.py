# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


class ContributionPipeline(ModelPipeline):

    ''' Fires when a Contribution is put or deleted. '''

    _model_binding = 'openfire.models.contribution.Contribution'


class ContributionTypePipeline(ModelPipeline):

    ''' Fires when a ContributionType is put or deleted. '''

    _model_binding = 'openfire.models.contribution.ContributionType'
