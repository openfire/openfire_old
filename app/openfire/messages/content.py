from protorpc import messages


#### ++++ Object Messages ++++ ####
class ContentArea(messages.Message):

    ''' Represents an editable, targeted, versioned area of content. '''

    pass


class ContentSnippet(messages.Message):

    ''' Represents a blob of content data, that can be used as an Area or as a versioned content container under an Area. '''

    pass


class ContentSummary(messages.Message):

    ''' Represents a shortened, plaintext summary of content in an HTML/versioned ContentSnippet. '''

    pass


#### ++++ Request/Response Messages ++++ ####
class GetContentRequest(messages.Message):

    ''' Retrieve a content snippet. '''

    snippet_key = messages.StringField(1)
    snippet_keyname = messages.StringField(2)


class SaveContentRequest(messages.Message):

    ''' Request to save a new version of a content snippet. '''

    snippet_keyname = messages.StringField(1)
    snippet_key = messages.StringField(2)
    inner_html = messages.StringField(3)


class ContentResponse(messages.Message):

    ''' Respond to a request to save a new version of a content snippet. '''

    snippet_key = messages.StringField(1)
    snippet_keyname = messages.StringField(2)
    inner_html = messages.StringField(3)
