from openfire.models import AppModel
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Asset(AppModel):

    ''' Describes a stored asset, like CSS or JS or an image. '''

    url = ndb.StringProperty('u', indexed=True, default=None)
    cdn = ndb.StringProperty('c', indexed=True, default=None)
    kind = ndb.StringProperty('t', indexed=True, choices=['i', 's', 't', 'v'], default='i')  # image, style, script, video
    blob = ndb.BlobKeyProperty('b', indexed=True)
    versions = ndb.KeyProperty('v', indexed=True)


class Media(polymodel.PolyModel):

    ''' Describes an attachment between a Asset and a site object. '''

    url = ndb.StringProperty('r', indexed=False, required=False)
    asset = ndb.KeyProperty('a', indexed=True, required=True)
    caption = ndb.StringProperty('c', indexed=True, required=False)
    description = ndb.TextProperty('d', indexed=False, required=False)


class Avatar(Media):

    ''' Describes a user avatar. '''

    version = ndb.IntegerProperty('v', indexed=True, default=1)
    active = ndb.BooleanProperty('e', indexed=True, default=False)
    content = ndb.BlobProperty('bc', indexed=False)


class Video(Media):

    ''' Describes a web video. '''

    provider = ndb.StringProperty('p', indexed=True, choices=['youtube', 'vimeo'])


class CustomURL(AppModel):

    ''' Describes a custom URL mapping. '''

    slug = ndb.StringProperty('s', indexed=True, required=True)
    target = ndb.KeyProperty('t', indexed=True, required=True)
