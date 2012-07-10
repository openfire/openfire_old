from protorpc import messages

class Media(messages.Message):

    ''' Get media. '''

    media = messages.StringField(1)


class GenerateEndpoint(messages.Message):

    ''' Generate an endpoint to attach an optional target to. '''

    target = messages.StringField(1)
    session_id = messages.StringField(2)
    file_count = messages.IntegerField(3)
    backend = messages.StringField(4)


class Endpoint(messages.Message):

    ''' . '''

    endpoints = messages.StringField(1, repeated=True)


class AttachImage(messages.Message):

    ''' . '''

    media = messages.StringField(1)


class AttachImageEndpoint(messages.Message):

    ''' . '''

    media = messages.StringField(1)


class AttachVideo(messages.Message):

    ''' . '''

    media = messages.StringField(1)


class AttachAvatar(messages.Message):

    ''' . '''

    media = messages.StringField(1)


class AttachAvatarEndpoint(messages.Message):

    ''' . '''

    media = messages.StringField(1)
