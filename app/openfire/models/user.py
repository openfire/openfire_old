# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel
from google.appengine.ext.ndb import polymodel

# Model Attachments
from openfire.messages import user as messages
from openfire.pipelines.model import user as pipelines


######## ======== Top-Level User Models ======== ########

## User - top-level entity for user accounts
class User(AppModel):

    ''' An openfire user. '''

    _message_class = messages.User
    _pipeline_class = pipelines.UserPipeline

    user = ndb.UserProperty('usr', indexed=True)
    username = ndb.StringProperty('u', indexed=True)
    firstname = ndb.StringProperty('f', indexed=True)
    lastname = ndb.StringProperty('l', indexed=True)
    bio = ndb.TextProperty('b', indexed=False)
    location = ndb.StringProperty('loc', indexed=True)
    customurl = ndb.KeyProperty('url', indexed=True, default=None)
    permissions = ndb.KeyProperty('prms', indexed=True, repeated=True)
    email = ndb.KeyProperty('em', indexed=True, repeated=True)
    avatar = ndb.KeyProperty('av', repeated=True)

    def get_custom_url(self):
        if self.customurl:
            return self.customurl.id()
        return None


## EmailAddress - links an email address to a user, for the purpose of signin/notifications/contact
class EmailAddress(AppModel):

    ''' An openfire user's email address. '''

    _message_class = messages.EmailAddress
    _pipeline_class = pipelines.EmailAddressPipeline

    user = ndb.KeyProperty('u', indexed=True)
    address = ndb.StringProperty('e', indexed=True)
    label = ndb.StringProperty('l', indexed=False, choices=['d', 'w', 'p', 'o'], default='p')  # work, personal & other
    notify = ndb.BooleanProperty('n', indexed=True, default=False)  # use this email to notify?
    jabber = ndb.BooleanProperty('j', indexed=True, default=False)  # use this email for jabber?
    gravatar = ndb.BooleanProperty('g', indexed=True, default=False)  # use this email for gravatar?


## Permissions - a set of binary permissions that can be bestowed/revoked on a user
class Permissions(AppModel):

    ''' Describes permissions bestowed on an openfire user. '''

    _message_class = messages.Permissions
    _pipeline_class = pipelines.PermissionsPipeline

    user = ndb.KeyProperty('u', indexed=True)
    moderator = ndb.BooleanProperty('m', indexed=True, default=False)
    admin = ndb.BooleanProperty('a', indexed=True, default=False)
    developer = ndb.BooleanProperty('d', indexed=True, default=False)


######## ======== 3rd Party Account Models ======== ########

## SocialAccount - a linked 3rd party account on an external platform
class SocialAccount(polymodel.PolyModel):

    ''' Describes an account from a 3rd party platform that an openfire user has attached. '''

    _message_class = messages.SocialAccount
    _pipeline_class = pipelines.SocialAccountPipeline

    user = ndb.KeyProperty('u', indexed=True)
    ext_id = ndb.StringProperty('e', indexed=True)
    login = ndb.BooleanProperty('a', indexed=True, default=True)
    public = ndb.BooleanProperty('p', indexed=True, default=True)
    token = ndb.StringProperty('t', indexed=False)
    link = ndb.StringProperty('l', indexed=False)


## GoogleAccount - account federation from Google via OAuth/OpenID
class GoogleAccount(SocialAccount):

    ''' Describes a Google account that is attached to an openfire user. '''

    pass


## FacebookAccount - account federation from Facebook via OAuth
class FacebookAccount(SocialAccount):

    ''' Describes a Facebook account that is attached to an openfire user. '''

    pass


## TwitterAccount - account federation from Twitter via OAuth
class TwitterAccount(SocialAccount):

    ''' Describes a Twitter account that is attached to an openfire user. '''

    pass


## OpenIDAccount - account federation from anyone via OpenID
class OpenIDAccount(SocialAccount):

    ''' Describes an OpenID account that is attached to an openfire user. '''

    pass
