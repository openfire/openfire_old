from protorpc import messages
from openfire.messages.common import Goal, FutureGoal


class Backer(messages.Message):

    ''' Represents a single backer. '''

    user = messages.StringField(1)


class Project(messages.Message):

    ''' Contains all project fields for users. Can be request or response. '''

    key = messages.StringField(1)
    name = messages.StringField(2)
    status = messages.StringField(3)
    category = messages.StringField(4)
    customurl = messages.StringField(5)
    summary = messages.StringField(6)
    pitch = messages.StringField(7)
    tech = messages.StringField(8)
    keywords = messages.StringField(9, repeated=True)
    creator = messages.StringField(10)
    owners = messages.StringField(11, repeated=True)
    public = messages.BooleanField(12)
    viewers = messages.StringField(13, repeated=True)
    backers = messages.IntegerField(14)
    followers = messages.IntegerField(15)
    money = messages.FloatField(16)
    progress = messages.IntegerField(17)
    active_goal = messages.StringField(18)
    completed_goals= messages.StringField(19, repeated=True)
    future_goal = messages.StringField(20)


class Projects(messages.Message):

    ''' A list of projects. '''

    projects = messages.MessageField(Project, 1, repeated=True)


class ProjectRequest(messages.Message):

    ''' Request a project by key. '''

    key = messages.StringField(1)
    comment = messages.StringField(2)


class Backers(messages.Message):

    ''' A list of backers of the project. '''

    users = messages.StringField(1, repeated=True)


class BackProject(messages.Message):

    ''' Become a backer of a project. '''

    user = messages.StringField(1)
    project = messages.StringField(2)
    contribution = messages.StringField(3)

class CancelProjectRequest(messages.Message):

    ''' Request to cancel a project by key, with option to refund all charges.. '''

    key = messages.StringField(1)
    refund_all = messages.BooleanField(2)
