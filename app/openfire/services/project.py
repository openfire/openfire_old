import webapp2
from apptools.services.builtin import Echo
from google.appengine.ext import ndb
from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.messages import project as project_messages
from openfire.messages import common as common_messages
from openfire.messages import media as media_messages
from openfire.models.project import Project, Tier, Goal
from openfire.core.matcher import CoreMatcherAPI


class ProjectService(RemoteService):

    ''' Project service api. '''

    __matcher_api = None

    @webapp2.cached_property
    def matcher(self):

        ''' Cached access to a constructed CoreMatcherAPI. '''

        if self.__matcher_api is None:
            self.__matcher_api = CoreMatcherAPI()

        return self.__matcher_api

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


        try:
            project_key = ndb.Key(urlsafe=self.decrypt(request.key))
        except:
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

        try:
            project_key = ndb.Key(urlsafe=self.decrypt(request.key))
        except:
            project_key = ndb.Key(urlsafe=request.key)
        project = project_key.get()

        if not project:
            raise remote.ApplicationError('Failed to find project')

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

        project_key = ndb.Key(urlsafe=self.decrypt(request.key))
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

        project_key = ndb.Key(urlsafe=self.decrypt(request.key))
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

        return Echo(message='cool')

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

    @remote.method(project_messages.SuspendProject, Echo)
    def suspend(self, request):

        ''' Suspend a project. '''

        project_key = ndb.Key(urlsafe=self.decrypt(request.key))
        project = project_key.get()

        if not project:
            # Project not found.
            raise remote.ApplicationError('Project not found')

        project.status = 'p'
        project.put()

        return Echo(message='Project suspended')

    @remote.method(project_messages.ShutdownProject, Echo)
    def shutdown(self, request):

        ''' Shut down a project. '''

        project_key = ndb.Key(urlsafe=self.decrypt(request.key))
        project = project_key.get()

        if not project:
            # Project not found.
            raise remote.ApplicationError('Project not found')

        project.status = 'c'
        project.put()

        return Echo(message='Project shut down')


    #############################################
    # Project Goals
    #############################################

    @remote.method(common_messages.GoalRequest, common_messages.Goal)
    def get_goal(self, request):

        ''' Get a project goal. '''

        goal_key = ndb.Key(urlsafe=self.decrypt(request.key))
        goal = goal_key.get()
        if not goal:
            raise remote.ApplicationError('Could not find goal.')
        return goal.to_message()


    @remote.method(common_messages.GoalRequest, common_messages.Goals)
    def list_goals(self, request):

        ''' List all goals for a project. '''

        project_key = ndb.Key(urlsafe=self.decrypt(request.project))
        project = project_key.get()
        if not project:
            raise remote.ApplicationError('Failed to find project to list goals for.')

        messages = []
        for goal in project.goals:
            goal_obj = goal.get()
            if goal_obj:
                messages.append(goal_obj.to_message())
        return common_messages.Goals(goals=messages)


    @remote.method(common_messages.Goal, common_messages.Goal)
    def put_goal(self, request):

        ''' Create or edit a project goal. '''

        if not request.target:
            raise remote.ApplicationError('No target to attach goal to.')
        target_key = ndb.Key(urlsafe=request.target)
        target = target_key.get()
        if not target:
            raise remote.ApplicationError('Could not find target for goal.')

        if not request.key:
            # Create a new goal.
            goal = Goal(parent=target_key)
        else:
            # Get the goal to edit.
            goal_key = ndb.Key(urlsafe=request.key)
            goal = goal_key.get()

        if not goal:
            raise remote.ApplicationError('Failed to create goal or find goal to edit.')

        # Update the goal.
        goal.mutate_from_message(request)
        goal.put()

        return goal.to_message()


    @remote.method(common_messages.GoalRequest, Echo)
    def delete_goal(self, request):

        ''' Create or edit a project goal. '''

        goal_key = ndb.Key(urlsafe=self.decrypt(request.key))
        goal_key.delete()
        return Echo(message='OK')


    #############################################
    # Project Tiers
    #############################################

    @remote.method(common_messages.TierRequest, common_messages.Tier)
    def get_tier(self, request):

        ''' Get a project tier. '''

        tier_key = ndb.Key(urlsafe=self.decrypt(request.key))
        tier = tier_key.get()
        if not tier:
            raise remote.ApplicationError('Could not find tier.')
        return tier.to_message()


    @remote.method(common_messages.TierRequest, common_messages.Tiers)
    def list_tiers(self, request):

        ''' List all tiers for a project. '''

        project_key = ndb.Key(urlsafe=self.decrypt(request.project))
        project = project_key.get()
        if not project:
            raise remote.ApplicationError('Failed to find project to list tiers for.')

        messages = []
        for tier in project.tiers:
            tier_obj = tier.get()
            if tier_obj:
                messages.append(tier_obj.to_message())
        return common_messages.Tiers(tiers=messages)


    @remote.method(common_messages.Tier, common_messages.Tier)
    def put_tier(self, request):

        ''' Create or edit a project tier. '''

        if not request.target:
            raise remote.ApplicationError('No target to attach tier to.')
        target_key = ndb.Key(urlsafe=request.target)
        target = target_key.get()
        if not target:
            raise remote.ApplicationError('Could not find target for tier.')

        if not request.key:
            # Create a new tier.
            tier = Tier(parent=target_key)
        else:
            # Get the tier to edit.
            tier_key = ndb.Key(urlsafe=request.key)
            tier = tier_key.get()

        if not tier:
            raise remote.ApplicationError('Failed to create tier or find tier to edit.')

        # Update the tier.
        tier.mutate_from_message(request)
        tier.put()

        return tier.to_message()


    @remote.method(common_messages.TierRequest, Echo)
    def delete_tier(self, request):

        ''' Delete a project tier. '''

        tier_key = ndb.Key(urlsafe=self.decrypt(request.key))
        tier_key.delete()
        return Echo(message='OK')
