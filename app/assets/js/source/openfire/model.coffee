## Openfire models

# A single project card
class ProjectCard  extends Model

    model:
        name: String()
        project: Key
        progress: String()
        backer_count: Number()
        met: Boolean()

# an activity feed item
class ActivityItem extends Model

    model:
        timestamp: Date()
        project: Key

## project activities
class Follow extends ActivityItem

    model:
        username: String()
        project: Key
        timestamp: Date()

class Back extends ActivityItem

    model:
        username: String()
        project: Key
        timestamp: Date()

class Update extends ActivityItem

    model:
        username: String()
        text: String()
        timestamp: Date()
        project: Key

## media
class Asset extends Model


# Classes common to proposals and projects.


class Tier extends Model

    model:
        key: String()
        target: String()
        name: String()
        contribution_type: String()
        amount: Number()
        description: String()
        delivery: String()
        next_step_votes: Number()
        backer_count: Number()
        backer_limit: Number()


class NextStep extends Model

    model:
        key: String()
        summary: String()
        description: String()
        votes: Number()

class Goal extends Model

    model:
        key: String()
        target: String()
        contribution_type: String()
        approved: Boolean()
        rejected: Boolean()
        amount: Number()
        description: String()
        backer_count: Number()
        progress: Number()
        met: Boolean()
        created: String()
        modified: String()
        amount_pledged: Number()
        amount_processed: Number()
        funding_day_limit: Number()
        funding_deadline: String()
        deliverable_description: String()
        deliverable_date: String()
        tiers: ListField(Tier)
        next_steps: ListField(NextStep)



@__openfire_preinit.abstract_base_classes.push Follow, Asset, Goal, Tier, NextStep
