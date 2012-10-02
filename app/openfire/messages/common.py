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


class TopicRequest(messages.Message):

    ''' A request for a topic by slug. '''

    slug = messages.StringField(1)
    key = messages.StringField(2)


class Topic(messages.Message):

    ''' A user topic. '''

    key = messages.StringField(1)
    slug = messages.StringField(2)
    name = messages.StringField(3)
    description = messages.StringField(4)
    user_count = messages.IntegerField(5)


class Topics(messages.Message):

    ''' A list of topics. '''

    topics = messages.MessageField(Topic, 1, repeated=True)


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


class Tier(messages.Message):

    '''
    Common to proposals and projects, defines a contribution tier.
    Required: (key, target)
    '''

    key = messages.StringField(1)
    target = messages.StringField(2)
    name = messages.StringField(3)
    contribution_type = messages.StringField(4)
    amount = messages.FloatField(5)
    description = messages.StringField(6)
    delivery = messages.StringField(7)
    next_step_votes = messages.IntegerField(8)
    backer_count = messages.IntegerField(9)
    backer_limit = messages.IntegerField(10)


class NextStep(messages.Message):

    ''' A next step for a goal. '''

    key = messages.StringField(1)
    summary = messages.StringField(2)
    description = messages.StringField(3)
    votes = messages.IntegerField(4)


class Goal(messages.Message):

    '''
    Common to proposals and projects, defines a funding goal.
    Required: (key, target)
    '''

    key = messages.StringField(1)
    target = messages.StringField(2)
    contribution_type = messages.StringField(3)
    approved = messages.BooleanField(4)
    rejected = messages.BooleanField(5)
    amount = messages.FloatField(6)
    description = messages.StringField(7)
    backer_count = messages.IntegerField(8)
    progress = messages.IntegerField(9)
    met = messages.BooleanField(10)
    created = messages.StringField(11)
    modified = messages.StringField(12)
    amount_pledged = messages.FloatField(13)
    amount_processed = messages.FloatField(14)
    funding_day_limit = messages.IntegerField(15)
    funding_deadline = messages.StringField(16)
    deliverable_description = messages.StringField(17)
    deliverable_date = messages.StringField(18)
    tiers = messages.MessageField(Tier, 19, repeated=True)
    next_steps = messages.MessageField(NextStep, 20, repeated=True)


class Goals(messages.Message):

    ''' A list of project goals. '''

    goals = messages.MessageField(Goal, 1, repeated=True)
    project = messages.StringField(2)


class GoalRequest(messages.Message):

    ''' Used to request a project goal by key, or active and future goals by project. '''

    key = messages.StringField(1)
    project = messages.StringField(2)


class ProposeGoal(messages.Message):

    ''' Used to propose a new goal. '''

    project = messages.StringField(1)
    amount = messages.FloatField(2)
    description = messages.StringField(3)
    funding_day_limit = messages.IntegerField(4)
    deliverable_description = messages.StringField(5)
    deliverable_date = messages.StringField(6)


class Tiers(messages.Message):

    ''' A list of project tiers. '''

    tiers = messages.MessageField(Tier, 1, repeated=True)
    project = messages.StringField(2)


class TierRequest(messages.Message):

    ''' Request a project tier by key or a list of tiers by project goal. '''

    key = messages.StringField(1)
    goal = messages.StringField(2)


class NextSteps(messages.Message):

    ''' A group of next steps for a goal. '''

    goal = messages.StringField(1)
    next_steps = messages.MessageField(NextStep, 2, repeated=True)


class NextStepVote(messages.Message):

    ''' A nubmer of next step votes for a single next step. '''

    key = messages.StringField(1)
    num_votes = messages.IntegerField(2)


class FutureGoal(messages.Message):

    ''' A big future goal. '''

    key = messages.StringField(1)
    summary = messages.StringField(2)
    description = messages.StringField(3)


class Comment(messages.Message):

    ''' An existing comment. '''

    class Commenter(messages.Message):

		''' Represents a user attached to a comment. '''

		username = messages.StringField(1)
		profile = messages.StringField(2)
		firstname = messages.StringField(3)
		lastname = messages.StringField(4)
		is_admin = messages.BooleanField(5)
		avatar = messages.StringField(6)

    text = messages.StringField(1)
    timestamp = messages.StringField(2)
    timeago = messages.StringField(3)
    author = messages.MessageField(Commenter, 4)
    subject = messages.StringField(5)


class Comments(messages.Message):

    ''' A list of comments. '''

    comments = messages.MessageField(Comment, 1, repeated=True)
    count = messages.IntegerField(2)
    subject = messages.StringField(3)

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


class ViewerRequest(messages.Message):

    ''' Used to add and remove viewers from projects and proposals. '''

    user = messages.StringField(1)
    target = messages.StringField(2)
