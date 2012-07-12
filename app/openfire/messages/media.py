from protorpc import messages

class Media(messages.Message):

    ''' Get media. '''

    media = messages.StringField(1)


class ImageIntake(messages.Enum):

    ''' A way to upload an image to be served. '''

    UPLOAD = 0
    URL = 1


class ImageBackend(messages.Enum):

    ''' Where to store an image. '''

    BLOB = 0
    CLOUD = 1


class GenerateEndpoint(messages.Message):

    ''' Generate an endpoint to attach an optional target to. '''

    target = messages.StringField(1)
    file_count = messages.IntegerField(2)
    backend = messages.EnumField(ImageBackend, 3, default='BLOB')


class Endpoint(messages.Message):

    ''' . '''

    endpoints = messages.StringField(1, repeated=True)


class AttachAvatar(messages.Message):

    ''' Attach an avatar to a person or project. '''

    target = messages.StringField(1)
    intake = messages.EnumField(ImageIntake, 2, default='UPLOAD')
    backend = messages.EnumField(ImageBackend, 3, default='BLOB')
    name = messages.StringField(4)
    size = messages.IntegerField(5)


class AttachAvatarEndpoint(messages.Message):

    ''' . '''

    endpoint = messages.StringField(1)


class AttachImage(messages.Message):

    ''' Attach an image to a project page or personal profile page. '''

    target = messages.StringField(1)
    intake = messages.EnumField(ImageIntake, 2, default='UPLOAD')
    backend = messages.EnumField(ImageBackend, 3, default='BLOB')
    name = messages.StringField(4)
    size = messages.IntegerField(5)


class AttachImageEndpoint(messages.Message):

    ''' . '''

    endpoint = messages.StringField(1)


class AttachVideo(messages.Message):

    ''' Attach a vide to a project page. '''

    class VideoProvider(messages.Enum):

        ''' Backend providers for our videos. '''

        VIMEO = 0
        YOUTUBE = 1

    target = messages.StringField(1)
    provider = messages.EnumField(VideoProvider, 2)
    reference = messages.StringField(3)
    primary = messages.StringField(4)
