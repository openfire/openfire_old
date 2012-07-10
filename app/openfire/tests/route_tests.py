# -*- coding: utf-8 -*-
"""
Route tests.
"""

import unittest
from google.appengine.ext import testbed

import bootstrap
bootstrap.AppBootstrapper.prepareImports()
from apptools import dispatch

import webapp2

import test_db_loader as db_loader


def generic_view_success_test(test_case, url, error="generic view error"):
    """ A generic success test for a given url.
    """
    request = webapp2.Request.blank(url)
    response = request.get_response(dispatch.gateway)
    test_case.assertEqual(response.status_int, 200, error)
    test_case.assertTrue(len(response.body), error)


class HomepageTestCase(unittest.TestCase):
    """ Test cases for the homepage.
    """

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_homepage(self):
        generic_view_success_test(self, '/')


class AboutPagesTestCase(unittest.TestCase):
    """ Test cases for the about/privacy/terms/etc pages.
    """

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_about_page(self):
        generic_view_success_test(self, '/about')

    def test_terms_page(self):
        generic_view_success_test(self, '/terms')

    def test_privacy_page(self):
        generic_view_success_test(self, '/privacy')

    def test_support_page(self):
        generic_view_success_test(self, '/support')


class UserPageTestCase(unittest.TestCase):
    """ Test cases for the user profile and account pages.
    """

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_users_page(self):
        generic_view_success_test(self, '/users')

    def test_user_profile_page(self):
        generic_view_success_test(self, '/user/fakie')

    def test_user_account_page(self):
        generic_view_success_test(self, '/user/fakie/account')


class ProposalPageTestCase(unittest.TestCase):
    """ Test cases for the proposal and apply pages.
    """

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        # Create a proposal with token 'proposaltoken'.
        db_loader.create_proposal()

    def tearDown(self):
        self.testbed.deactivate()

    def test_propose_page(self):
        generic_view_success_test(self, '/propose')

    def test_apply_page(self):
        generic_view_success_test(self, '/apply')

    def test_proposal_page(self):
        generic_view_success_test(self, '/proposal/proposaltoken')


class ProjectPageTestCase(unittest.TestCase):
    """ Test cases for the project landing and project homepage.
    """

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        # Create a project called 'fakeproject'.
        self.project_key = db_loader.create_project()

    def tearDown(self):
        self.testbed.deactivate()

    def test_projects_page(self):
        generic_view_success_test(self, '/projects')

    def test_project_page(self):
        # Visit the project at its key page.
        generic_view_success_test(self, '/project/' + self.project_key.urlsafe(), 'Failed to display project page.')


class BBQPageTestCase(unittest.TestCase):
    """ Test cases for the bbq admin moderation page.
    """

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_projects_page(self):
        generic_view_success_test(self, '/bbq')


class CustomUrlTestCase(unittest.TestCase):
    """ Test cases for the about/privacy/terms/etc pages.
    """

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

        # Create a project and a user.
        self.project_key = db_loader.create_project()
        self.user_key = db_loader.create_user()

    def tearDown(self):
        self.testbed.deactivate()

    def test_custom_project_url(self):
        db_loader.create_custom_url(slug='fakeproject', target_kind='Project', target_id=self.project_key.id())
        generic_view_success_test(self, '/fakeproject')

    def test_custom_user_url(self):
        db_loader.create_custom_url(slug='fakie', target_kind='User', target_id='fakie')
        generic_view_success_test(self, '/fakie')
