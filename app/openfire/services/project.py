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

        projects = Project.query(Project.status!='p').fetch()
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

        project_key = ndb.Key('Project', request.project_id)
        project = project_key.get(use_memcache=False)

        if not project:
            # Project not found.
            raise remote.ApplicationError('Project not found')

        if project.is_private() and not (is_owner or is_admin):
            # Not allowed to view this project.
            return project_messages.Project()

        return project.to_message()


    @remote.method(project_messages.ProjectRequest, project_messages.Project)
    def put(self, request):

        ''' Create or edit a project. '''

        return project_messages.Project()


    @remote.method(common_messages.Comment, Echo)
    def comment(self, request):

        ''' Comment on a project. '''

        return Echo('')


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


    @remote.method(media_messages.AddMedia, media_messages.Media)
    def add_media(self, request):

        ''' Add media to a project. '''

        return media_messages.Media()


    @remote.method(message_types.VoidMessage, media_messages.Media)
    def media(self, request):

        ''' Return media for a project. '''

        return common_messages.Media()


    @remote.method(common_messages.FollowRequest, Echo)
    def follow(self, request):

        ''' Follow a project and return the new follow count. '''

        return Echo('')


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

        return Echo('')


    @remote.method(project_messages.SuspendProject, Echo)
    def suspend(self, request):

        ''' Suspend a project. '''

        return Echo('')


    @remote.method(project_messages.ShutdownProject, Echo)
    def shutdown(self, request):

        ''' Shut down a project. '''

        return Echo('')
