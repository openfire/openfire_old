from protorpc import messages


## Update - small, Twitter-style content posted under a project or a user profile
class Update(messages.Message):

    ''' An update posted under a profile or project. '''

    ## Poster - represents the user who authored the post
    class Poster(messages.Message):

        ''' User that authored the post. '''

        username = messages.StringField(1)
        profile = messages.StringField(2)
        firstname = messages.StringField(3)
        lastname = messages.StringField(4)
        avatar = messages.StringField(5)

    ## PrivacyOptions - a set of modes to assume for protecting the post
    class PrivacyOptions(messages.Enum):

        ''' Privacy options for an update. '''

        PRIVATE = 0
        LIMITED = 1
        PUBLIC = 2

    ## Attachment - media attached to the update, like a photo or a video
    class Attachment(messages.Message):

        ''' Media attached to an update. '''

        ## MediaType - options for types of media that can be attached
        class MediaTypes(messages.Enum):

            ''' Media type options. '''

            LINK = 0
            TEXT = 1
            IMAGE = 2
            VIDEO = 3

        ## MediaProviders - options for external providers that we recognize
        class MediaProviders(messages.Enum):

            ''' Media provider options. '''

            WEB = 0
            FACEBOOK = 1
            TWITTER = 2
            YOUTUBE = 3
            VIMEO = 4

        media = messages.EnumField(MediaTypes, 1)
        provider = messages.EnumField(MediaProviders, 2)
        href = messages.StringField(3)
        mime = messages.STringField(4)

    key = messages.StringField(1)
    subject = messages.StringField(2)
    content = messages.StringField(3)
    privacy = messages.EnumField(PrivacyOptions, 4, default=PrivacyOptions.PRIVATE)
    attachment = messages.MessageField(Attachment, 5)
    author = messages.MessageField(Poster)
    modified = messages.StringField(6)
    modified_ago = messages.StringField(7)
    created = messages.StringField(8)
    created_ago = messages.StringField(9)


## Updates - request/response for a list of updates, given a project or user
class Updates(messages.Message):

    ''' Retrieve updates. '''

    updates = messages.MessageField(Post, 1, repeated=True)
    count = messages.IntegerField(2)
    subject = messages.StringField(3)
