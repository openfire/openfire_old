# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


class UserPaymentAccountPipeline(ModelPipeline):

    ''' Processes user payment account puts/deletes. '''

    _model_binding = 'openfire.models.payment.UserPaymentAccount'


class ProjectAccountPipeline(ModelPipeline):

    ''' Processes project account puts/deletes. '''

    _model_binding = 'openfire.models.payment.ProjectAccount'


class PaymentPipeline(ModelPipeline):

    ''' Processes payment puts/deletes. '''

    _model_binding = 'openfire.models.payment.Payment'


class TransactionPipeline(ModelPipeline):

    ''' Processes transaction puts/deletes. '''

    _model_binding = 'openfire.models.payment.Transaction'


class MoneySourcePipeline(ModelPipeline):

    ''' Processes money source puts/deletes. '''

    _model_binding = 'openfire.models.payment.MoneySource'
