# -*- coding: utf-8 -*-

## Core Imports
from openfire.core import CoreAPI

## NDB Imports
from google.appengine.ext import ndb
from google.appengine.ext.ndb import context
from google.appengine.ext.ndb import tasklet

## SDK Imports
from google.appengine.api import memcache
from google.appengine.ext import blobstore

## Openfire Imports
from openfire.models import content as models


class CoreContentAPI(CoreAPI):

    ''' Core API for managing dynamic content. '''

    # Content Models
    areas = []
    snippets = []

    # Structure Cache
    keygroups = []
    heuristics = []

    # Class References
    handler = None
    service = None

    ## == System Methods == ##
    def __init__(self, handler=None, service=None):

        ''' Init the Core Content API, and attach the handler/service. '''

        if handler is not None:
            self.handler = handler
        elif service is not None:
            self.service = service
            self.handler = service.handler

    ## == Low-level Methods == ##
    @ndb.tasklet
    def _batch_fulfill(self, batch):
        pass

    @ndb.tasklet
    def _run_query(self, query, options):
        pass

    @ndb.tasklet
    def _consider_result(self, result):
        pass

    ## == Mid-level Methods == ##
    def _build_keygroup(self):
        pass

    def _build_area_key(self):
        pass

    def _build_snippet_key(self):
        pass

    def _build_summary_key(self):
        pass

    def _walk_jinja2_ast(self):
        pass

    ## == High-level Methods == ##
    def resolve_content_area(self):
        pass

    def encounter_content_area(self):
        pass


class ContentMixin(object):

    ''' Mixin that bridges dynamic content methods into RemoteServices and WebHandlers. '''

    __content_bridge = None

    def __acquire_content_bridge(self):

        ''' Resolve the current instance of the CoreContentAPI, or create one. '''

        if self.__content_bridge is None:
            self.__content_bridge = CoreContentAPI(handler=self)
        return self.__content_bridge
