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
