# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel


# Model Attachments
from openfire.messages import content as messages
from openfire.pipelines.model import content as pipelines


######## ======== XMS Content Models ======== ########

# ContentArea - marks an editable dynamic area on a given page for a given data point
class ContentArea(AppModel):

    ''' Represents a content area that can be edited for a certain datapoint. '''

    # Storage Settings
    _use_cache = True
    _use_memcache = True
    _use_datastore = True

    # Messages/Pipelines
    _message_class = messages.ContentArea
    _pipeline_class = pipelines.ContentAreaPipeline

    target = ndb.KeyProperty('t')
    section = ndb.StringProperty('s', choices=['prf', 'prj', 'sys'])  # profile, project or system
    html = ndb.BlobProperty('ht', compressed=False)
    text = ndb.TextProperty('tx', compressed=False)
    versions = ndb.KeyProperty('v', repeated=True)


# ContentSnippet - a content value for a content area (multiple exist for an area only for versioned content sections)
class ContentSnippet(AppModel):

    ''' Represents a versioned content value of a content area. '''

    # Storage Settings
    _use_cache = True
    _use_memcache = True
    _use_datastore = True

    # Messages/Pipelines
    _message_class = messages.ContentSnippet
    _pipeline_class = pipelines.ContentSnippetPipeline

    area = ndb.KeyProperty('a')
    html = ndb.BlobProperty('h', compressed=False)
    text = ndb.TextProperty('t', compressed=True)


## ContentSummary - a shortened summary value for a content area's content
class ContentSummary(AppModel):

    ''' Represents a summary of content in a content area. '''

    # Storage Settings
    _use_cache = True
    _use_memcache = True
    _use_datastore = True

    # Messages/Pipelines
    _message_class = messages.ContentSummary
    _pipeline_class = pipelines.ContentSummaryPipeline

    target = ndb.KeyProperty('t')
    html = ndb.BlobProperty('ht', compressed=False)
    text = ndb.TextProperty('tx', compressed=False)
