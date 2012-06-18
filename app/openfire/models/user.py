from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

from openfire.models.assets import Avatar


######## ======== Top-Level User Models ======== ########

## User Account
class User(ndb.Model):

    ''' An openfire user. '''

    username = ndb.StringProperty('u', indexed=True)
    firstname = ndb.StringProperty('f', indexed=True)
    lastname = ndb.StringProperty('l', indexed=True)
    bio = ndb.TextProperty('b', indexed=False)


## User Avatar
class UserAvatar(Avatar):

    ''' Maps an avatar to a user. '''

    user = ndb.KeyProperty('u', indexed=True, required=True)


## User Email
class EmailAddress(ndb.Model):

    ''' An openfire user's email address. '''

    user = ndb.KeyProperty('u', indexed=True)
    address = ndb.StringProperty('e', indexed=True)
    label = ndb.StringProperty('l', indexed=False, choices=['w', 'p', 'o'], default='p')  # work, personal & other
    notify = ndb.BooleanProperty('n', indexed=True, default=False)
    jabber = ndb.BooleanProperty('j', indexed=True, default=False)


## User Profile Content
class ProfileContent(ndb.Model):

    ''' Content from the profile of an openfire user. '''

    user = ndb.KeyProperty('u', indexed=True)
    snippet_id = ndb.StringProperty('s', indexed=True)
    content = ndb.TextProperty('c', indexed=False)


## User Permissions
class Permissions(ndb.Model):

    ''' Describes permissions bestowed on an openfire user. '''

    user = ndb.KeyProperty('u', indexed=True)
    moderator = ndb.BooleanProperty('m', indexed=True, default=False)
    admin = ndb.BooleanProperty('a', indexed=True, default=False)
    developer = ndb.BooleanProperty('d', indexed=True, default=False)


######## ======== 3rd Party Account Models ======== ########

## External Acocunt
class SocialAccount(polymodel.PolyModel):

    ''' Describes an account from a 3rd party platform that an openfire user has attached. '''

    user = ndb.KeyProperty('u', indexed=True)
    ext_id = ndb.StringProperty('e', indexed=True)
    login = ndb.BooleanProperty('a', indexed=True, default=True)
    public = ndb.BooleanProperty('p', indexed=True, default=True)
    token = ndb.StringProperty('t', indexed=False)
    link = ndb.StringProperty('l', indexed=False)


## Google via OAuth/OpenID
class GoogleAccount(SocialAccount):

    ''' Describes a Google account that is attached to an openfire user. '''

    pass


## Facebook via OAuth
class FacebookAccount(SocialAccount):

    ''' Describes a Facebook account that is attached to an openfire user. '''

    pass


## Twitter via OAuth
class TwitterAccount(SocialAccount):

    ''' Describes a Twitter account that is attached to an openfire user. '''

    pass


## Anyone via OpenID
class OpenIDAccount(SocialAccount):

    ''' Describes an OpenID account that is attached to an openfire user. '''

    pass
