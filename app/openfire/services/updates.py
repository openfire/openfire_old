# -*- coding: utf-8 -*-

# Base
import config
import webapp2
from protorpc import remote
from apptools.util import debug
from apptools.util import datastructures

# Models
from openfire.models import user
from openfire.models import social
from openfire.models import project

# Messages + Services
from openfire.messages import common
from openfire.messages import updates
from openfire.services import RemoteService


## Updates API.
class UpdatesService(RemoteService):

    ''' Interact with project updates. '''

    ## +=+=+ Exceptions +=+=+ ##
    class UpdateServiceException(RemoteService.exceptions.ApplicationError): ''' Base exception for all errors specific to the Updates Service. '''
    class LoginRequired(UpdateServiceException): ''' Thrown when login is required to perform an action on the Updates Service. '''
    class NotAuthorized(UpdateServiceException): ''' Thrown when a user is logged in, but not allowed to post/read updates on the specified subject. '''
    class InvalidSubject(UpdateServiceException): ''' Thrown when a subject key cannot be resolved, or is of an invalid type. '''

    exceptions = datastructures.DictProxy({

        'LoginRequired': LoginRequired,
        'NotAuthorized': NotAuthorized,
        'InvalidSubject': InvalidSubject

    })

    ## +=+=+ Internals +=+=+ ##
    @webapp2.cached_property
    def config(self):

        ''' Named config pipe. '''

        return config.config.get('openfire.project.updates', {})

    @webapp2.cached_property
    def logging(self):

        ''' Named logging pipe. '''

        return debug.AppToolsLogger(path='openfire.services.updates', name='UpdatesServices')._setcondition(self.config.get('debug', False))

    ## +=+=+ Exposed Methods +=+=+ ##
    @remote.method(updates.Update, updates.Update)
    def publish(self, request):

        ''' Publish a new update, under a user profile or project. '''

        pass

    @remote.method(common.Comment, common.Comment)
    def comment(self, request):

        ''' Comment on an update. '''

        pass

    @remote.method(updates.Update, common.Comments)
    def comments(self, request):

        ''' Retrieve comments on an update. '''

        pass
