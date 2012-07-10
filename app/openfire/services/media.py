from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from protorpc import remote
from apptools.services.builtin import Echo
from openfire.core.data import CoreDataAPI
from openfire.services import RemoteService
from openfire.models.assets import Asset
import openfire.messages.media as messages
import base64

class MediaService(RemoteService):

    ''' Media service api. '''

    @remote.method(messages.GenerateEndpoint, messages.Endpoint)
    def generate_endpoint(self, request):

        ''' Generate and endpoint to upload something for the content editor. '''

        # Create an asset which is marked as uploading.
        asset = Asset().put()
        asset_key = asset.urlsafe()
        target_key = request.target
        handler_url = '/_assets/blob_uploaded/%s' % asset_key
        if target_key and len(target_key):
            handler_url += '/%s' % target_key
        return messages.Endpoint(endpoints=[blobstore.create_upload_url(handler_url)])


    @remote.method(messages.AttachImage, messages.AttachImageEndpoint)
    def attach_image(self, request):

        ''' Attach an image to a project or profile. '''

        target_key = ndb.Key(urlsafe=base64.b64decode(request.target.split(':')[1]))
        if not target_key:
            raise remote.ApplicationError('no target provided for image')

        target = target_key.get()
        if not target:
            raise remote.ApplicationError('no target found for image')

        asset = Asset(kind='i').put()

        handler_url = '/_assets/blob_uploaded/%s/%s' % (asset.urlsafe(), target_key.urlsafe())

        return messages.AttachImageEndpoint(endpoint=blobstore.create_upload_url(handler_url))


    @remote.method(messages.AttachAvatar, messages.AttachAvatarEndpoint)
    def attach_avatar(self, request):

        ''' Attach an avatar to a project or profile. '''

        target_key = ndb.Key(urlsafe=base64.b64decode(request.target.split(':')[1]))
        if not target_key:
            raise remote.ApplicationError('no target provided for image')

        target = target_key.get()
        if not target:
            raise remote.ApplicationError('no target found for image')

        asset = Asset(kind='a').put()

        handler_url = '/_assets/blob_uploaded/%s/%s' % (asset.urlsafe(), target_key.urlsafe())

        return messages.AttachAvatarEndpoint(endpoint=blobstore.create_upload_url(handler_url))


    @remote.method(messages.AttachVideo, Echo)
    def attach_video(self, request):

        ''' Attach a video. '''

        return Echo(message='')
