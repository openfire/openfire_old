# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel

# Message Classes
from openfire.messages import common
from openfire.messages import project
from openfire.messages import proposal

# Pipeline Classes
from openfire.pipelines.model import project as pipelines


_default_contribution_type = ndb.Key('ContributionType', 'money')


######## ======== Top-Level Project Models ======== ########

## Project Categories
class Category(AppModel):

    ''' A category for projects and proposals to exist in. '''

    _message_class = common.Category
    _pipeline_class = pipelines.CategoryPipeline

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


## Contribution Goals
class Goal(AppModel):

    ''' Represents a contribution goal for an openfire project. '''

    _message_class = common.Goal
    _pipeline_class = pipelines.GoalPipeline

    target = ndb.KeyProperty('t', indexed=True, default=None)
    contribution_type = ndb.KeyProperty('p', indexed=True, default=_default_contribution_type)
    amount = ndb.IntegerProperty('a', indexed=True, required=True)
    description = ndb.TextProperty('d', indexed=False)
    backer_count = ndb.IntegerProperty('b', indexed=True, default=0)
    progress = ndb.IntegerProperty('pg', indexed=True, choices=range(0, 100), default=0)
    met = ndb.BooleanProperty('m', indexed=True, default=False)


## Contribution Tiers
class Tier(AppModel):

    ''' Represents a contribution tier for an openfire project. '''

    _message_class = common.Tier
    _pipeline_class = pipelines.TierPipeline

    name = ndb.StringProperty('n', indexed=False)
    target = ndb.KeyProperty('t', indexed=True, default=None)
    contribution_type = ndb.KeyProperty('p', indexed=True, default=_default_contribution_type)
    amount = ndb.IntegerProperty('a', indexed=True, required=True)
    description = ndb.TextProperty('pd', indexed=False)
    delivery = ndb.DateProperty('d', indexed=True)
    backer_count = ndb.IntegerProperty('b', indexed=True, default=0)
    backer_limit = ndb.IntegerProperty('l', indexed=True, default=0)


## Project Proposals
class Proposal(AppModel):

    ''' A proposal for a project on openfire. '''

    _message_class = proposal.Proposal
    _pipeline_class = pipelines.ProposalPipeline

    # Naming/Status
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

    # Tiers + Goals
    tiers = ndb.LocalStructuredProperty(Tier, 'tr', repeated=True, compressed=True)
    goals = ndb.LocalStructuredProperty(Goal, 'gl', repeated=True, compressed=True)


## Projects
class Project(AppModel):

    ''' An openfire project, also known as a `spark` :) '''

    _message_class = project.Project
    _pipeline_class = pipelines.ProjectPipeline

    # Naming/Status/Ancestry
    name = ndb.StringProperty('n', indexed=True, required=True)
    status = ndb.StringProperty('st', indexed=True, choices=['p', 'f', 'o', 'c'])  # private, featured, open, closed
    proposal = ndb.KeyProperty('pr', indexed=True, required=True)
    category = ndb.KeyProperty('ct', indexed=True, required=True)
    customurl = ndb.KeyProperty('url', indexed=True, default=None)

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

    # Tiers + Goals
    tiers = ndb.KeyProperty('tr', repeated=True)
    goals = ndb.KeyProperty('gl', repeated=True)

    def is_private(self):
        return self.status not in ['p', 'c']

    def get_custom_url(self):
        if self.customurl:
            return self.customurl.id()
        return None


######## ======== Project Submodels ======== ########

## Backer - when a user contributes to a project, they have "backed" it
class Backer(AppModel):

    ''' Describes a user who has backed a project. '''

    _message_class = project.Backer
    _pipeline_class = pipelines.BackerPipeline

    user = ndb.KeyProperty('u', indexed=True, required=True)
    project = ndb.KeyProperty('p', indexed=True, required=True)
    contributions = ndb.KeyProperty('c', indexed=True, repeated=True)
    anonymous = ndb.BooleanProperty('a', indexed=True, default=False)


## Update - a status/media/engagement update posted on a project by project creators
class Update(AppModel):

    ''' Describes an update posted by project admins. '''

    _message_class = common.Post
    _pipeline_class = pipelines.UpdatePipeline

    project = ndb.KeyProperty('p', indexed=True, required=True)
    author = ndb.KeyProperty('u', indexed=True, required=True)
    content = ndb.StringProperty('c', indexed=True, required=True)
