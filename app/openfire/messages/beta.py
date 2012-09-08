# -*- coding: utf-8 -*-
from protorpc import messages


class BetaSignup(messages.Message):

    ''' Represents a user signup request call, made from the placeholder page. '''

    name = messages.StringField(1, required=True)
    email = messages.StringField(2, required=True)
    token = messages.StringField(3, required=True)
    message = messages.StringField(4, required=False)


class BetaSignupResponse(messages.Message):

    ''' Response to a BetaSignup request, containing the signup key and token. '''

    key = messages.StringField(1, required=True)
    token = messages.StringField(2, required=True)
