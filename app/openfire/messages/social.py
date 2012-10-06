from protorpc import messages
from openfire.messages.project import Project


class Follower(messages.Message):

    ''' Represents the person who is doing the following. '''

    key = messages.StringField(1)
    username = messages.StringField(2)
    firstname = messages.StringField(3)
    lastname = messages.StringField(4)
    profile = messages.StringField(5)
    avatar = messages.StringField(6)


class Follow(messages.Message):

    ''' Request and response for a user follow. '''

    class NotificationOptions(messages.Message):

        ''' Represents options for the follow record. '''

        class Transport(messages.Enum):

            ''' Represents transport options for a notification. '''

            TEXT = 0
            XMPP = 1
            EMAIL = 2

        class Frequency(messages.Enum):

            ''' Represents notification frequency options. '''

            REALTIME = 0
            DAILY = 1
            WEEKLY = 2

        frequency = messages.EnumField(Frequency, 1, default=Frequency.REALTIME)
        transport = messages.EnumField(Transport, 2, repeated=True)

    class FollowSubject(messages.Message):

        ''' Represents the item being followed. '''

        class SubjectType(messages.Enum):

            ''' Represents possible subject types. '''

            PROJECT = 1
            PROFILE = 2

        key = messages.StringField(1)
        kind = messages.EnumField(SubjectType, 2)
        user = messages.MessageField(Follower, 3)
        project = messages.MessageField(Project, 4)

    subject = messages.MessageField(FollowSubject, 1)
    options = messages.MessageField(NotificationOptions, 2)
    follower = messages.MessageField(Follower, 3)


class Followers(messages.Message):

    ''' Represents a set of users following a user or project. '''

    count = messages.IntegerField(1)
    subject = messages.MessageField(Follow.FollowSubject, 2)
    follows = messages.MessageField(Follow, 3, repeated=True)