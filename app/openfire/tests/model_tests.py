# -*- coding: utf-8 -*-
"""
Model tests.
"""

import unittest
#from google.appengine.ext import db
#from google.appengine.api import memcache
from google.appengine.ext import testbed
import webapp2

from openfire.tests.file_testbed import TestbedWithFiles

from openfire.models.project import Category
import test_db_loader as db_loader

import bootstrap
bootstrap.AppBootstrapper.prepareImports()
from apptools import dispatch

from test_util import encrypt, decrypt

class FixturesTestCase(unittest.TestCase):

    ''' Load the fixtures through the dev url. '''

    #fixtures = ['fixtures.json']

    def setUp(self):
        self.testbed = TestbedWithFiles()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_blobstore_stub()
        self.testbed.init_images_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_load_fixtures(self):
        request = webapp2.Request.blank("/_dev/data")
        response = request.get_response(dispatch.gateway)
        self.assertEqual(response.status_int, 302, "Failed to load fixtures. Returned: %d" % response.status_int)


class CategoryTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_insert_entity(self):
        category_key = db_loader.create_category()
        self.assertTrue(category_key, "Failed to create an entity and return a key.")
        self.assertEqual(1, len(Category.query().fetch(2)), "Failed to retrieve a stored entity.")
