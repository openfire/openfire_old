from protorpc import messages
from openfire.messages.common import Goal, Tier, FutureGoal, NextStep


class Proposal(messages.Message):

    ''' Contains all proposal fields for users. Can be request or response. '''

    key = messages.StringField(1)
    name = messages.StringField(2)
    status = messages.StringField(3)
    category = messages.StringField(4)
    desired_url = messages.StringField(5)
    summary = messages.StringField(6)
    pitch = messages.StringField(7)
    tech = messages.StringField(8)
    team = messages.StringField(9)
    keywords = messages.StringField(10, repeated=True)
    creator = messages.StringField(11)
    owners = messages.StringField(12, repeated=True)
    initial_goal = messages.MessageField(Goal, 13)
    initial_tiers = messages.MessageField(Tier, 14, repeated=True)
    initial_next_steps = messages.MessageField(NextStep, 15, repeated=True)
    future_goal = messages.MessageField(FutureGoal, 16)


class Proposals(messages.Message):

    ''' A list of proposals. '''

    proposals = messages.MessageField(Proposal, 1, repeated=True)


class ProposalRequest(messages.Message):

    ''' Request proposal info by key. '''

    key = messages.StringField(1)
    comment = messages.StringField(2)
