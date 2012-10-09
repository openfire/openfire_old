# -*- coding: utf-8 -*-

# Base
import config
import webapp2

# AppTools
from apptools.util import debug
from apptools.util import datastructures

# ProtoRPC
from protorpc import remote
from protorpc import messages
from protorpc import message_types

# NDB / Builtins
from google.appengine.ext import ndb
from apptools.services.builtin import Echo

# Core APIs
from openfire.core.payment import PaymentAPI

# Service + Messages
from openfire.services import RemoteService
from openfire.messages import common as common_messages
from openfire.messages import project as project_messages
from openfire.messages import proposal as proposal_messages

# Models
from openfire.models import user
from openfire.models import social
from openfire.models.project import Goal
from openfire.models.project import Tier
from openfire.models.project import Project
from openfire.models.project import NextStep
from openfire.models.project import Proposal
from openfire.models.project import FutureGoal
from openfire.models.assets import CustomURL


## Proposal API.
class ProposalService(RemoteService):

    ''' Interact and mutate project proposals. '''

    ## +=+=+ Exceptions +=+=+ ##
    class ProposalServiceException(RemoteService.exceptions.ApplicationError): ''' Base exception for all errors specific to the Proposal Service. '''
    class LoginRequired(ProposalServiceException): ''' Thrown when login is required to perform an action on the Proposal Service. '''
    class NotAuthorized(ProposalServiceException): ''' Thrown when a user isn't authorized to comment on a subject data point. '''

    exceptions = datastructures.DictProxy({

		'LoginRequired': LoginRequired,
        'NotAuthorized': NotAuthorized

	})

    ## +=+=+ Internals +=+=+ ##
    @webapp2.cached_property
    def config(self):

        ''' Named config pipe. '''

        return config.config

    @webapp2.cached_property
    def logging(self):

        ''' Named logging pipe. '''

        return debug.AppToolsLogger(path='openfire.services.proposal', name='ProposalService')._setcondition(self.config.get('debug', False))

    ## +=+=+ Exposed Methods +=+=+ ##
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
        proposal.mutate_from_message(request, exclude=['key', 'status', 'creator', 'owners',
                'initial_goal', 'future_goal', 'initial_tiers', 'initial_next_steps'])

        # Set the goals, tiers, and next steps since mutate_from_message does not handle those.
        if isinstance(request.initial_goal, messages.Message):
            goal = Goal().mutate_from_message(request.initial_goal)
            if goal and goal.amount:
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
                if tier and tier.amount:
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

    @remote.method(common_messages.Comment, common_messages.Comment)
    def comment(self, request):

        ''' Comment on a proposal. '''

        self.logging.info('Received a request to post a comment by user "%s" on subject item "%s".' % (self.__dict__.get('user', None), str(request.subject)))
        if not hasattr(self, 'user') or not getattr(self, 'user'):
            self.logging.warning('User tried to post a comment without being logged in. Returning error.')
            raise self.exceptions.LoginRequired("You must log in to post a comment!")
        else:
            try:
                s = ndb.Key(urlsafe=request.subject)
                sub = s.get()

                if sub is not None:

                    if (self.user.key not in sub.owners) and (self.user.key not in sub.viewers) and not self.permissions.admin:
                        raise self.exceptions.NotAuthorized("Woops! You aren't allowed to comment on that!")

                    c = social.Comment(**{
                        'key': ndb.Key(social.Comment, social.Comment.allocate_ids(1)[0], parent=s),
                        'user': self.user.key,
                        'content': request.text,
                        'subject': s})

                    ckey = c.put(use_cache=True, use_memcache=True, use_datastore=True)
                    self.logging.info('Successfully posted comment at new key "%s".' % str(ckey.urlsafe()))

                    return common_messages.Comment(**{
                        'text': request.text,
                        'timestamp': str(c.created),
                        'timeago': 'some time ago',
                        'subject': s.urlsafe(),
                        'author': common_messages.Comment.Commenter(**{
                            'username': self.user.username,
                            'profile': self.user.get_custom_url(),
                            'firstname': self.user.firstname,
                            'lastname': self.user.lastname,
                            'is_admin': self.permissions.admin,
                            'avatar': self.user.get_avatar_url()
                        })
                    })

                else:
                    self.logging.error('Subject at key "%s" could not be found.' % str(request.subject))
                    raise self.exceptions.SubjectNotFound("Couldn't find the specified subject key.")

            except RemoteService.exceptions.ApplicationError, e:
                raise

            except Exception, e:
                self.logging.error('Encountered an unknown exception posting a comment.')
                raise self.exceptions.ApplicationError('Oops! Something went wrong.')

    @remote.method(common_messages.Comments, common_messages.Comments)
    def comments(self, request):

        ''' Comments for a proposal. '''

        if not hasattr(self, 'user') or not self.user:
            self.logging.warning('User tried to view comments without being logged in. Returning error.')
            raise self.exceptions.LoginRequired("You must log in to view comments!")

        else:
            s = ndb.Key(urlsafe=request.subject)
            sub = s.get()

            if sub is not None:

                if (self.user.key not in sub.owners) and (self.user.key not in sub.viewers) and not self.permissions.admin:
                    raise self.exceptions.NotAuthorized("Woops! You aren't allowed to comment on that!")

                comments_q = social.Comment.query(ancestor=s).order(social.Comment.created)
                count = comments_q.count()
                if count > 0:
                    comments = comments_q.fetch(comments_q.count(), projection=('c', 'u', '_tc'))
                    comment_users = []

                    for comment in comments:
                        if comment.user not in comment_users:
                            comment_users.append(comment.user)

                    users = dict([tuple([key, u]) for key, u in zip(comment_users, ndb.get_multi(comment_users))])
                    permissions = dict([tuple([key, permissions]) for key, permissions in zip(comment_users, ndb.get_multi([ndb.Key(user.Permissions, 'global', parent=k) for k in comment_users]))])

                    return common_messages.Comments(**{

                        'comments': [common_messages.Comment(**{

                            'text': comment.content,
                            'timeago': 'some time ago',
                            'timestamp': str(comment.created),
                            'subject': request.subject,
                            'author': common_messages.Comment.Commenter(**{
                                'username': users.get(comment.user).username,
                                'profile': users.get(comment.user).get_custom_url(),
                                'firstname': users.get(comment.user).firstname,
                                'lastname': users.get(comment.user).lastname,
                                'is_admin': permissions.get(comment.user).admin,
                                'avatar': users.get(comment.user).get_avatar_url()
                            })

                        }) for comment in comments],

                        'count': len(comments),
                        'subject': request.subject

                    })

                else:

                    return common_messages.Comments(**{
                        'comments': [],
                        'count': 0,
                        'subject': request.subject
                    })

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

        # Set up the custom URL if it is available.
        custom_url = None
        if proposal.desired_url:
            url_key = ndb.Key(CustomURL, proposal.desired_url)
            if not url_key.get():
                custom_url = CustomURL(key=url_key, slug=proposal.desired_url, target=new_project.key)
                custom_url.put()
                new_project.customurl = custom_url.key
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
    def submit(self, request):

        ''' Suspend a proposal. '''

        # TODO: Permissions.
        if not request.key:
            raise remote.ApplicationError('No proposal provided.')

        proposal = ndb.Key(urlsafe=self.decrypt(request.key)).get()
        if not proposal:
            raise remote.ApplicationError('Proposal not found.')

        proposal.status = 's'
        proposal.put()

        return Echo(message='Proposal submitted for approval')

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
