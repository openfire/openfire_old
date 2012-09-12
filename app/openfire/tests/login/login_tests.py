# -*- coding: utf-8 -*-
"""
Login tests.
"""

import unittest
from openfire.tests import OFTestCase, LoggedInTestCase
import openfire.fixtures.fixture_util as db_loader

import bootstrap
bootstrap.AppBootstrapper.prepareImports()
from apptools import dispatch

import webapp2


class BasicLoginTestCase(OFTestCase):

    """ Test site login and logout. """

    @unittest.expectedFailure
    def test_basic_login(self):

        """ Does not currently work. See OF-155 for more details. """

        # Run the fixtures.
        """
        fixture_response = self.of_handler_test('/_dev/data', desired_response_code=302, expect_response_content=False,
                error='Failed to load the fixture data at /_dev/data.')

        login_post = {
            'username': 'ethan.leland@gmail.com',
            'password': 'ethaniscool',
        }
        """

        login_request = webapp2.Request.blank('/login', POST=login_post)

        login_request.method = 'POST'
        login_response = login_request.get_response(dispatch.gateway)

        homepage_request = webapp2.Request.blank('/')
        homepage_response = homepage_request.get_response(dispatch.gateway)

        logout_request = webapp2.Request.blank('/logout')
        logout_response = logout_request.get_response(dispatch.gateway)



""""
class ServiceLoginTestCase(OFTestCase):

    ''' Test cases for service that use login. '''

    def test_service_login(self):

        ''' Test the basic login for service calls. '''

        params = {}
        response = self.of_service_test('TODO: service name', 'TODO: service method', params=params)
"""
