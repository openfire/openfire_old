from google.appengine.ext import ndb
from apptools.services.builtin import Echo
from protorpc import messages, message_types, remote
from openfire.services import RemoteService
from openfire.messages import proposal as proposal_messages
from openfire.messages import project as project_messages
from openfire.messages import common as common_messages
from openfire.models.project import Proposal, Project, Goal, FutureGoal, Tier, NextStep
from openfire.models.payment import WePayUserPaymentAccount
from openfire.core.payment import PaymentAPI

class ProposalService(RemoteService):

    ''' Proposal service api. '''

    @remote.method(message_types.VoidMessage, proposal_messages.Proposals)
    def list(self, request):

        ''' Returns a list of proposals. '''

        # TODO: Permissions.
        msgs = [proposal.to_message() for proposal in Proposal.query().fetch()]
        return proposal_messages.Proposals(proposals=msgs)

    @remote.method(message_types.VoidMessage, proposal_messages.Proposals)
    def submitted(self, request):

        ''' Returns a list of pending submitted proposals that need BBQ action. '''

        # TODO: Permissions.
        msgs = [proposal.to_message() for proposal in Proposal.query(Proposal.status == 's').fetch()]
        return proposal_messages.Proposals(proposals=msgs)

    @remote.method(proposal_messages.ProposalRequest, proposal_messages.Proposal)
    def get(self, request):

        ''' Return a proposal. '''

        # TODO: Permissions.
        proposal_key = ndb.Key(urlsafe=self.decrypt(request.key))
        proposal = proposal_key.get()
        return proposal.to_message()

    @remote.method(proposal_messages.Proposal, proposal_messages.Proposal)
    def put(self, request):

        ''' Create a new or or edit an existing proposal. '''

        # TODO: Permissions.
        # If there is a key, use the existing proposal. Otherwise, create a new proposal.
        proposal = None
        if request.key:
            proposal = ndb.Key(urlsafe=self.decrypt(request.key)).get()
            if not proposal:
                raise remote.ApplicationError('Bad proposal key provided.')
        else:

            # For now we will allow setting the creator and owner during creation, so that we can
            # write tests for this code. this might be removed in the future. [OF-155]
            creator_key = None
            owner_keys = []
            if request.creator:
                creator_key = ndb.Key(urlsafe=request.creator)
            if request.owners:
                for owner_key in request.owners:
                    owner_keys.append(ndb.Key(urlsafe=owner_key))
            if not creator_key in owner_keys:
                owner_keys.append(creator_key)

            if not creator_key:
                if not (hasattr(self, 'user') and self.user and hasattr(self.user, 'key') and self.user.key):
                    raise remote.ApplicationError('Must be logged in.')
                creator_key = self.user.key
                owner_keys = [self.user.key]

            # Create the new proposal and add a creator and owners
            proposal = Proposal()
            proposal.creator = creator_key
            proposal.owners = owner_keys

        # Update the proposal.
        proposal.mutate_from_message(request, exclude=['key', 'status', 'creator', 'owners'])

        # Set the goals, tiers, and next steps since mutate_from_message does not handle those.
        if isinstance(request.initial_goal, messages.Message):
            goal = Goal().mutate_from_message(request.initial_goal)
            if goal:
                proposal.initial_goal = goal

        # Future Goal
        if isinstance(request.future_goal, messages.Message):
            future_goal = FutureGoal().mutate_from_message(request.future_goal)
            if future_goal:
                proposal.future_goal = future_goal

        # Initial Tiers
        if request.initial_tiers and isinstance(request.initial_tiers[0], messages.Message):
            tiers = []
            for tier_message in request.initial_tiers:
                tier = Tier().mutate_from_message(tier_message)
                if tier:
                    tiers.append(tier)
            proposal.initial_tiers = tiers

        # Initial Next Steps
        if request.initial_next_steps and isinstance(request.initial_next_steps[0], messages.Message):
            next_steps = []
            for next_step_message in request.initial_next_steps:
                next_step = NextStep().mutate_from_message(next_step_message)
                if next_step:
                    next_steps.append(next_step)
            proposal.initial_next_steps = next_steps

        proposal.put()

        return proposal.to_message()

    @remote.method(proposal_messages.ProposalRequest, Echo)
    def delete(self, request):

        ''' Remove a category. '''

        # TODO: Permissions.
        proposal_key = ndb.Key(urlsafe=self.decrypt(request.key))
        proposal_key.delete()
        return Echo(message='Proposal removed')

    @remote.method(common_messages.Comment, Echo)
    def comment(self, request):

        ''' Comment/iterate on a proposal. '''

        return Echo(message='You have commented on a proposal.')

    @remote.method(message_types.VoidMessage, common_messages.Comments)
    def comments(self, request):

        ''' Comments for a proposal. '''

        return common_messages.Comments()

    @remote.method(proposal_messages.ProposalRequest, project_messages.Project)
    def promote(self, request):

        '''
        Promote a proposal to become a project.

        TODO: Eventually this will kick off a pipeline to create a new project
        and copy over the relevent info. For now, just create and link the project.
        '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('No proposal provided.')

        proposal = ndb.Key(urlsafe=self.decrypt(request.key)).get()
        if proposal.status == 'a':
            raise remote.ApplicationError('Proposal has already been accepted.')

        new_project = Project(
            name=proposal.name,
            proposal=proposal.key,
            category=proposal.category,
            summary=proposal.summary,
            pitch=proposal.pitch,
            tech=proposal.tech,
            keywords=proposal.keywords,
            creator=proposal.creator,
            owners=proposal.owners,
        )
        new_project.put()

        # Might need to save the project again after updating active and future goals.
        project_needs_put = False

        # Set up the initial goal with tiers and next steps if there was a proposed goal.
        initial_goal = None
        if proposal.initial_goal:
            initial_goal = proposal.initial_goal
            initial_goal.parent = new_project.key
            initial_goal.put()

            tier_keys = []
            for initial_tier in proposal.initial_tiers:
                tier = initial_tier
                tier.parent = initial_goal.key
                tier.put()
                tier_keys.append(tier.key)
            initial_goal.tiers = tier_keys

            next_step_keys = []
            for initial_next_step in proposal.initial_next_steps:
                next_step = initial_next_step
                next_step.parent = initial_goal.key
                next_step.put()
                next_step_keys.append(next_step.key)
            initial_goal.next_steps = next_step_keys

            initial_goal.put()
            new_project.active_goal = initial_goal.key
            project_needs_put = True

        # Set up the future goal if there is one.
        future_goal = None
        if proposal.future_goal:
            future_goal = proposal.future_goal
            future_goal.parent = new_project.key
            future_goal.put()
            new_project.future_goal = future_goal.key
            project_needs_put = True

        # Save the project again if anything just changed.
        if project_needs_put:
            new_project.put()

        account_response = PaymentAPI.set_up_project_payment_account(new_project)
        if not account_response.success:
            # TODO: Show a message somewhere saying that a payment account was not created for this project.
            pass

        # Set the proposal to accepted.
        proposal.status = 'a'
        proposal.put()

        return new_project.to_message()

    @remote.method(proposal_messages.ProposalRequest, Echo)
    def suspend(self, request):

        ''' Suspend a proposal. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('No proposal provided.')

        proposal = ndb.Key(urlsafe=self.decrypt(request.key)).get()
        if not proposal:
            raise remote.ApplicationError('Proposal not found.')

        proposal.status = 'p'
        proposal.put()

        return Echo(message='Proposal suspended')

    @remote.method(proposal_messages.ProposalRequest, Echo)
    def reject(self, request):

        ''' Reject a proposal. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('No proposal provided.')

        proposal = ndb.Key(urlsafe=self.decrypt(request.key)).get()
        if not proposal:
            raise remote.ApplicationError('Proposal not found.')

        proposal.status = 'd'
        proposal.put()

        return Echo(message='Proposal rejected')

    @remote.method(proposal_messages.ProposalRequest, proposal_messages.Proposal)
    def reopen(self, request):

        ''' Reject a proposal. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('No proposal provided.')

        proposal = ndb.Key(urlsafe=self.decrypt(request.key)).get()
        if not proposal:
            raise remote.ApplicationError('Proposal not found.')

        if proposal.status == 'f':
            raise remote.ApplicationError('Proposal already open and draft.')
        elif proposal.status == 'a':
            raise remote.ApplicationError('Proposal already accepted.')

        proposal.status = 'f'
        proposal.put()

        return proposal.to_message()


    #############################################
    # Add and remove viewers.
    #############################################

    @remote.method(common_messages.ViewerRequest, Echo)
    def add_viewer(self, request):

        ''' Add a viewer to a proposal. '''

        # TODO: Permissions.
        if not request.target:
            raise remote.ApplicationError('No proposal provided.')
        if not request.user:
            raise remote.ApplicationError('No user provided.')

        proposal = ndb.Key(urlsafe=self.decrypt(request.target)).get()
        if not proposal:
            raise remote.ApplicationError('Proposal not found.')

        user = ndb.Key(urlsafe=self.decrypt(request.user)).get()
        if not proposal:
            raise remote.ApplicationError('User not found.')

        if user.key in proposal.viewers:
            raise remote.ApplicationError('User is already a viewer.')

        proposal.viewers.append(user.key)
        proposal.put()
        return Echo(message='User added')

    @remote.method(common_messages.ViewerRequest, Echo)
    def remove_viewer(self, request):

        ''' Remove a viewer from a proposal. '''

        # TODO: Permissions.
        if not request.target:
            raise remote.ApplicationError('No proposal provided.')
        if not request.user:
            raise remote.ApplicationError('No user provided.')

        proposal = ndb.Key(urlsafe=self.decrypt(request.target)).get()
        if not proposal:
            raise remote.ApplicationError('Proposal not found.')

        user = ndb.Key(urlsafe=self.decrypt(request.user)).get()
        if not proposal:
            raise remote.ApplicationError('User not found.')

        if not user.key in proposal.viewers:
            raise remote.ApplicationError('User is not a viewer.')

        proposal.viewers.remove(user.key)
        proposal.put()
        return Echo(message='User removed')
