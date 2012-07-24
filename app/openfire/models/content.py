# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel


# Model Attachments
from openfire.messages import content as messages
from openfire.pipelines.model import content as pipelines


######## ======== XMS Content Models ======== ########

# ContentNamespace - groups runtime sections of dynamic content, if not assigned a datastore key as a namespace
class ContentNamespace(AppModel):

    ''' Represents a group of ContentAreas namespaced by something other than a datastore key (otherwise they are put under that and just correlated here). '''

    # Storage Settings
    _use_cache = True
    _use_memcache = True
    _use_datastore = True

    name = ndb.StringProperty('n', required=True, indexed=True)
    target = ndb.KeyProperty('t', required=False, indexed=True, default=None)
    areas = ndb.KeyProperty('a', repeated=True, indexed=True)


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

    html = ndb.TextProperty('ht', compressed=False)
    text = ndb.TextProperty('tx', compressed=False)
    local = ndb.BooleanProperty('lc', default=False)
    latest = ndb.KeyProperty('l', default=None)
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
    html = ndb.TextProperty('h', compressed=True)
    text = ndb.TextProperty('t', compressed=True)
    summary = ndb.KeyProperty('s')


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
