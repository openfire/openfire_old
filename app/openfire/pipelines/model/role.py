# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


## RolePipeline - fired when a Role entity is put/deleted
class RolePipeline(ModelPipeline):

    ''' Processes role puts/deletes. '''

    _model_binding = 'openfire.models.role.Role'


## RoleMappingPipeline - fired when a RoleMapping entity is put/deleted
class RoleMappingPipeline(ModelPipeline):

    ''' Processes role mapping puts/deletes. '''

    _model_binding = 'openfire.models.role.RoleMapping'
