# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


## TopicPipeline - fired when a Topic entity is put/deleted
class TopicPipeline(ModelPipeline):

    ''' Processes topic puts/deletes. '''

    _model_binding = 'openfire.models.user.Topic'


## UserPipeline - fired when a User entity is put/deleted
class UserPipeline(ModelPipeline):

    ''' Processes user puts/deletes. '''

    _model_binding = 'openfire.models.user.User'


## EmailAddressPipeline - fired when a EmailAddress entity is put/deleted
class EmailAddressPipeline(ModelPipeline):

    ''' Processes email address puts/deletes. '''

    _model_binding = 'openfire.models.user.EmailAddress'


## PermissionsPipeline - fired when a Permissions entity is put/deleted
class PermissionsPipeline(ModelPipeline):

    ''' Processes permission puts/deletes. '''

    _model_binding = 'openfire.models.user.Permissions'


## SocialAccountPipeline - fired when a SocialAccount entity is put/deleted
class SocialAccountPipeline(ModelPipeline):

    ''' Processes social account puts/deletes. '''

    _model_binding = 'openfire.models.user.SocialAccount'
