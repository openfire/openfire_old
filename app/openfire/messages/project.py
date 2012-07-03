from protorpc import messages
from openfire.messages.common import Goal, Tier


class Backer(messages.Message):

    ''' Represents a single backer. '''

    pass


class Project(messages.Message):

    ''' Contains all project fields for users. Can be request or response. '''

    key = messages.StringField(1)
    slug = messages.StringField(2)
    name = messages.StringField(3)
    status = messages.StringField(4)
    category = messages.StringField(5)
    summary = messages.StringField(6)
    pitch = messages.StringField(7)
    tech = messages.StringField(8)
    keywords = messages.StringField(9, repeated=True)
    creator = messages.StringField(10)
    owners = messages.StringField(11, repeated=True)
    goals = messages.MessageField(Goal, 12, repeated=True)
    tiers = messages.MessageField(Tier, 13, repeated=True)


class Projects(messages.Message):

    ''' A list of projects. '''

    projects = messages.MessageField(Project, 1, repeated=True)


class ProjectRequest(messages.Message):

    ''' Request a project by slug. '''

    slug = messages.StringField(1)


class Backers(messages.Message):

    ''' A list of backers of the project. '''

    users = messages.StringField(1, repeated=True)


class BackProject(messages.Message):

    ''' Become a backer of a project. '''

    user = messages.StringField(1)
    project = messages.StringField(2)
    contribution = messages.StringField(3)


class ShutdownProject(messages.Message):

    ''' Shutdown a project. '''

    project_id = messages.StringField(1)
    reason = messages.StringField(2)


class SuspendProject(messages.Message):

    ''' Suspend a project. '''

    project_id = messages.StringField(1)
    reason = messages.StringField(2)
