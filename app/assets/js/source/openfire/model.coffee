## Openfire models

# represents javascript key
class Key extends Model
    constructor: () ->

# A single project card
class ProjectCard extends Model

    name: String()
    project: Key()
    progress: String()
    backer_count: Number()
    met: Boolean()

# an activity feed item
class ActivityItem extends Model

    timestamp: Date()
    project: Key()

## project activities
class Follow extends ActivityItem

    username: String()
    project: Key()
    timestamp: Date()

class Back extends ActivityItem

    username: String()
    project: Key()
    timestamp: Date()

class Update extends ActivityItem

    username: String()
    text: String()
    timestamp: Date()
    project: Key()

## project updates
class MediaUpdate extends Update

class GoalReached extends Update

class ThresholdReached extends Update

class ProjectOpened extends Update

class ProjectClosed extends Update


## proposal activities
class CreateProposal extends ActivityItem

class ProposalPromoted extends Update

class ProposalDenied extends Update

class ProposalReturned extends Update

## common activities
class AddUserRole extends ActivityItem # project or proposal

class Comment extends ActivityItem

    username: String()
    text: String()

# Login dialogue - does sam want to fill these out?
class Login extends Model

# Signup - same as ^^^?
class Signup extends Model
