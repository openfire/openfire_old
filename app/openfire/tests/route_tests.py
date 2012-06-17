# -*- coding: utf-8 -*-
"""
Route tests.
"""
from google.appengine.dist import use_library
use_library('django', '1.2')

import unittest
from google.appengine.ext import testbed

import bootstrap
bootstrap.AppBootstrapper.prepareImports()
from apptools import dispatch

import webapp2


def generic_view_success_test(test_case, url):
    """ A generic success test for a given url.
    """
    request = webapp2.Request.blank(url)
    response = request.get_response(dispatch.gateway)
    test_case.assertEqual(response.status_int, 200)
    test_case.assertTrue(len(response.body))


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

    def tearDown(self):
        self.testbed.deactivate()

    def test_propose_page(self):
        generic_view_success_test(self, '/propose')

    def test_apply_page(self):
        generic_view_success_test(self, '/apply')

    def test_proposal_page(self):
        generic_view_success_test(self, '/project/proposaltoken')


class ProjectPageTestCase(unittest.TestCase):
    """ Test cases for the project landing and project homepage.
    """

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_projects_page(self):
        generic_view_success_test(self, '/projects')

    def test_project_page(self):
        generic_view_success_test(self, '/project/fakeproject')


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
