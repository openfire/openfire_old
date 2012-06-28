from openfire.models import AppModel
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Comment(polymodel.PolyModel):

    ''' Represents a comment made by a user on some site object. '''

    user = ndb.KeyProperty('u', indexed=True, required=True)
    content = ndb.StringProperty('c', indexed=True, required=True)
    reply_to = ndb.KeyProperty('r', indexed=True, default=None)


class Follow(polymodel.PolyModel):

    ''' Describes a user's desire to follow some site object. '''

    user = ndb.KeyProperty('u', indexed=True, required=True)
