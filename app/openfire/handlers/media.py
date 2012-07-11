# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.handlers import WebHandler
from google.appengine.ext.webapp import blobstore_handlers
from openfire.models.assets import Asset, Avatar, Image, Video
import logging


class BlobstoreUploaded(blobstore_handlers.BlobstoreUploadHandler):

    ''' Handle Responses from the google blog store. '''

    def post(self, asset_key, target_key=None):

        ''' Handle google blobstore repsonses. '''

        asset_key = ndb.Key(urlsafe=asset_key)
        asset = asset_key.get()
        if asset:
            asset.pending = False
            asset.put()

        # If there is a target, attach this media to a project or user.
        if target_key:
            target = ndb.Key(urlsafe=target_key).get()
            if target:
                # TODO: Populate a few more fields of Image and Avatar here, like size and name. -Ethan
                if asset.kind == 'i' and hasattr(target, 'images'):
                    image = Image(asset=asset_key)
                    image.put()
                    target.images.append(image.key)
                    target.put()
                elif asset.kind == 'a' and hasattr(target, 'avatar'):
                    avatar = Avatar(asset=asset_key, active=True)
                    avatar.put()
                    target.avatar.append(avatar.key)
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

        self.response.body = '[{"key":"' + asset_key + '"}]'
