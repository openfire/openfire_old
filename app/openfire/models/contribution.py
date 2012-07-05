# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel


## ContributionType - a type of contribution that a user can make to a project
class ContributionType(AppModel):

    ''' A type of contribution that a user can make to a project. '''

    slug = ndb.StringProperty('s', indexed=True, required=True)
    name = ndb.StringProperty('n', indexed=True, required=True)
    unit = ndb.StringProperty('u', indexed=True, required=True)
    plural = ndb.StringProperty('p', indexed=True, required=True)
    subunit = ndb.StringProperty('su', indexed=True, default=None)
    subunit_plural = ndb.StringProperty('sp', indexed=True, default=None)


## Contribution - something given to a project from a user
class Contribution(AppModel):

    ''' Represents a contribution made by a user to a project, making them a `Backer`. '''

    type = ndb.KeyProperty('t', indexed=True, required=True)
    project = ndb.KeyProperty('p', indexed=True, required=True)
    user = ndb.KeyProperty('u', indexed=True, required=True)
    amount = ndb.IntegerProperty('a', indexed=True, required=True)
