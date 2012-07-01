from google.appengine.ext import ndb
from protorpc import remote
from apptools.services.builtin import Echo
from openfire.core.data import CoreDataAPI
from openfire.services import RemoteService
from openfire.models.assets import CustomURL
from openfire.messages.common import CustomUrl as CustomUrlMessage
from openfire.messages.common import CustomUrls as CustomUrlsMessage
from openfire.messages.common import CustomUrlCheck as CustomUrlCheckMessage

class CustomUrlService(RemoteService):

    ''' Custom URL service api. '''

    @remote.method(CustomUrlMessage, CustomUrlMessage)
    def get(self, request):

        ''' Get a custom URL for a target Project or User. '''

        url_key = ndb.Key('CustomURL', request.slug)
        custom_url = url_key.get()
        return custom_url.to_message()


    @remote.method(CustomUrlMessage, CustomUrlsMessage)
    def list(self, request):

        ''' List all custom URLs for target Projects or Users. '''

        urls = CustomURL.query().fetch()
        messages = []
        for url in urls:
            messages.append(url.to_message())
        return CustomUrlsMessage(urls=messages)


    @remote.method(CustomUrlMessage, CustomUrlMessage)
    def put(self, request):

        ''' Create a new custom URL. If the url is already in use, error.'''

        url_key = ndb.Key('CustomURL', request.slug)
        custom_url = url_key.get()

        if custom_url != None:
            # Url is already in use.
            raise remote.ApplicationError('Custom URL already exists.')

        target = ndb.Key(urlsafe=request.target)
        custom_url = CustomURL(key=url_key, slug=request.slug, target=target)
        custom_url.put()

        return custom_url.to_message()


    @remote.method(CustomUrlMessage, Echo)
    def delete(self, request):

        ''' Remove a custom URL from a target, if it exists. '''
        url_key = ndb.Key(urlsafe=request.key)
        url_key.delete()
        return Echo(message='custom url removed')


    @remote.method(CustomUrlMessage, CustomUrlCheckMessage)
    def check(self, request):

        ''' Check to see if a url slug is available. '''

        return CustomUrlCheckMessage(slug=request.slug,
            taken=CoreDataAPI.custom_url_taken(request.slug))
