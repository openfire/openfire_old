# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel


class Role(AppModel):

    ''' Represents a role that a user can play on a project. '''

    slug = ndb.StringProperty('s', indexed=True, required=True)
    name = ndb.StringProperty('n', indexed=True, required=True)
    description = ndb.TextProperty('t', indexed=False, required=True)


class RoleMapping(AppModel):

    ''' Maps a user to a role and a project/proposal. '''

    user = ndb.KeyProperty('u', indexed=True, required=True)
    role = ndb.KeyProperty('r', indexed=True, required=True)
