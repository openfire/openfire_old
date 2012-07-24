# -*- coding: utf-8 -*-

## Basic Imports
import hashlib
import webapp2

## SDK Imports
from google.appengine.ext import ndb

## Lib Imports
from protorpc import remote
from apptools.services import RequestError
from openfire.services import RemoteService

## Content API
from openfire.core import content

## Models, Messages + Pipelines
from openfire.models import user
from openfire.models import project
from openfire.models import content as models
from openfire.messages import content as messages
from openfire.pipelines import content as pipelines


## ContentServiceException - parent class for all content service exceptions
class ContentServiceException(RequestError):
    pass


## ContentService
class ContentService(RemoteService, content.ContentBridge):

    ''' Server-side backend for content management features. '''

    @webapp2.cached_property
    def _content_bridge(self):

        ''' Load and resolve a content bridge. '''

        bridge = content.ContentBridge()
        bridge._initialize_dynamic_content(self.handler.app, self.handler, self)
        return bridge

    @remote.method(messages.SaveContent, messages.ContentResponse)
    def save(self, request):

        ''' Save a content area. '''

        pass

    @remote.method(messages.GetContent, messages.ContentResponse)
    def get(self, request):

        ''' Retrieve a content area. '''

        pass

    @remote.method(messages.GetContentMulti, messages.ContentResponseMulti)
    def save_multi(self, request):

        ''' Save multiple content areas in batch. '''

        pass

    @remote.method(messages.SaveContentMulti, messages.ContentResponseMulti)
    def get_multi(self, request):

        ''' Get multiple content areas in batch. '''

        pass

    @remote.method(messages.ContentArea, messages.ContentArea)
    def save_snippet(self, request):

        ''' Save a snippet of dynamic content. '''

        # resolve namespace
        namespace = self._content_bridge.get_dynamic_namespace(request.namespace)
        hashed_keyname = hashlib.sha256(request.keyname).hexdigest()

        # process content area
        area = models.ContentArea.get_by_id(request.keyname, parent=namespace)
        if area is None:
            area = models.ContentArea(**{
                'key': ndb.Key(models.ContentArea, hashed_keyname, parent=namespace),
                'html': request.html,
                'text': request.text,
                'local': True
            })
        else:
            area.html = request.html
            area.text = request.text
            area.local = True

        # process content snippet
        area_key = area.put()

        # build response
        return messages.ContentArea(keyname=hashed_keyname, namespace=namespace.urlsafe(), html=area.html, text=area.text)
