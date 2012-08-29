import hashlib
import datetime
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from apptools import BaseHandler

from openfire.models import system
from openfire.handlers import WebHandler
from openfire.handlers import NamespaceBridge

from openfire.fixtures import fixture_loader


class TestMultipart(BaseHandler):

    ''' Test multipart uploads. '''

    def get(self):

        ''' Return the form. '''

        from google.appengine.ext import blobstore
        return self.render('test/multipart.html', endpoint=blobstore.create_upload_url('/_test/multipart/passthrough'))


class TestPassthrough(blobstore_handlers.BlobstoreUploadHandler):

    ''' Test the blobstore passthrough. '''

    def post(self):

        ''' Passthrough. '''

        uploads = self.get_uploads()

        return self.response.write('<pre>' + str(self.request) + '</pre>')


class DevModels(BaseHandler, NamespaceBridge):

    ''' Quickly insert some dev models for testing. This is NOT meant to be a full, permanent fixture. '''

    force_load_session = False

    def get(self):

        ''' Load the fixtures if they have not already been loaded. '''

        self.prepare_namespace(self.request)

        run = True
        flag = system.SystemProperty.get('fixture', 'openfire.dev.BaseDataFixture')
        if flag:
            run = (not flag.has_run)
            if not run:
                return self.redirect_to('landing')

        # Load all the fixtures.
        fixture_loader.load_fixtures()

        return self.redirect_to('landing')


class JasmineTests(WebHandler, NamespaceBridge):

    ''' Return the page that will run all of our jasmine unit tests. '''

    template = 'test/jasmine_tests.html'

    def get(self):

        ''' Just return the jasmine test page. '''

        return self.render('test/jasmine_tests.html')
