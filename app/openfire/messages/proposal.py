from protorpc import messages
from openfire.messages.common import Goal, Tier


class Proposal(messages.Message):

    ''' Contains all proposal fields for users. Can be request or response. '''

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


class Proposals(messages.Message):

    ''' A list of proposals. '''

    proposals = messages.MessageField(Proposal, 1, repeated=True)


class ProposalRequest(messages.Message):

    ''' Request proposal info, or, if proposal is populated, edit profile. '''

    slug = messages.StringField(1)


class Promote(messages.Message):

    ''' Request proposal info, or, if proposal is populated, edit profile. '''

    proposal_id = messages.StringField(1)


class RejectProposal(messages.Message):

    ''' Reject a proposal. '''

    proposal_id = messages.StringField(1)
    reason = messages.StringField(2)


class SuspendProposal(messages.Message):

    ''' Suspend a proposal. '''

    proposal_id = messages.StringField(1)
    reason = messages.StringField(2)
