from apptools.services.builtin import Echo
from protorpc import message_types, remote
from openfire.services import RemoteService

class BBQService(RemoteService):

    ''' BBQ service api. '''

    @remote.method(message_types.VoidMessage, Echo)
    def grant(self, request):

        ''' Grant a permission. '''

        return Echo(message='Granted')


    @remote.method(message_types.VoidMessage, Echo)
    def revoke(self, request):

        ''' Revoke a permission. '''

        return Echo(message='Revoked')


    @remote.method(message_types.VoidMessage, Echo)
    def flush_cache(self, request):

        ''' Flush memcache. '''

        return Echo(message='Flush cache')


    @remote.method(message_types.VoidMessage, Echo)
    def create_user(self, request):

        ''' Create a user. '''

        return Echo(message='Create user')
