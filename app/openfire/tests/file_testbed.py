'''
This file is needed becuase init_blobstore_stub does not support
uploading files to the blobstore. The code was adapted from this
stackoverflow post:
http://stackoverflow.com/questions/8130063/test-function-with-google-app-engine-files-api
'''
from google.appengine.ext import testbed
from google.appengine.api.blobstore import blobstore_stub, file_blob_storage
from google.appengine.api.files import file_service_stub

class TestbedWithFiles(testbed.Testbed):

    ''' Create a testbed that can accept and serve blobstore files. '''

    def init_blobstore_stub(self):
        blob_storage = file_blob_storage.FileBlobStorage('/tmp/testbed.blobstore',
                                                testbed.DEFAULT_APP_ID)
        blob_stub = blobstore_stub.BlobstoreServiceStub(blob_storage)
        file_stub = file_service_stub.FileServiceStub(blob_storage)
        self._register_stub('blobstore', blob_stub)
        self._register_stub('file', file_stub)
