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

        # TODO: Do more with the target when possible. -Ethan
        if target_key:
            target_key = ndb.Key(urlsafe=target_key)

        return self.redirect('/_assets/get/%s' % asset_key.urlsafe())


class MediaStorage(WebHandler):

    ''' Get a json struct describing how to get an asset from the blobstore. '''

    def get(self, asset_key):

        ''' Get a json struct describing how to get an asset from the blobstore. '''

        self.response.body = '[{"key":"' + asset_key + '"}]'
