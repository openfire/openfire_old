from openfire.models import AppModel
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Role(ndb.Model):

    ''' Represents a role that a user can play on a project. '''

    slug = ndb.StringProperty('s', indexed=True, required=True)
    name = ndb.StringProperty('n', indexed=True, required=True)
    description = ndb.TextProperty('t', indexed=False, required=True)


class RoleMapping(polymodel.PolyModel):

    ''' Maps a user to a role and a project/proposal. '''

    user = ndb.KeyProperty('u', indexed=True, required=True)
    role = ndb.KeyProperty('r', indexed=True, required=True)
