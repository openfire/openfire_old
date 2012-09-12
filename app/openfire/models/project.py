# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel

# Message Classes
from openfire.messages import common
from openfire.messages import project
from openfire.messages import proposal

from openfire.models.assets import Avatar, Video

# Pipeline Classes
from openfire.pipelines.model import project as pipelines

import datetime


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
    project_count = ndb.IntegerProperty('pc', indexed=True, default=0)
    backer_count = ndb.IntegerProperty('bc', indexed=True, default=0)


## Project Contribution Goals
class Goal(AppModel):

    ''' Represents a contribution goal for an openfire project. '''

    _message_class = common.Goal
    _pipeline_class = pipelines.GoalPipeline

    slug = ndb.StringProperty('sl', indexed=True)
    target = ndb.KeyProperty('t', indexed=True, default=None)
    contribution_type = ndb.KeyProperty('p', indexed=True, default=_default_contribution_type)
    approved = ndb.BooleanProperty('aa', default=False)
    rejected = ndb.BooleanProperty('rj', default=False)

    # Description and stats.
    description = ndb.TextProperty('d', indexed=False)
    backer_count = ndb.IntegerProperty('b', indexed=True, default=0)
    progress = ndb.IntegerProperty('pg', indexed=True, default=0)
    met = ndb.BooleanProperty('m', indexed=True, default=False)

    # The target amount.
    amount = ndb.FloatProperty('a', indexed=True, required=True)

    # Pledged and processed amounts.
    amount_pledged = ndb.FloatProperty('ar', indexed=True, default=0.0)
    amount_processed = ndb.FloatProperty('ap', indexed=True, default=0.0)

    # Funding status, limits, and exact times.
    funding_open = ndb.BooleanProperty('fo', indexed=True, default=False)
    funding_day_limit = ndb.IntegerProperty('fl', indexed=True, choices=range(15, 101))
    funding_deadline = ndb.DateTimeProperty('fd', indexed=True, required=False)
    funding_start = ndb.DateTimeProperty('fs', indexed=True, required=False)
    funding_end = ndb.DateTimeProperty('fe', indexed=True, required=False)

    # Deliverable and deadline.
    deliverable_description = ndb.TextProperty('ds', indexed=True)
    deliverable_date = ndb.DateTimeProperty('dt', indexed=True)
    deliverable_complete = ndb.BooleanProperty('dc', indexed=True, default=False)

    # Donation tiers for this goal and potential next steps.
    tiers = ndb.KeyProperty('tr', repeated=True)
    next_steps = ndb.KeyProperty('ns', repeated=True)

    # Payment tracking lists.
    igniting_payments = ndb.KeyProperty('ip', repeated=True)
    extra_payments = ndb.KeyProperty('ep', repeated=True)
    successful_payments = ndb.KeyProperty('sp', repeated=True)

    def open_goal(self):

        ''' Set the funding start to now and set the funding deadline
        to funding limit days from now, then open the goal.
        '''

        now = datetime.datetime.now()
        self.funding_start = now
        self.funding_deadline = now + datetime.timedelta(days=self.funding_day_limit)
        self.funding_open = True
        self.put()

    def close_goal(self):

        ''' Set the goal to closed and note the time. '''

        now = datetime.datetime.now()
        self.funding_end = now
        self.funding_open = False
        self.put()


## Goal Next Step
class NextStep(AppModel):

    '''
    Represents a potential next step for a project after completing the active goal.
    Child object of a goal.
    '''

    _message_class = common.NextStep
    _pipeline_class = pipelines.NextStepPipeline

    summary = ndb.StringProperty('s', indexed=True)
    description = ndb.TextProperty('d', indexed=False)
    votes = ndb.IntegerProperty('v', indexed=True, default=0)


## Ambitious Future Goal
class FutureGoal(AppModel):

    ''' Represents a big ambitious future goal. '''

    _message_class = common.FutureGoal
    _pipeline_class = pipelines.FutureGoalPipeline

    summary = ndb.StringProperty('s', indexed=True)
    description = ndb.TextProperty('d', indexed=False)


## Contribution Tiers
class Tier(AppModel):

    ''' Represents a contribution tier for an openfire project. '''

    _message_class = common.Tier
    _pipeline_class = pipelines.TierPipeline

    name = ndb.StringProperty('n', indexed=False)
    target = ndb.KeyProperty('t', indexed=True, default=None)
    contribution_type = ndb.KeyProperty('p', indexed=True, default=_default_contribution_type)
    amount = ndb.FloatProperty('a', indexed=True, required=True)
    description = ndb.TextProperty('pd', indexed=False)
    delivery = ndb.StringProperty('d', indexed=False)
    next_step_votes = ndb.IntegerProperty('v', indexed=True, default=1)
    backer_count = ndb.IntegerProperty('b', indexed=True, default=0)
    backer_limit = ndb.IntegerProperty('l', indexed=True, default=0)


## Project Proposals
class Proposal(AppModel):

    ''' A proposal for a project on openfire. '''

    _message_class = proposal.Proposal
    _pipeline_class = pipelines.ProposalPipeline

    # Naming/Status
    name = ndb.StringProperty('n', indexed=True, required=True)
    status = ndb.StringProperty('st', indexed=True, choices=['f', 's', 'r', 'd', 'a', 'p'])  # draft, submitted, review, denied, accepted, suspended
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

    # Goals + Tiers
    initial_goal = ndb.LocalStructuredProperty(Goal, 'ig', compressed=True)
    initial_tiers = ndb.LocalStructuredProperty(Tier, 'ts', compressed=True, repeated=True)
    initial_next_steps = ndb.LocalStructuredProperty(NextStep, 'ns', compressed=True, repeated=True)
    future_goal = ndb.LocalStructuredProperty(FutureGoal, 'fg', compressed=True)

    # Avatar + Video
    avatar = ndb.LocalStructuredProperty(Avatar, 'av')
    video = ndb.LocalStructuredProperty(Video, 'vi')


## Projects
class Project(AppModel):

    ''' An openfire project, also known as a `spark` :) '''

    _message_class = project.Project
    _pipeline_class = pipelines.ProjectPipeline

    # Naming/Status/Ancestry
    name = ndb.StringProperty('n', indexed=True, required=True)
    status = ndb.StringProperty('st', indexed=True, choices=['p', 'f', 'o', 'c', 'x', 's'], default='p')  # private, featured, open, closed, canceled, suspended
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
    money = ndb.FloatProperty('mn', default=0.0)
    progress = ndb.IntegerProperty('pro', default=0)

    # Goals
    active_goal = ndb.KeyProperty('ag', indexed=True)
    completed_goals = ndb.KeyProperty('cg', repeated=True)
    future_goal = ndb.KeyProperty('fg', indexed=True)

    # Payments
    payments = ndb.KeyProperty('pm', repeated=True)

    # Avatar + Media
    avatar = ndb.KeyProperty('av')
    images = ndb.KeyProperty('im', repeated=True)
    video = ndb.KeyProperty('vi')

    def is_private(self):
        return (self.status in ['p', 'c']) or (not self.public)

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
