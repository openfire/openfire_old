# -*- coding: utf-8 -*-
"""
Sessions tests.
"""

from openfire.tests import OFTestCase
import openfire.fixtures.fixture_util as db_loader

class DatastoreSessionLoaderTestCase(OFTestCase):

    ''' Test the datastore session loader. '''

    pass


class MemcacheSessionLoaderTestCase(OFTestCase):

    ''' Test the memcache session loader. '''

    pass


class ThreadcacheSessionLoaderTestCase(OFTestCase):

    ''' Test the threadcache session loader. '''

    pass


class SessionManagerTestCase(OFTestCase):

    ''' Test the session manager. '''

    pass


class SessionAPITestCase(OFTestCase):

    ''' Test the session API test case. '''

    pass


class SessionCollectorTestCase(OFTestCase):

    ''' Test the Session garbage collector. '''

    pass
