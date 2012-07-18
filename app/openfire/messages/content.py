from protorpc import messages
from openfire.messages.user import Profile


#### ++++ Object Messages ++++ ####

## ContentFormat - keeps track of available content formats
class ContentFormat(messages.Enum):

    ''' Specifies available formats under which content can be saved/retrieved. '''

    TEXT = 1  # sentinel for plaintext content
    HTML = 2  # sentinel for richtext content


## ContentSummary - summarizes a contentsnippet entity
class ContentSummary(messages.Message):

    ''' Represents a shortened, plaintext/html summary of content in an HTML/versioned ContentSnippet. '''

    text = messages.StringField(1)  # text summary
    html = messages.StringField(2)  # html summary


## ContentSnippet - full content message, for a revision of a contentarea
class ContentSnippet(messages.Message):

    ''' Represents a blob of content data, that can be used as an Area or as a versioned content container under an Area. '''

    html = messages.StringField(1)
    text = messages.StringField(2)
    summary = messages.MessageField(ContentSummary, 3)


## ContentArea - an area of editable content, either plaintext/richtext
class ContentArea(messages.Message):

    ''' Represents an editable, targeted, versioned area of content. '''

    ## ContentSection - enum representing where this belongs on the site
    class ContentSection(messages.Enum):

        ''' Enumerates sections of OF that a ContentArea can appear in. '''

        SYSTEM = 1   # general content areas around the site
        PROFILE = 2  # content areas on a user's profile page
        PROJECT = 3  # content areas on a project's main page

    ## ContentVersion - container for a versioned contentsnippet
    class ContentVersion(messages.Message):

        ''' Container for a versioned ContentSnippet. '''

        diff = messages.IntegerField(1, default=0)          # quick estimate of how big a change this was from the last, or 0 if it's the first revision
        version = messages.IntegerField(2, default=1)       # integer version of this revision in this set of contentsnippets under this contentarea (not persisted)
        author = messages.MessageField(Profile, 3)          # author of this revision, a full profile message from the `user` messages package
        content = messages.MessageField(ContentSnippet, 4)  # embedded contentsnippet, with html/text properties that hold the actual content, if requested
        committed = messages.StringField(5)                 # string timestamp, parsable in JS, for when this revision was saved
        committed_ago = messages.StringField(6)             # string description, suitable for use in UI widgets, describing when this revision was saved

    keyname = messages.StringField(1, required=True)
    namespace = messages.StringField(2, required=True)
    section = messages.EnumField(ContentSection, 3, default=ContentSection.SYSTEM)
    html = messages.StringField(4, default=None)
    text = messages.StringField(5, default=None)
    versioned = messages.BooleanField(6, default=False)
    versions = messages.MessageField(ContentVersion, 7, repeated=True)


#### ++++ Request/Response Messages ++++ ####

## GetContent - a request to get a contentarea
class GetContent(messages.Message):

    ''' Retrieve a content snippet. '''

    keyname = messages.StringField(1, required=False)
    namespace = messages.StringField(2, required=True)
    content = messages.BooleanField(3, default=True)
    formats = messages.EnumField(ContentFormat, 4, repeated=True)
    versions = messages.BooleanField(5, default=True)


## ContentResponse - contains a single content snippet in response to get/save
class ContentResponse(messages.Message):

    ''' Response to a single request for content. '''

    area = messages.MessageField(ContentArea, 1)
    version = messages.IntegerField(2, default=1)


## GetContentMulti - a request to get multiple contentareas in batch
class GetContentMulti(messages.Message):

    ''' Request to save a new version of a content snippet. '''

    ## RequestedArea - tiny message representing a requested content area
    class RequestedArea(messages.Message):

        ''' A tiny struct representing a requested ContentArea. '''

        keyname = messages.StringField(1, required=False)
        namespace = messages.StringField(2, required=True)

    areas = messages.MessageField(RequestedArea, 1, repeated=True)
    content = messages.BooleanField(2, default=True)
    formats = messages.EnumField(ContentFormat, 3, repeated=True)
    versions = messages.BooleanField(4, default=True)


## SaveContent - request to save a single contentblock
class SaveContent(messages.Message):

    ''' Retrieve a content snippet. '''

    ## ContentBlock - a block of content to be saved, with versioning and formatting information
    class ContentBlock(messages.Message):

        ''' A content block to save. '''

        format = messages.EnumField(ContentFormat, 1, default=ContentFormat.TEXT)
        version = messages.IntegerField(2, default=1)
        minor = messages.BooleanField(3, default=False)
        content = messages.StringField(4, required=True)

    keyname = messages.StringField(1, required=True)
    namespace = messages.StringField(2, required=True)
    versioned = messages.BooleanField(3, default=False)
    content = messages.MessageField(ContentBlock, 4, repeated=True)


## SaveContentMulti - request to save multiple contentblocks in batch
class SaveContentMulti(messages.Message):

    ''' Retrieve a content snippet. '''

    areas = messages.MessageField(SaveContent, 1, repeated=True)


## ContentResponseMulti - contains a single content snippet in response to get/save
class ContentResponseMulti(messages.Message):

    ''' Response to a request for multiple content areas. '''

    areas = messages.MessageField(ContentResponse, 1, repeated=True)
