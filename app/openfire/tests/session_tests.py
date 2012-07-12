# -*- coding: utf-8 -*-
"""
Sessions tests.
"""

import unittest
from google.appengine.ext import testbed

import bootstrap
bootstrap.AppBootstrapper.prepareImports()
from apptools import dispatch

import webapp2

import test_db_loader as db_loader

from test_util import encrypt, decrypt

class DatastoreSessionLoaderTestCase(unittest.TestCase):

    ''' Test the datastore session loader. '''

    pass


class MemcacheSessionLoaderTestCase(unittest.TestCase):

    ''' Test the memcache session loader. '''

    pass


class ThreadcacheSessionLoaderTestCase(unittest.TestCase):

    ''' Test the threadcache session loader. '''

    pass


class SessionManagerTestCase(unittest.TestCase):

    ''' Test the session manager. '''

    pass


class SessionAPITestCase(unittest.TestCase):

    ''' Test the session API test case. '''

    pass


class SessionCollectorTestCase(unittest.TestCase):

    ''' Test the Session garbage collector. '''

    pass
