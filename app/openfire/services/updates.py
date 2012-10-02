# -*- coding: utf-8 -*-

# Base
import webapp2
from apptools import debug
from protorpc import remote

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

    @webapp2.cached_property
    def config(self):

        ''' Named config pipe. '''

        return config.config.get('openfire.project.updates', {})

    def logging(self):

        ''' Named logging pipe. '''

        return debug.AppToolsLogger(path='openfire.services.updates', name='UpdatesServices')._setcondition(self.config.get('debug', False))

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
