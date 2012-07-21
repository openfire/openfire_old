# -*- coding: utf-8 -*-

## Lib Imports
from protorpc import remote
from apptools.services import RequestError
from openfire.services import RemoteService

## Models, Messages + Pipelines
from openfire.models import content as models
from openfire.messages import content as messages
from openfire.pipelines import content as pipelines


## ContentServiceException - parent class for all content service exceptions
class ContentServiceException(RequestError):
    pass


## ContentService
class ContentService(RemoteService):

    ''' Server-side backend for content management features. '''

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
