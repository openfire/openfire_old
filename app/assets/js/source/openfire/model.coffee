## Openfire models

# represents javascript key
class Key # extends Model

    constructor: (@key) ->
        return @

# A single project card
class ProjectCard # extends Model

    name: String()
    project: Key()
    progress: String()
    backer_count: Number()
    met: Boolean()

# an activity feed item
class ActivityItem # extends Model

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

## media
class Asset

    constructor: (hash) ->

        if hash? and Util.is_object hash
            @[prop] = val for prop, val of hash

        return @