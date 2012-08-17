# -*- coding: utf-8 -*-
"""
Route tests.
"""

from openfire.tests import OFTestCase
import openfire.fixtures.fixture_util as db_loader


class HomepageTestCase(OFTestCase):
    """ Test cases for the homepage.
    """

    def test_homepage(self):
        self.of_handler_test('/')


class AboutPagesTestCase(OFTestCase):
    """ Test cases for the about/privacy/terms/etc pages.
    """

    def test_about_page(self):
        self.of_handler_test('/about')

    def test_terms_page(self):
        self.of_handler_test('/terms')

    def test_privacy_page(self):
        self.of_handler_test('/privacy')

    def test_support_page(self):
        self.of_handler_test('/support')


class UserPageTestCase(OFTestCase):
    """ Test cases for the user profile and account pages.
    """

    def test_users_page(self):
        self.of_handler_test('/users')

    def test_user_profile_page(self):
        user_key = db_loader.create_user(username='fakie')
        db_loader.create_custom_url(slug='fakie', target_key=user_key)
        self.of_handler_test('/fakie')

    def test_user_account_page(self):
        self.of_handler_test('/user/fakie/account')


class ProposalPageTestCase(OFTestCase):
    """ Test cases for the proposal and apply pages.
    """

    def setUp(self):
        super(ProposalPageTestCase, self).setUp()

        # Create a proposal with token 'proposaltoken'.
        db_loader.create_proposal()

    def tearDown(self):
        self.testbed.deactivate()

    def test_propose_page(self):
        self.of_handler_test('/propose')

    def test_apply_page(self):
        self.of_handler_test('/apply')

    def test_proposal_page(self):
        self.of_handler_test('/proposal/proposaltoken')


class ProjectPageTestCase(OFTestCase):
    """ Test cases for the project landing and project homepage.
    """

    def setUp(self):
        super(ProjectPageTestCase, self).setUp()

        # Create a project called 'fakeproject'.
        self.project_key = db_loader.create_project()

    def tearDown(self):
        self.testbed.deactivate()

    def test_projects_page(self):
        self.of_handler_test('/projects')

    def test_project_page(self):
        # Visit the project at its key page.
        self.of_handler_test('/project/' + self.project_key.urlsafe(), error='Failed to display project page.')


class BBQPageTestCase(OFTestCase):
    """ Test cases for the bbq admin moderation page.
    """

    def test_projects_page(self):
        self.of_handler_test('/bbq')


class CustomUrlTestCase(OFTestCase):
    """ Test cases for the about/privacy/terms/etc pages.
    """

    def setUp(self):
        super(CustomUrlTestCase, self).setUp()

        # Create a project and a user.
        self.project_key = db_loader.create_project()
        self.user_key = db_loader.create_user()

    def tearDown(self):
        self.testbed.deactivate()

    def test_custom_project_url(self):
        db_loader.create_custom_url(slug='fakeproject', target_key=self.project_key)
        self.of_handler_test('/fakeproject')

    def test_custom_user_url(self):
        db_loader.create_custom_url(slug='fakie', target_key=self.user_key)
        self.of_handler_test('/fakie')


class PaymentHandlerTestCase(OFTestCase):
    """ Test cases for the payment handler.
    """

    def test_payment_handler(self):
        self.of_handler_test('/_payment/handler')

