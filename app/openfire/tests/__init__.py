import unittest
from google.appengine.ext import testbed
from google.appengine.api.blobstore import blobstore_stub, file_blob_storage
from google.appengine.api.files import file_service_stub

import bootstrap
bootstrap.AppBootstrapper.prepareImports()
from apptools import dispatch

import webapp2
import json
import copy
import os

from openfire.core.sessions import SessionsBridge


def load_tests(loader, standard_tests, pattern):

    ''' Override the test discovery method and load all tests ourselves. '''

    # Load anything that matches the passed in pattern.
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern=pattern)

    # Load all the tests in all current subdirectories.
    test_directories = [d for d in os.listdir(this_dir) if os.path.isdir(os.path.join(this_dir, d))]
    for directory in test_directories:
        package_tests.addTest(loader.discover(start_dir=os.path.join(this_dir, directory), pattern='*'))

    # Add all the tests to the current suite.
    standard_tests.addTests(package_tests)
    return standard_tests


# Dict used for api service posts.
API_DICT = {
    'id':1,
    'opts':{},
    'agent':{},
    'request': {
        'params': {},
        'method':'echo',
        'api':'system',
    },
}


class OFTestCase(unittest.TestCase):

    ''' A base class for all openfire tests to inherit from. '''

    def setUp(self):

        ''' A generic google app engine test setup method. '''

        self.testbed = TestbedWithFiles()
        self.testbed.activate()

        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_blobstore_stub()
        self.testbed.init_images_stub()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_taskqueue_stub()

        os.environ['RUNNING_TESTS'] = 'TESTING'

    def tearDown(self):

        ''' A generic google app engine test tear down method. '''

        self.testbed.deactivate()
        os.environ['RUNNING_TESTS'] = ''

    def encrypt(self, value, simple=True, cipher=True):

        ''' An common alias to encryption. '''

        return SessionsBridge().encrypt(value, simple=simple, cipher=cipher)

    def decrypt(self, value):

        ''' An common alias to decryption. '''

        return SessionsBridge().decrypt(value)

    def of_service_test(self, service_name, service_method, params={}, request_method='POST', should_fail=False):

        ''' A generic success test for a given service url.

        Returns a response dict loaded from the response body with json.
        '''

        requestDict = copy.deepcopy(API_DICT)
        requestDict['request']['api'] = service_name
        requestDict['request']['method'] = service_method
        requestDict['request']['params'] = params
        request = webapp2.Request.blank('/_api/rpc/%s.%s' % (service_name, service_method))
        request.headers['content-type'] = 'application/json'
        request.method = request_method
        request.body = json.dumps(requestDict)
        response = request.get_response(dispatch.gateway)
        if not should_fail:
            self.assertEqual(response.status_int, 200)
            self.assertTrue(len(response.body))
        responseDict = json.loads(response.body)
        self.assertTrue(responseDict)
        return responseDict

    def of_handler_test(self, url, desired_response_code=200, expect_response_content=True,
                error='generic handler error', is_post=False, post_data=None):

        ''' A generic success test for a given url.

        Returns the response that was retreived from the gateway.
        '''

        request = webapp2.Request.blank(url, POST=post_data)
        if is_post:
            request.method = 'POST'
        response = request.get_response(dispatch.gateway)
        self.assertEqual(response.status_int, desired_response_code, error)
        if expect_response_content:
            self.assertTrue(len(response.body), error)
        return response



'''
This file is needed becuase init_blobstore_stub does not support
uploading files to the blobstore. The code was adapted from this
stackoverflow post:
http://stackoverflow.com/questions/8130063/test-function-with-google-app-engine-files-api
'''

class TestbedWithFiles(testbed.Testbed):

    ''' Create a testbed that can accept and serve blobstore files. '''

    def init_blobstore_stub(self):
        blob_storage = file_blob_storage.FileBlobStorage('/tmp/testbed.blobstore',
                                                testbed.DEFAULT_APP_ID)
        blob_stub = blobstore_stub.BlobstoreServiceStub(blob_storage)
        file_stub = file_service_stub.FileServiceStub(blob_storage)
        self._register_stub('blobstore', blob_stub)
        self._register_stub('file', file_stub)
