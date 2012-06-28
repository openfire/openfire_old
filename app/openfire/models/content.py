# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel


######## ======== XMS Content Models ======== ########

# ContentArea - marks an editable dynamic area on a given page for a given data point
class ContentArea(AppModel):

    ''' Represents a content area that can be edited for a certain datapoint. '''

    target = ndb.KeyProperty('t')
    section = ndb.StringProperty('s', choices=['prf', 'prj', 'sys'])  # profile, project or system
    html = ndb.BlobProperty('ht', compressed=False)
    text = ndb.TextProperty('tx', compressed=False)
    versions = ndb.KeyProperty('v', repeated=True)


# ContentSnippet - a content value for a content area (multiple exist for an area only for versioned content sections)
class ContentSnippet(AppModel):

    ''' Represents a versioned content value of a content area. '''

    area = ndb.KeyProperty('a')
    html = ndb.BlobProperty('h', compressed=False)
    text = ndb.TextProperty('t', compressed=True)


## ContentSummary - a shortened summary value for a content area's content
class ContentSummary(AppModel):

    ''' Represents a summary of content in a content area. '''

    target = ndb.KeyProperty('t')
    html = ndb.BlobProperty('ht', compressed=False)
    text = ndb.TextProperty('tx', compressed=False)
