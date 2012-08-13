# -*- coding: utf-8 -*-
'''
Model tests for openfire.
'''

from openfire.tests import OFTestCase

from openfire.models.project import Category
import openfire.fixtures.fixture_util as db_loader

class FixturesTestCase(OFTestCase):

    ''' Load the fixtures through the dev url. '''

    def test_load_fixtures(self):
        self.of_handler_test('/_dev/data', desired_response_code=302, expect_response_content=False,
                error='Failed to load the fixture data at /_dev/data.')


class CategoryTestCase(OFTestCase):

    ''' Test loading a category into the database. '''

    def test_insert_category(self):

        ''' Test loading a category into the database. '''

        category_key = db_loader.create_category()
        self.assertTrue(category_key, "Failed to create an entity and return a key.")
        self.assertEqual(1, len(Category.query().fetch(2)), "Failed to retrieve a stored entity.")
