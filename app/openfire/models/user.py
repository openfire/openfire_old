# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel
from google.appengine.ext.ndb import polymodel

# Model Attachments
from openfire.messages import common
from openfire.messages import user as messages
from openfire.pipelines.model import user as pipelines


######## ======== Top-Level User Models ======== ########

## Topics that users can follow and display interest in.
class Topic(AppModel):

    ''' A topic for users to display interest in and follow. '''

    _message_class = common.Topic
    _pipeline_class = pipelines.TopicPipeline

    # Name and description
    slug = ndb.StringProperty('s', indexed=True, required=True)
    name = ndb.StringProperty('n', indexed=True, required=True)
    description = ndb.StringProperty('d', indexed=False, required=True)

    # Count
    user_count = ndb.IntegerProperty('uc', indexed=True, default=0)


## User - top-level entity for user accounts
class User(AppModel):

    ''' An openfire user. '''

    _message_class = messages.User
    _pipeline_class = pipelines.UserPipeline

    user = ndb.UserProperty('usr', indexed=True)
    username = ndb.StringProperty('u', indexed=True)
    password = ndb.StringProperty('p', indexed=True, default=None)
    firstname = ndb.StringProperty('f', indexed=True)
    lastname = ndb.StringProperty('l', indexed=True)
    activated = ndb.BooleanProperty('xa', default=False, indexed=True)
    public = ndb.BooleanProperty('xp', default=False, indexed=True)
    bio = ndb.StringProperty('b', indexed=True)
    topics = ndb.KeyProperty('ts', indexed=True, repeated=True)
    location = ndb.StringProperty('loc', indexed=True)
    customurl = ndb.KeyProperty('url', indexed=True, default=None)
    permissions = ndb.KeyProperty('prms', indexed=True, repeated=True)
    email = ndb.KeyProperty('em', indexed=True, repeated=True)
    avatar = ndb.KeyProperty('av')
    images = ndb.KeyProperty('im', repeated=True)

    def has_custom_url(self):

        ''' Check and see if a custom URL is attached. '''

        return (self.customurl is not None)

    def get_custom_url(self):

        ''' Return this user's profile custom URL. '''

        if self.customurl:
            return self.customurl.id()
        return None

    def has_avatar(self):

        ''' Check and see if an avatar is attached. '''

        return (self.avatar is not None)

    def get_avatar_url(self, extension='jpg', size='32'):

        ''' Return this user's avatar URL, or false if we don't have it but *do* have an email (yay gravatar) or FBID. '''

        if self.avatar is not None:
            avatar, asset = tuple(ndb.get_multi([self.avatar, ndb.Key(urlsafe=self.avatar.id()).get()]))
            if avatar.url is not None:
                return avatar.url
            elif asset.cdn is not None:
                ## extension is ignored for CDN urls
                return '='.join([asset.cdn, 's' + size])
            elif asset.url is not None:
                return asset.url
            elif asset.blob is not None:
                if extension:
                    return self.url_for('serve-asset-filename', asset_key=str(asset.blob), filename='.'.join(['profile', extension]), s=size)
                else:
                    return self.url_for('serve-asset', asset_key=str(asset.blob))
        return False


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
    link = ndb.StringProperty('l', indexed=False)


## GoogleAccount - account federation from Google via OAuth/OpenID
class GoogleAccount(SocialAccount):

    ''' Describes a Google account that is attached to an openfire user. '''

    identity = ndb.UserProperty('a', indexed=True)


## FacebookAccount - account federation from Facebook via OAuth
class FacebookAccount(SocialAccount):

    ''' Describes a Facebook account that is attached to an openfire user. '''

    identity = ndb.StringProperty('a', indexed=True)  # opengraph account URL
    auth_token = ndb.StringProperty('tt', indexed=False)    # most recent auth token
    access_token = ndb.StringProperty('at', indexed=False)  # most recent access token
    expiration = ndb.DateTimeProperty('e', indexed=True)   # access token expiration


## TwitterAccount - account federation from Twitter via OAuth
class TwitterAccount(SocialAccount):

    ''' Describes a Twitter account that is attached to an openfire user. '''

    pass


## OpenIDAccount - account federation from anyone via OpenID
class OpenIDAccount(SocialAccount):

    ''' Describes an OpenID account that is attached to an openfire user. '''

    pass
