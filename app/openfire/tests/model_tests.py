# -*- coding: utf-8 -*-
"""
Model tests.
"""
from google.appengine.dist import use_library
use_library('django', '1.2')

import unittest
#from google.appengine.ext import db
#from google.appengine.api import memcache
from google.appengine.ext import testbed

from openfire.models.project import Category
import test_db_loader as db_loader

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
