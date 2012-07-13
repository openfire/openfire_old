from protorpc import messages


class CategoryRequest(messages.Message):

    ''' A request for a category by slug. '''

    slug = messages.StringField(1)
    key = messages.StringField(2)


class Category(messages.Message):

    ''' A project or proposal category. '''

    key = messages.StringField(1)
    slug = messages.StringField(2)
    name = messages.StringField(3)
    description = messages.StringField(4)
    # TODO: Fill in remaining category items.


class Categories(messages.Message):

    ''' A list of categories. '''

    categories = messages.MessageField(Category, 1, repeated=True)


class CustomUrl(messages.Message):

    ''' A message to be used for custom urls. '''

    key = messages.StringField(1)
    slug = messages.StringField(2)
    target = messages.StringField(3)


class CustomUrls(messages.Message):

    ''' A list of custom urls. '''

    urls = messages.MessageField(CustomUrl, 1, repeated=True)


class CustomUrlCheck(messages.Message):

    ''' A message to be used for custom url check responses. '''

    slug = messages.StringField(1)
    taken = messages.BooleanField(2)
    suggestions = messages.StringField(3, repeated=True)


class Goal(messages.Message):

    ''' Common to proposals and projects, defines a funding goal. '''

    key = messages.StringField(1)
    target = messages.StringField(2)
    contribution_type = messages.StringField(3)
    amount = messages.IntegerField(4)
    description = messages.StringField(5)
    backer_count = messages.IntegerField(6)
    progress = messages.IntegerField(7)
    met = messages.BooleanField(8)


class Goals(messages.Message):

    ''' A list of project goals. '''

    goals = messages.MessageField(Goal, 1, repeated=True)
    project = messages.StringField(2)


class GoalRequest(messages.Message):

    ''' Request a project goal by key. '''

    key = messages.StringField(1)
    project = messages.StringField(2)


class Tier(messages.Message):

    ''' Common to proposals and projects, defines a contribution tier. '''

    key = messages.StringField(1)
    target = messages.StringField(2)
    name = messages.StringField(3)
    contribution_type = messages.StringField(4)
    amount = messages.IntegerField(5)
    description = messages.StringField(6)
    delivery = messages.StringField(7)
    backer_count = messages.IntegerField(8)
    backer_limit = messages.IntegerField(9)


class Tiers(messages.Message):

    ''' A list of project tiers. '''

    tiers = messages.MessageField(Tier, 1, repeated=True)
    project = messages.StringField(2)


class TierRequest(messages.Message):

    ''' Request a project tier by key. '''

    key = messages.StringField(1)
    project = messages.StringField(2)


class Comment(messages.Message):

    ''' Comment on something. '''

    username = messages.StringField(1)
    text = messages.StringField(2)


class Comments(messages.Message):

    ''' A list of comments. '''

    comments = messages.MessageField(Comment, 1, repeated=True)


class Post(messages.Message):

    ''' Post something. '''

    username = messages.StringField(1)
    text = messages.StringField(2)


class Posts(messages.Message):

    ''' A list of posts. '''

    posts = messages.MessageField(Post, 1, repeated=True)


class Follow(messages.Message):

    ''' Represents a user Follow. @TODO: Fill this out. '''

    pass


class FollowRequest(messages.Message):

    ''' Request to follow a user. '''

    user = messages.StringField(1)


class FollowersRequest(messages.Message):

    ''' Request to see the followers of a user '''

    user = messages.StringField(1)


class FollowersResponse(messages.Message):

    ''' Response containing a list of follower usernames. '''

    profiles = messages.StringField(1, repeated=True)
