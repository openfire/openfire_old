# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel

# Model Attachments
from openfire.messages import role as messages
from openfire.pipelines.model import role as pipelines


class Role(AppModel):

    ''' Represents a role that a user can play on a project. '''

    _message_class = messages.Role
    _pipeline_class = pipelines.RolePipeline

    slug = ndb.StringProperty('s', indexed=True, required=True)
    name = ndb.StringProperty('n', indexed=True, required=True)
    description = ndb.TextProperty('t', indexed=False, required=True)


class RoleMapping(AppModel):

    ''' Maps a user to a role and a project/proposal. '''

    _message_class = messages.RoleMapping
    _pipeline_class = pipelines.RoleMappingPipeline

    user = ndb.KeyProperty('u', indexed=True, required=True)
    role = ndb.KeyProperty('r', indexed=True, required=True)
