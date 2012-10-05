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

    def test_basic_login(self):

        """ Does not currently work. See OF-155 for more details. """

        db_loader.create_user(username='fakie', password='test', email='fakie@mcfakerton.com')
        cookie =  self.get_login_cookie('fakie', 'test')
        self.assertTrue(cookie, 'Failed to get a cookie when logging in.')


""""
class ServiceLoginTestCase(OFTestCase):

    ''' Test cases for service that use login. '''

    def test_service_login(self):

        ''' Test the basic login for service calls. '''

        params = {}
        response = self.of_service_test('TODO: service name', 'TODO: service method', params=params)
"""
