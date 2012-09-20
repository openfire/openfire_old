import webapp2
from apptools.services.builtin import Echo
from google.appengine.ext import ndb
from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.messages import project as project_messages
from openfire.messages import common as common_messages
from openfire.messages import media as media_messages
from openfire.models.project import Project, Tier, Goal, NextStep
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

        ''' Edit an existing project. Projects are created only when proposals are promoted. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('Failed to find project')

        project = ndb.Key(urlsafe=self.decrypt(request.key)).get()
        if not project:
            raise remote.ApplicationError('Failed to find project')

        # Update the project.
        project.mutate_from_message(request)
        project.put()

        return project.to_message()

    @remote.method(project_messages.ProjectRequest, Echo)
    def go_live(self, request):

        ''' Enable a project to be shown to the general public. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('Failed to find project')

        project = ndb.Key(urlsafe=self.decrypt(request.key)).get()
        if not project:
            raise remote.ApplicationError('Failed to find project')

        # Update the project to open.
        project.status = 'o'
        project.public = True
        project.put()

        return Echo(message='Opened project')


    @remote.method(project_messages.ProjectRequest, Echo)
    def delete(self, request):

        ''' Remove a category. '''

        # TODO: Permissions.
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

    @remote.method(project_messages.ProjectRequest, Echo)
    def suspend(self, request):

        ''' Suspend a project. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('Failed to find project')

        project = ndb.Key(urlsafe=self.decrypt(request.key)).get()
        if not project:
            raise remote.ApplicationError('Failed to find project')

        # Set the status to suspended.
        project.status = 's'
        project.public = False
        project.put()

        return Echo(message='Project suspended')

    @remote.method(project_messages.ProjectRequest, Echo)
    def shutdown(self, request):

        ''' Shut down a project. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('Failed to find project')

        project = ndb.Key(urlsafe=self.decrypt(request.key)).get()
        if not project:
            raise remote.ApplicationError('Failed to find project')

        project.status = 'c'
        project.public = False
        project.put()

        return Echo(message='Project shut down')

    @remote.method(project_messages.ProjectRequest, Echo)
    def cancel(self, request):

        ''' Cancel a project and potentially refund all charges. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('Failed to find project')

        project = ndb.Key(urlsafe=self.decrypt(request.key)).get()
        if not project:
            raise remote.ApplicationError('Failed to find project')

        project.status = 'x'
        project.public = False
        project.put()

        # TODO: Cancel all pending payments.

        return Echo(message='Project canceled')


    #############################################
    # Project Goals
    #############################################

    @remote.method(common_messages.GoalRequest, common_messages.Goal)
    def get_goal(self, request):

        ''' Get a project goal. '''

        # TODO: Permissions.
        goal_key = ndb.Key(urlsafe=self.decrypt(request.key))
        goal = goal_key.get()
        if not goal:
            raise remote.ApplicationError('Could not find goal.')
        return goal.to_message()

    @remote.method(common_messages.GoalRequest, common_messages.Goal)
    def active_goal(self, request):

        ''' Return the active goal for a project. '''

        # TODO: Permissions.
        project_key = ndb.Key(urlsafe=self.decrypt(request.project))
        project = project_key.get()
        if not project:
            raise remote.ApplicationError('Failed to find project to get active goal for.')

        if not project.active_goal:
            raise remote.ApplicationError('No active goal has been set for this project.')

        return project.active_goal.get().to_message()

    @remote.method(common_messages.GoalRequest, common_messages.Goals)
    def completed_goals(self, request):

        ''' List all completed goals for a project. '''

        # TODO: Permissions.
        project_key = ndb.Key(urlsafe=self.decrypt(request.project))
        project = project_key.get()
        if not project:
            raise remote.ApplicationError('Failed to find project to list goals for.')

        messages = []
        for goal in project.completed_goals:
            goal_obj = goal.get()
            if goal_obj:
                messages.append(goal_obj.to_message())
        return common_messages.Goals(goals=messages)

    @remote.method(common_messages.GoalRequest, common_messages.FutureGoal)
    def future_goal(self, request):

        ''' Return the future goal for a project. '''

        # TODO: Permissions.
        project_key = ndb.Key(urlsafe=self.decrypt(request.project))
        project = project_key.get()
        if not project:
            raise remote.ApplicationError('Failed to find project to get future goal for.')

        future_goal_key = project.future_goal
        if not future_goal_key:
            raise remote.ApplicationError('No future goal has been set for this project.')

        return future_goal_key.get().to_message()

    @remote.method(common_messages.Goal, common_messages.Goal)
    def put_goal(self, request):

        ''' Create or edit a project goal. '''

        # TODO: Permissions.
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
        # TODO: Exclude some fields so users can't update things like status and amount.
        goal.mutate_from_message(request)
        goal.put()
        return goal.to_message()

    @remote.method(common_messages.FutureGoal, common_messages.FutureGoal)
    def put_future_goal(self, request):

        ''' Edit the future goal for a project. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('Provided no future goal key.')

        future_goal_key = ndb.Key(urlsafe=self.decrypt(request.key))
        future_goal = future_goal_key.get()
        if not future_goal:
            raise remote.ApplicationError('Provided bad future goal key.')

        future_goal.mutate_from_message(request)
        future_goal.put()
        return future_goal.to_message()

    @remote.method(common_messages.GoalRequest, Echo)
    def delete_goal(self, request):

        ''' Create or edit a project goal. '''

        # TODO: Permissions.
        goal_key = ndb.Key(urlsafe=self.decrypt(request.key))
        goal_key.delete()
        return Echo(message='OK')

    @remote.method(common_messages.ProposeGoal, common_messages.Goal)
    def propose_goal(self, request):

        ''' Propose a new goal for a project. '''

        # TODO: Permissions.
        if not request.project:
            raise remote.ApplicationError('No project to propose goal for.')
        project = ndb.Key(urlsafe=request.project).get()
        if not project:
            raise remote.ApplicationError('Could not find project to propose goal for.')

        goal = Goal(parent=project.key, approved=False)
        goal.mutate_from_message(request)
        goal.put()
        return goal.to_message()

    @remote.method(common_messages.GoalRequest, common_messages.Goals)
    def proposed_goals(self, request):

        ''' List all proposed goals for a project. '''

        # TODO: Permissions.
        project_key = ndb.Key(urlsafe=self.decrypt(request.project))
        project = project_key.get()
        if not project:
            raise remote.ApplicationError('Failed to find project to list proposed goals for.')

        messages = []
        goals = Goal.query(Goal.approved == False, ancestor=project_key).fetch()
        for goal in goals:
            messages.append(goal.to_message())
        return common_messages.Goals(goals=messages)

    @remote.method(common_messages.GoalRequest, common_messages.Goal)
    def approve_goal(self, request):

        ''' Approve a goal and set it as the active goal. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('No goal to approve.')
        new_goal = ndb.Key(urlsafe=request.key).get()
        project = new_goal.parent.get()
        if not project:
            raise remote.ApplicationError('Failed to find project to approve goal for.')

        if project.active_goal:
            # If there was an active goal, make sure it is closed and move it to completed.
            active_goal = project.active_goal.get()
            if not active_goal:
                raise remote.ApplicationError('Internal error: bad active goal key.')

            if active_goal.funding_open:
                active_goal.close_goal()
            project.completed_goals.append(project.active_goal)

        new_goal.approved = True
        new_goal.put()
        project.active_goal = new_goal.key
        project.put()
        return new_goal.to_message()

    @remote.method(common_messages.GoalRequest, common_messages.Goal)
    def reject_goal(self, request):

        ''' Reject a request for a new goal. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('No goal to reject.')
        goal = ndb.Key(urlsafe=request.key).get()
        goal.approved = False
        goal.rejected = True
        goal.put()
        return goal.to_message()


    #############################################
    # Project Goal Tiers
    #############################################

    @remote.method(common_messages.TierRequest, common_messages.Tier)
    def get_tier(self, request):

        ''' Get a project tier. '''

        # TODO: Permissions.
        tier_key = ndb.Key(urlsafe=self.decrypt(request.key))
        tier = tier_key.get()
        if not tier:
            raise remote.ApplicationError('Could not find tier.')
        return tier.to_message()

    @remote.method(common_messages.TierRequest, common_messages.Tiers)
    def list_tiers(self, request):

        ''' List all tiers for a project goal. '''

        # TODO: Permissions.
        if not request.goal:
            raise remote.ApplicationError('No goal provided to list tiers for.')
        goal = ndb.Key(urlsafe=self.decrypt(request.goal)).get()
        if not goal:
            raise remote.ApplicationError('Failed to find goal to list tiers for.')

        messages = []
        for tier in goal.tiers:
            tier_obj = tier.get()
            if tier_obj:
                messages.append(tier_obj.to_message())
        return common_messages.Tiers(tiers=messages)

    @remote.method(common_messages.Tier, common_messages.Tier)
    def put_tier(self, request):

        ''' Create or edit a project goal tier. '''

        # TODO: Permissions.
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

        ''' Delete a project goal tier. '''

        # TODO: Permissions.
        tier_key = ndb.Key(urlsafe=self.decrypt(request.key))
        tier_key.delete()
        return Echo(message='OK')


    #############################################
    # Project Goal Next Steps
    #############################################

    @remote.method(common_messages.NextStep, common_messages.NextStep)
    def get_next_step(self, request):

        ''' Get a project next step. '''

        # TODO: Permissions.
        next_step_key = ndb.Key(urlsafe=self.decrypt(request.key))
        next_step = next_step_key.get()
        if not next_step:
            raise remote.ApplicationError('Could not find next step.')
        return next_step.to_message()

    @remote.method(common_messages.NextSteps, common_messages.NextSteps)
    def list_next_steps(self, request):

        ''' List all next steps for a project goal. '''

        # TODO: Permissions.
        if not request.goal:
            raise remote.ApplicationError('No goal provided to list next steps for.')
        goal = ndb.Key(urlsafe=self.decrypt(request.goal)).get()
        if not goal:
            raise remote.ApplicationError('Failed to find goal to list next steps for.')

        messages = []
        for next_step in goal.next_steps:
            next_step_obj = next_step.get()
            if next_step_obj:
                messages.append(next_step_obj.to_message())
        return common_messages.NextSteps(next_steps=messages)

    @remote.method(common_messages.NextStep, common_messages.NextStep)
    def put_next_step(self, request):

        '''
        Create or edit a project next step.
        Accepts either a next step key for edit, or a goal key for add.
        '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('No goal or key for next step to.')
        next_step = None
        goal = None
        key = ndb.Key(urlsafe=request.key)
        if key.kind() == 'NextStep':
            next_step = key.get()
            if not next_step:
                raise remote.ApplicationError('Bad next step key.')

        elif key.kind() == 'Goal':
            goal = key.get()
            if not goal:
                raise remote.ApplicationError('Bad goal for next step.')

        else:
            raise remote.ApplicationError('Invalid key.')

        if not next_step:
            next_step = NextStep(parent=goal.key)

        if not next_step:
            raise remote.ApplicationError('Failed to create next step or find next step to edit.')

        # Update the next_step and return it.
        next_step.mutate_from_message(request)
        next_step.put()
        return next_step.to_message()

    @remote.method(common_messages.NextStep, Echo)
    def delete_next_step(self, request):

        ''' Delete a project next_step. '''

        # TODO: Permissions.
        next_step_key = ndb.Key(urlsafe=request.key)
        next_step_key.delete()
        return Echo(message='Success')


    #############################################
    # Add and remove viewers.
    #############################################

    @remote.method(common_messages.ViewerRequest, Echo)
    def add_viewer(self, request):

        ''' Add a viewer to a project. '''

        # TODO: Permissions.
        if not request.target:
            raise remote.ApplicationError('No project provided.')
        if not request.user:
            raise remote.ApplicationError('No user provided.')

        project = ndb.Key(urlsafe=self.decrypt(request.target)).get()
        if not project:
            raise remote.ApplicationError('Project not found.')

        user = ndb.Key(urlsafe=self.decrypt(request.user)).get()
        if not project:
            raise remote.ApplicationError('User not found.')

        if user.key in project.viewers:
            raise remote.ApplicationError('User is already a viewer.')

        project.viewers.append(user.key)
        project.put()
        return Echo(message='User added')

    @remote.method(common_messages.ViewerRequest, Echo)
    def remove_viewer(self, request):

        ''' Remove a viewer from a project. '''

        # TODO: Permissions.
        if not request.target:
            raise remote.ApplicationError('No project provided.')
        if not request.user:
            raise remote.ApplicationError('No user provided.')

        project = ndb.Key(urlsafe=self.decrypt(request.target)).get()
        if not project:
            raise remote.ApplicationError('Project not found.')

        user = ndb.Key(urlsafe=self.decrypt(request.user)).get()
        if not project:
            raise remote.ApplicationError('User not found.')

        if not user.key in project.viewers:
            raise remote.ApplicationError('User is not a viewer.')

        project.viewers.remove(user.key)
        project.put()
        return Echo(message='User removed')
