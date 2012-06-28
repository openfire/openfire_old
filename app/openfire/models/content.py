from openfire.models import AppModel
from google.appengine.ext import ndb


# Basic snippet features.
class ContentSnippet(ndb.Model):

    ''' Represents a content fragment that can be edited. '''

    content = ndb.TextProperty()
