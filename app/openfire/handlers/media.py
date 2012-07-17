# -*- coding: utf-8 -*-
from google.appengine.ext import ndb, blobstore
from openfire.handlers import WebHandler
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.blobstore import BlobReader
from openfire.models.assets import Asset, Avatar, Image, Video
from google.appengine.api import images
import logging
from webapp2 import RequestHandler
import base64


class BlobstoreUploaded(blobstore_handlers.BlobstoreUploadHandler, RequestHandler):

    ''' Handle Responses from the google blog store. '''

    def post(self, asset_key, target_key=None):

        ''' Handle google blobstore repsonses. '''

        import pdb; pdb.set_trace()

        upload = None
        try:
            upload = self.get_uploads('file')[0]
        except:
            logging.critical('Failed to get call "self.get_uploads()"')

        asset_key = ndb.Key(urlsafe=asset_key)
        asset = asset_key.get()
        if asset:
            asset.pending = False
            asset.blob = upload.key()
            asset.mime = upload.content_type
            asset.url = self.url_for('serve-asset-filename', action='serve', asset_key=asset.key.urlsafe(), filename=upload.filename)
            asset.put()

        # If there is a target, attach this media to a project or user.
        if target_key:
            target = ndb.Key(urlsafe=target_key).get()
            if target:
                # TODO: Populate a few more fields of Image and Avatar here, like size and name. -Ethan
                if asset.kind == 'i' and hasattr(target, 'images'):
                    image = Image(asset=asset_key, parent=target.key)
                    image.put()
                    target.images.append(image.key)
                    target.put()
                elif asset.kind == 'a' and hasattr(target, 'avatar'):
                    # TODO: Set all other avatars as inactive?
                    avatar = Avatar(id=asset_key.urlsafe(), asset=asset_key, active=True, parent=target.key)
                    avatar.put()
                    target.avatar = avatar.key
                    target.put()
                else:
                    # We do not currently support any kind other than image.
                    # Eventually we will support 's', 't', 'v' (style, script, video)
                    pass

        return self.redirect('/_assets/get/%s' % asset_key.urlsafe())


class MediaStorage(WebHandler):

    ''' Get a json struct describing how to get an asset from the blobstore. '''

    def get(self, asset_key):

        ''' Get a json struct describing how to get an asset from the blobstore. '''

        self.response.write('[{"key":"' + asset_key + '"}]')


class AssetServer(WebHandler):

    def get(self, action, asset_key, filename=''):

        asset_key = ndb.Key(urlsafe=asset_key)
        asset = asset_key.get()
        if not asset:
            return self.error(404)
        if not asset.blob:
            return self.error(404)

        blob_info = blobstore.get(asset.blob)
        if not blob_info:
            return self.error(404)

        value = BlobReader(blob_info.key(), buffer_size=blob_info.size).read()
        self.response.body = value

        self.response.headers['Content-Type'] = str(blob_info.content_type)
        if action == 'get':
            self.response.headers['Content-Disposition'] = str('attachment; filename=' + blob_info.filename)

        return self.response


"""
class FutureAssetServer(blobstore_handlers.BlobstoreDownloadHandler):

    ''' Serve an asset from the blobstore...correctly. '''

    def get(self, action, asset_key, filename=''):

        asset_key = ndb.Key(urlsafe=asset_key)
        asset = asset_key.get()
        if not asset:
            return self.error(404)
        blob_info = blobstore.get(asset.blob)

        url = images.get_serving_url(asset.blob)
        return self.redirect(str(url))

        #img = images.Image(blob_key=asset.blob)
        #return self.send_blob(blob_info, content_type=blob_info.content_type)
"""
