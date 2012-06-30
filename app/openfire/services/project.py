from apptools.services.builtin import Echo
from google.appengine.ext import ndb
from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.messages import project as project_messages
from openfire.messages import common as common_messages
from openfire.messages import media as media_messages
from openfire.models.project import Project


class ProjectService(RemoteService):

    ''' Project service api. '''

    @remote.method(message_types.VoidMessage, project_messages.Projects)
    def list(self, request):

        ''' Returns a list of projects. '''

        projects = Project.query(Project.status != 'p').fetch()
        messages = []
        for project in projects:
            messages.append(project.to_message())
        return project_messages.Projects(projects=messages)

    @remote.method(project_messages.ProjectRequest, project_messages.Project)
    def get(self, request):

        ''' Return a project. '''

        # TODO: Authentication.
        is_owner = False
        is_admin = True

        project_key = ndb.Key(urlsafe=request.key)
        project = project_key.get()

        if not project:
            # Project not found.
            raise remote.ApplicationError('Project not found')

        if project.is_private() and not (is_owner or is_admin):
            # Not allowed to view this project.
            return project_messages.Project()

        return project.to_message()

    @remote.method(project_messages.Project, project_messages.Project)
    def put(self, request):

        ''' Edit a project. Projects are created when proposals are promoted. '''

        if not request.key:
            # Cannot create a project through this service.
            # TODO: How to return error?
            return project_messages.Project()

        project_key = ndb.Key(urlsafe=request.key)
        project = project_key.get()

        # Update the project.
        project.mutate_from_message(request)
        project.slug = "TODO: Remove me! (OF-64)"
        project.put()

        return project.to_message()


    @remote.method(project_messages.ProjectRequest, Echo)
    def go_live(self, request):

        ''' Enable a project to be shown to the general public. '''

        if not request.key:
            # Cannot create a project through this service.
            # TODO: How to return error?
            return project_messages.Project()

        project_key = ndb.Key(urlsafe=request.key)
        project = project_key.get()

        if not project:
            # Project not found.
            raise remote.ApplicationError('Project not found')

        # Update the project to open.
        project.status = 'o'
        project.put()

        return Echo(message='Opened project')


    @remote.method(project_messages.ProjectRequest, Echo)
    def delete(self, request):

        ''' Remove a category. '''

        project_key = ndb.Key(urlsafe=request.key)
        project_key.delete()
        return Echo(message='Project removed')


    @remote.method(common_messages.Comment, Echo)
    def comment(self, request):

        ''' Comment on a project. '''

        return Echo(message='')

    @remote.method(common_messages.Comments, Echo)
    def comments(self, request):

        ''' Return comments for a project. '''

        return common_messages.Comments()

    @remote.method(common_messages.Post, message_types.VoidMessage)
    def post(self, request):

        ''' Post and update to a project. '''

        return None

    @remote.method(message_types.VoidMessage, common_messages.Posts)
    def posts(self, request):

        ''' Return posts for a project. '''

        return common_messages.posts()

    @remote.method(message_types.VoidMessage, media_messages.Media)
    def media(self, request):

        ''' Return media for a project. '''

        return common_messages.Media()

    @remote.method(common_messages.FollowRequest, Echo)
    def follow(self, request):

        ''' Follow a project and return the new follow count. '''

<<<<<<< HEAD
        return Echo(message='cool')
=======
        return Echo(message='')

>>>>>>> 33f69f093df6ddd0fc5711db2f7b5deeb135d7e8

    @remote.method(common_messages.FollowersRequest, common_messages.FollowersResponse)
    def followers(self, request):

        ''' Return followers of a project. '''

        return common_messages.FollowersResponse()

    @remote.method(message_types.VoidMessage, project_messages.Backers)
    def backers(self, request):

        ''' Return backers of a project. '''

        return project_messages.Backers()

    @remote.method(project_messages.BackProject, Echo)
    def back(self, request):

        ''' Become a backer of a project. '''

        return Echo(message='')
<<<<<<< HEAD
=======

>>>>>>> 33f69f093df6ddd0fc5711db2f7b5deeb135d7e8

    @remote.method(project_messages.SuspendProject, Echo)
    def suspend(self, request):

        ''' Suspend a project. '''

        project_key = ndb.Key(urlsafe=request.key)
        project = project_key.get()

        if not project:
            # Project not found.
            raise remote.ApplicationError('Project not found')

        project.status = 'p'
        project.put()
<<<<<<< HEAD
=======

        return Echo(message='Project suspended')
>>>>>>> 33f69f093df6ddd0fc5711db2f7b5deeb135d7e8

        return Echo(message='Project suspended')

    @remote.method(project_messages.ShutdownProject, Echo)
    def shutdown(self, request):

        ''' Shut down a project. '''

        project_key = ndb.Key(urlsafe=request.key)
        project = project_key.get()

        if not project:
            # Project not found.
            raise remote.ApplicationError('Project not found')

        project.status = 'c'
        project.put()

        return Echo(message='Project shut down')
