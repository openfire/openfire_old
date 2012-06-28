# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel
from google.appengine.ext.ndb import polymodel

from openfire.models.assets import Media
from openfire.models.assets import Avatar
from openfire.models.social import Follow
from openfire.models.social import Comment
from openfire.models.role import RoleMapping

from openfire.messages.project import Project as ProjectMessage
from openfire.messages.proposal import Proposal as ProposalMessage
from openfire.messages.common import Category as CategoryMessage


######## ======== Top-Level Project Models ======== ########

## Project Categories
class Category(AppModel):

    ''' A category for projects and proposals to exist in. '''
    _message_class = CategoryMessage

    # Naming/Ancestry
    slug = ndb.StringProperty('s', indexed=True, required=True)
    name = ndb.StringProperty('n', indexed=True, required=True)
    parent = ndb.KeyProperty('p', indexed=True, default=None)

    # Description
    description = ndb.StringProperty('d', indexed=False, required=True)
    keywords = ndb.StringProperty('k', indexed=True, repeated=True)

    # Counts
    project_count = ndb.IntegerProperty('pc', indexed=True, default=1)
    backer_count = ndb.IntegerProperty('bc', indexed=True, default=1)

    # Timestamps
    modified = ndb.DateTimeProperty('m', auto_now=True, indexed=True)
    created = ndb.DateTimeProperty('c', auto_now_add=True, indexed=True)


## Project Proposals
class Proposal(AppModel):

    ''' A proposal for a project on openfire. '''
    _message_class = ProposalMessage

    # Naming/Status
    slug = ndb.StringProperty('s', indexed=True, required=True)
    name = ndb.StringProperty('n', indexed=True, required=True)
    status = ndb.StringProperty('st', indexed=True, choices=['f', 's', 'r', 'd', 'a'])  # draft, submitted, review, denied, accepted
    category = ndb.KeyProperty('ct', indexed=True, required=True)

    # Content
    summary = ndb.StringProperty('m', indexed=True)
    pitch = ndb.TextProperty('p', indexed=False)
    tech = ndb.TextProperty('t', indexed=False)
    keywords = ndb.StringProperty('k', indexed=True, repeated=True)

    # Users
    creator = ndb.KeyProperty('c', indexed=True, required=True)
    owners = ndb.KeyProperty('o', indexed=True, repeated=True)

    # Privacy
    public = ndb.BooleanProperty('pp', indexed=True, default=False)
    viewers = ndb.KeyProperty('pv', indexed=True, repeated=True)


## Projects
class Project(AppModel):

    ''' An openfire project, also known as a `spark` :) '''

    _message_class = ProjectMessage

    # Naming/Status/Ancestry
    slug = ndb.StringProperty('s', indexed=True, required=True)
    name = ndb.StringProperty('n', indexed=True, required=True)
    status = ndb.StringProperty('st', indexed=True, choices=['p', 'f', 'o', 'c'])  # private, featured, open, closed
    proposal = ndb.KeyProperty('pr', indexed=True, required=True)
    category = ndb.KeyProperty('ct', indexed=True, required=True)

    # Content
    summary = ndb.StringProperty('m', indexed=True)
    pitch = ndb.TextProperty('p', indexed=False)
    tech = ndb.TextProperty('t', indexed=False)
    keywords = ndb.StringProperty('k', indexed=True, repeated=True)

    # Users
    creator = ndb.KeyProperty('c', indexed=True, required=True)
    owners = ndb.KeyProperty('o', indexed=True, repeated=True)

    # Privacy
    public = ndb.BooleanProperty('pp', indexed=True, default=False)
    viewers = ndb.KeyProperty('pv', indexed=True, repeated=True)

    # Progress
    backers = ndb.IntegerProperty('b', default=0)
    followers = ndb.IntegerProperty('f', default=0)
    money = ndb.IntegerProperty('mn', default=0)
    progress = ndb.IntegerProperty('pr', default=0, choices=set(range(0, 100)))

    def is_private(self):
        return self.status == 'p'


## Contribution Goals
class Goal(AppModel):

    ''' Represents a contribution goal for an openfire project. '''

    target = ndb.KeyProperty('t', indexed=True, required=True)
    contribution_type = ndb.KeyProperty('p', indexed=True, required=True)
    amount = ndb.IntegerProperty('a', indexed=True, required=True)
    description = ndb.TextProperty('d', indexed=False)
    backer_count = ndb.IntegerProperty('b', indexed=True, default=0)
    progress = ndb.IntegerProperty('pg', indexed=True, choices=range(0, 100), default=0)
    met = ndb.BooleanProperty('m', indexed=True, default=False)


## Contribution Tiers
class Tier(AppModel):

    ''' Represents a contribution tier for an openfire project. '''

    target = ndb.KeyProperty('t', indexed=True, required=True)
    contribution_type = ndb.KeyProperty('p', indexed=True, required=True)
    amount = ndb.IntegerProperty('a', indexed=True, required=True)
    description = ndb.TextProperty('d', indexed=False)
    backer_count = ndb.IntegerProperty('b', indexed=True, default=0)


######## ======== Project Submodels ======== ########

## Backer - when a user contributes to a project, they have "backed" it
class Backer(AppModel):

    ''' Describes a user who has backed a project. '''

    user = ndb.KeyProperty('u', indexed=True, required=True)
    project = ndb.KeyProperty('p', indexed=True, required=True)
    contributions = ndb.KeyProperty('c', indexed=True, repeated=True)
    anonymous = ndb.BooleanProperty('a', indexed=True, default=False)


## Update - a status/media/engagement update posted on a project by project creators
class Update(AppModel):

    ''' Describes an update posted by project admins. '''

    project = ndb.KeyProperty('p', indexed=True, required=True)
    author = ndb.KeyProperty('u', indexed=True, required=True)
    content = ndb.StringProperty('c', indexed=True, required=True)
