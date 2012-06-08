from protorpc import messages
from openfire.messages.common import Goal, Tier

class Project(messages.Message):

    ''' Contains all project fields for users. Can be request or response. '''

    slug = messages.StringField(1)
    name = messages.StringField(2)
    status = messages.StringField(3)
    category = messages.StringField(4)
    summary = messages.StringField(5)
    pitch = messages.StringField(6)
    tech = messages.StringField(7)
    keywords = messages.StringField(8)
    creator = messages.StringField(9)
    owners = messages.StringField(10, repeated=True)
    goals = messages.MessageField(Goal, 11, repeated=True)
    tiers = messages.MessageField(Tier, 12, repeated=True)


class Projects(messages.Message):

    ''' A list of projects. '''

    projects = messages.MessageField(Project, 1, repeated=True)


class ProjectRequest(messages.Message):

    ''' Request project info or edit if project is populated. '''

    project_id = messages.StringField(1)
    project = messages.MessageField(Project, 2)


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
