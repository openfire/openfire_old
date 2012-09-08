from google.appengine.ext import ndb
from apptools.services.builtin import Echo
from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.messages import proposal as proposal_messages
from openfire.messages import common as common_messages
from openfire.models.project import Proposal, Project
from openfire.models.payment import WePayUserPaymentAccount
from openfire.core.payment import PaymentAPI

class ProposalService(RemoteService):

    ''' Proposal service api. '''

    @remote.method(message_types.VoidMessage, proposal_messages.Proposals)
    def list(self, request):

        ''' Returns a list of proposals. '''

        messages = [proposal.to_message() for proposal in Proposal.query().fetch()]
        return proposal_messages.Proposals(proposals=messages)


    @remote.method(proposal_messages.ProposalRequest, proposal_messages.Proposal)
    def get(self, request):

        ''' Return a proposal. '''

        proposal_key = ndb.Key(urlsafe=self.decrypt(request.key))
        proposal = proposal_key.get()
        return proposal.to_message()


    @remote.method(proposal_messages.Proposal, proposal_messages.Proposal)
    def put(self, request):

        ''' Create a new or or edit an existing proposal. '''

        if not request.key:

            # Create a new proposal. Must be logged in.
            if not self.session or not self.session.get('ukey', False):
                # Not logged in.
                return proposal_messages.Proposal()

            # Set the creator and owner to the logged in user.
            ukey = ndb.Key(urlsafe=self.session['ukey'])
            proposal = Proposal()
            proposal.creator = ukey
            proposal.owners = [ukey]

        else:
            # Get the proposal to edit.
            proposal_key = ndb.Key(urlsafe=self.decrypt(request.key))
            proposal = proposal_key.get()

        if not proposal:
            return proposal_messages.Proposal()

        # Update the proposal.
        proposal.mutate_from_message(request)
        proposal.put()

        return proposal.to_message()


    @remote.method(proposal_messages.ProposalRequest, Echo)
    def delete(self, request):

        ''' Remove a category. '''

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


    @remote.method(proposal_messages.Promote, Echo)
    def promote(self, request):

        '''
        Promote a proposal to become a project.

        TODO: Eventually this will kick off a pipeline to create a new project
        and copy over the relevent info. For now, just create and link the project.
        '''

        proposal_key = ndb.Key(urlsafe=self.decrypt(request.key))
        proposal = proposal_key.get()

        new_project = Project(
                name=proposal.name,
                status='p',
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

        # If any of the owners has a payment account linked, create a collection account for this project.
        for owner_key in proposal.owners:
            accounts = WePayUserPaymentAccount.query(WePayUserPaymentAccount.user == owner_key).fetch()
            if accounts and len(accounts):
                # Create a collection account for this project owner only.
                account_response = PaymentAPI.create_project_payment_account(
                        new_project.key, new_project.name,
                        'Collection account for ' + new_project.name, accounts[0])
                if not account_response.success:
                    pass # TODO: Log an error here or do something!
                break

        # Accept the proposal
        proposal.status = 'a'
        proposal.put()

        return Echo(message='')


    @remote.method(proposal_messages.SuspendProposal, Echo)
    def suspend(self, request):

        ''' Suspend a proposal. '''

        proposal_key = ndb.Key(urlsafe=self.decrypt(request.key))
        proposal = proposal_key.get()

        if not proposal:
            # Proposal not found.
            raise remote.ApplicationError('Proposal not found')

        proposal.status = 'f'
        proposal.put()

        return Echo(message='Proposal suspended')


    @remote.method(proposal_messages.RejectProposal, Echo)
    def reject(self, request):

        ''' Reject a proposal. '''

        proposal_key = ndb.Key(urlsafe=self.decrypt(request.key))
        proposal = proposal_key.get()

        if not proposal:
            # Proposal not found.
            raise remote.ApplicationError('Proposal not found')

        proposal.status = 'd'
        proposal.put()

        return Echo(message='Proposal rejected')
