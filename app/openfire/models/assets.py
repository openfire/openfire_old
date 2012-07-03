# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel
from google.appengine.ext.ndb import polymodel

# Model Attachments
from openfire.messages import assets as messages
from openfire.pipelines.model import assets as pipelines


######## ======== Assets + Media Top-Level Models ======== ########

## Asset - low-level entity that links a blob to a media item (only required when stored via blobstore or cloud storage)
class Asset(AppModel):

    ''' Describes a stored asset, like CSS or JS or an image. '''

    _message_class = messages.Asset
    _pipeline_class = pipelines.AssetPipeline

    url = ndb.StringProperty('u', indexed=True, default=None)
    cdn = ndb.StringProperty('c', indexed=True, default=None)
    kind = ndb.StringProperty('t', indexed=True, choices=['i', 's', 't', 'v'], default='i')  # image, style, script, video
    blob = ndb.BlobKeyProperty('b', indexed=True)
    versions = ndb.KeyProperty('v', indexed=True, repeated=True)


## Media - links another object to a static asset, either via an Asset reference or a URL
class Media(polymodel.PolyModel):

    ''' Describes an attachment between a Asset and a site object. '''

    _message_class = messages.Media
    _pipeline_class = pipelines.MediaPipeline

    url = ndb.StringProperty('r', indexed=False, required=False)
    asset = ndb.KeyProperty('a', indexed=True, required=True)
    caption = ndb.StringProperty('c', indexed=True, required=False)
    description = ndb.TextProperty('d', indexed=False, required=False)


######## ======== Media Submodels ======== ########

## Avatar - an image representing a data item, uploaded by the user that manages that data item
class Avatar(Media):

    ''' Describes a user avatar. '''

    _message_class = messages.Avatar
    _pipeline_class = pipelines.AvatarPipeline

    version = ndb.IntegerProperty('v', indexed=True, default=1)
    active = ndb.BooleanProperty('e', indexed=True, default=False)
    content = ndb.BlobProperty('bc', indexed=False)


## Video - a piece of content that is a video or movie (always external, never has an Asset attachment)
class Video(Media):

    ''' Describes a web video. '''

    _message_class = messages.Video
    _pipeline_class = pipelines.VideoPipeline

    provider = ndb.StringProperty('p', indexed=True, choices=['youtube', 'vimeo'])


######## ======== Custom URLs ======== ########

## CustomURL - mapping for a custom URL slug to a project or profile
class CustomURL(AppModel):

    ''' Describes a custom URL mapping. '''

    _message_class = messages.CustomURL
    _pipeline_class = pipelines.CustomURLPipeline

    slug = ndb.StringProperty('s', indexed=True, required=True)
    target = ndb.KeyProperty('t', indexed=True, required=True)
