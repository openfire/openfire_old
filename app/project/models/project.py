from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from project.models.assets import Avatar

from project.models.role import RoleMapping

from project.models.assets import Media
from project.models.social import Follow
from project.models.social import Comment


######## ======== Top-Level Project Models ======== ########

## Project Categories
class Category(ndb.Model):

    ''' A category for projects and proposals to exist in. '''

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
class Proposal(ndb.Model):

    ''' A proposal for a project on openfire. '''

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
class Project(ndb.Model):

    ''' An openfire project, also known as a `spark` :) '''

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


## Contribution Goals
class Goal(polymodel.PolyModel):

    ''' Represents a contribution goal for an openfire project. '''

    contribution_type = ndb.KeyProperty('t', indexed=True, required=True)
    amount = ndb.IntegerProperty('a', indexed=True, required=True)
    description = ndb.TextProperty('d', indexed=False)
    backer_count = ndb.IntegerProperty('b', indexed=True, default=0)
    progress = ndb.IntegerProperty('pg', indexed=True, choices=xrange(0, 100), default=0)
    met = ndb.BooleanProperty('m', indexed=True, default=False)


## Contribution Tiers
class Tier(polymodel.PolyModel):

    ''' Represents a contribution tier for an openfire project. '''

    target = ndb.KeyProperty('k', indexed=True, required=True)
    contribution_type = ndb.KeyProperty('t', indexed=True, required=True)
    amount = ndb.IntegerProperty('a', indexed=True, required=True)
    description = ndb.TextProperty('d', indexed=False)
    backer_count = ndb.IntegerProperty('b', indexed=True, default=0)


######## ======== Proposal Submodels ======== ########
class ProposalGoal(Goal):

    ''' Goal attached to a proposal. '''

    proposal = ndb.KeyProperty('pr', indexed=True, required=True)


class ProposalTier(Tier):

    ''' Tier attached to a proposal. '''

    proposal = ndb.KeyProperty('pr', indexed=True, required=True)


class ProposalAvatar(Avatar):

    ''' Maps an avatar to a proposal. '''

    proposal = ndb.KeyProperty('pr', indexed=True, required=True)


class ProposalMedia(Media):

    ''' Describes a piece of media attached to a proposal. '''

    proposal = ndb.KeyProperty('pr', indexed=True, required=True)


class ProposalComment(Comment):

    ''' Describes a comment posted to a proposal. '''

    proposal = ndb.KeyProperty('pr', indexed=True, required=True)


class ProposalRoleMapping(RoleMapping):

    ''' Maps a project to a user and a role. '''

    proposal = ndb.KeyProperty('pr', indexed=True, required=True)


######## ======== Project Submodels ======== ########
class Backer(ndb.Model):

    ''' Describes a user who has backed a project. '''

    user = ndb.KeyProperty('u', indexed=True, required=True)
    project = ndb.KeyProperty('p', indexed=True, required=True)
    contributions = ndb.KeyProperty('c', indexed=True, repeated=True)
    anonymous = ndb.BooleanProperty('a', indexed=True, default=False)


class Update(ndb.Model):

    ''' Describes an update posted by project admins. '''

    project = ndb.KeyProperty('p', indexed=True, required=True)
    author = ndb.KeyProperty('u', indexed=True, required=True)
    content = ndb.StringProperty('c', indexed=True, required=True)


class ProjectTier(Tier):

    ''' Tier attached to a project. '''

    project = ndb.KeyProperty('p', indexed=True, required=True)


class ProjectGoal(Goal):

    ''' Goal attached to a project. '''

    project = ndb.KeyProperty('p', indexed=True, required=True)


class ProjectMedia(Media):

    ''' Describes a piece of media attached to a project. '''

    project = ndb.KeyProperty('p', indexed=True, required=True)


class ProjectAvatar(Avatar):

    ''' Maps an avatar to a proposal. '''

    project = ndb.KeyProperty('p', indexed=True, required=True)


class ProjectFollow(Follow):

    ''' Describes a user's intent to follow a project. '''

    project = ndb.KeyProperty('p', indexed=True, required=True)
    trigger_email = ndb.BooleanProperty('e', indexed=True, default=False)
    trigger_sms = ndb.BooleanProperty('s', indexed=True, default=False)
    trigger_xmpp = ndb.BooleanProperty('x', indexed=True, default=False)


class ProjectComment(Comment):

    ''' Describes a comment posted to a project. '''

    project = ndb.KeyProperty('p', indexed=True, required=True)


class ProjectRoleMapping(RoleMapping):

    ''' Maps a project to a user and a role. '''

    project = ndb.KeyProperty('p', indexed=True, required=True)
