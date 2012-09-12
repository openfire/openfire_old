from protorpc import messages
from openfire.messages.common import Goal, Tier, FutureGoal, NextStep


class Proposal(messages.Message):

    ''' Contains all proposal fields for users. Can be request or response. '''

    key = messages.StringField(1)
    name = messages.StringField(2)
    status = messages.StringField(3)
    category = messages.StringField(4)
    summary = messages.StringField(5)
    pitch = messages.StringField(6)
    tech = messages.StringField(7)
    keywords = messages.StringField(8, repeated=True)
    creator = messages.StringField(9)
    owners = messages.StringField(10, repeated=True)
    initial_goal = messages.MessageField(Goal, 11)
    initial_tiers = messages.MessageField(Tier, 12, repeated=True)
    initial_next_steps = messages.MessageField(NextStep, 13, repeated=True)
    future_goal = messages.MessageField(FutureGoal, 14)


class Proposals(messages.Message):

    ''' A list of proposals. '''

    proposals = messages.MessageField(Proposal, 1, repeated=True)


class ProposalRequest(messages.Message):

    ''' Request proposal info by key. '''

    key = messages.StringField(1)
    comment = messages.StringField(2)
