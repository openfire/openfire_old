from protorpc import messages


class Login(messages.Message):

    ''' Log in message. '''

    pass


class Session(messages.Message):

    ''' User session message. '''

    sid = messages.StringField(1)
    csrf = messages.StringField(2)


class Request(messages.Message):

    ''' Request message. '''

    username = messages.StringField(1)


class Verify(messages.Message):

    ''' Verify message. '''

    username = messages.StringField(1)


class ThirdParty(messages.Message):

    ''' Third party sign up/in. '''

    third_party = messages.StringField(1)
    username = messages.StringField(2)


class SignUp(messages.Message):

    ''' Sign up. '''

    username = messages.StringField(1)
    email = messages.StringField(2)
    firstname = messages.StringField(3)
    lastname = messages.StringField(4)
    password_hash = messages.StringField(5)
