## Openfire models

# represents javascript key
class Key extends Model
    constructor: () ->

# a comment
class Comment extends Model

    username: String()
    text: String()

# a content post
class Post extends Model

    username: String()
    text: String()

# A single project card
class ProjectCard extends Model

    name: String()
    project: Key()
    progress: String()
    backer_count: Number()
    met: Boolean()


# a feed item (activity, etc)
class FeedItem extends Model

    timestamp: Date()
    project: Key()
    data: Object()

# Login dialogue - does sam want to fill these out?
class Login extends Model

# Signup - same as ^^^?
class Signup extends Model
