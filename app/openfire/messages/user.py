from protorpc import messages


class User(messages.Message):

    ''' Low-level representation of a user account. '''

    pass


class EmailAddress(messages.Message):

    ''' Represents a user's email address. '''

    pass


class Profile(messages.Message):

    '''
    Contains all profile fields for users.

    Can be request or response, but username, email, firstname,
    and lastname cannot be set from this message.
    '''

    username = messages.StringField(1)
    email = messages.StringField(2)
    firstname = messages.StringField(3)
    lastname = messages.StringField(4)
    bio = messages.StringField(5)
    location = messages.StringField(6)
    topics = messages.StringField(7, repeated=True)


class ProfileRequest(messages.Message):

    ''' Request profile info or edit if profile is populated. '''

    user = messages.StringField(1)
    profile = messages.MessageField(Profile, 2)


class Account(messages.Message):

    ''' Contains all account info for users. Can be request or response. '''

    username = messages.StringField(1)
    email = messages.StringField(2)


class AccountRequest(messages.Message):

    ''' Request account info or edit if account is populated. '''

    user = messages.StringField(1)
    account = messages.MessageField(Account, 2)


class Permissions(messages.Message):

    ''' Represents a set of permissions attached to a user. '''

    pass


class SocialAccount(messages.Message):

    ''' Represents a social account attached to an openfire account. '''

    pass
