# -*- coding: utf-8 -*-
"""
Service tests.
"""
from google.appengine.dist import use_library
use_library('django', '1.2')

import unittest
from google.appengine.ext import testbed, ndb

import bootstrap
bootstrap.AppBootstrapper.prepareImports()
from apptools import dispatch

import webapp2
import json
import copy

import test_db_loader as db_loader
from openfire.models.project import Category


API_DICT = {
    'id':1,
    'opts':{},
    'agent':{},
    'request': {
        'params': {},
        'method':'echo',
        'api':'system',
    },
}


def generic_service_method_success_test(test_case, service_name, service_method, params={}):
    ''' A generic success test for a given service url.
    Returns a response dict loaded from the response body with json.
    '''

    requestDict = copy.deepcopy(API_DICT)
    requestDict['request']['api'] = service_name
    requestDict['request']['method'] = service_method
    requestDict['request']['params'] = params
    request = webapp2.Request.blank('/_api/rpc/%s.%s' % (service_name, service_method))
    request.headers['content-type'] = 'application/json'
    request.method = 'POST'
    request.body = json.dumps(requestDict)
    response = request.get_response(dispatch.gateway)
    test_case.assertEqual(response.status_int, 200)
    test_case.assertTrue(len(response.body))
    responseDict = json.loads(response.body)
    test_case.assertTrue(responseDict)
    return responseDict


class SystemServiceTestCase(unittest.TestCase):
    ''' Test cases for user services.
    '''

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_echo_service_method(self):
        message_content = 'TESTING'
        echoParams = {'message': message_content}
        response = generic_service_method_success_test(self, 'system', 'echo', params=echoParams)
        self.assertEqual(response['response']['content']['message'], message_content, 'System echo service method failed.')

    def test_hello_service_method(self):
        response = generic_service_method_success_test(self, 'system', 'hello')
        self.assertTrue(response['response']['content']['message'].startswith('Hello'), 'System hello service failed.')


class ProjectServiceTestCase(unittest.TestCase):
    ''' Test cases for the project service.
    '''

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_project_list_method(self):
        ''' Add one private and one public project to the database then query. '''
        db_loader.create_project(slug='test-1')
        db_loader.create_project(slug='test-2', status='p')
        response = generic_service_method_success_test(self, 'project', 'list')
        self.assertEqual(response['response']['type'], 'Projects',
            'System project list service method failed.')
        self.assertEqual(len(response['response']['content']['projects']), 1,
            'Failed to return the correct number of projects.')

    def test_project_get_method(self):
        ''' Add one private and one public project to the database then query. '''
        slug = 'test-1'
        db_loader.create_project(slug=slug)
        response = generic_service_method_success_test(self, 'project', 'get', params={'slug':slug})
        self.assertEqual(response['response']['type'], 'Project',
            'Project get service method failed.')
        self.assertEqual(response['response']['content']['slug'], slug,
            'Project get method returned the wrong project.')

    def test_project_put_method(self):

        ''' Add a project (not through api) and then update it. '''

        slug = 'savetheeverything'
        proposalKey = ndb.Key('Proposal', 'fake')
        categoryKey = ndb.Key('Category', slug)
        creatorKey = ndb.Key('User', 'fakie')
        name_1 = 'Save the Everything!'
        pitch_1 = 'Save all the animals!'
        name_2 = 'Save everything!!'
        pitch_2 = 'Yeah, save all those things.'

        db_loader.create_project(slug=slug, name=name_1, pitch=pitch_1,
                    proposal=proposalKey, category=categoryKey, creator=creatorKey)

        params = {
            'key': slug,
            'slug': slug,
            'name': name_2,
            'pitch': pitch_2,
        }

        response = generic_service_method_success_test(self, 'project', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Project',
            'Project put service method failed.')
        self.assertEqual(response['response']['content']['name'], name_2,
            'Project put failed to change the name.')
        self.assertEqual(response['response']['content']['pitch'], pitch_2,
            'Project put failed to change the description.')



    """
    " We will fill in these tests as the service methods are implemented.
    "

    def test_project_comment_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'comment', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_comments_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'comments', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_post_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'post', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_posts_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'posts', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_media_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'media', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_add_media_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'add_medai', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_follow_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'follow', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_followers_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'followers', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_backers_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'backers', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_back_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'back', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_suspend_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'suspend', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_shutdown_method(self):
        ''' Test something. '''
        response = generic_service_method_success_test(self, 'project', 'shutdown', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')
    """


class ProposalServiceTestCase(unittest.TestCase):
    ''' Test cases for the proposal service.
    '''

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_proposal_list_method(self):
        ''' Add a proposal to the database then query. '''
        db_loader.create_proposal(slug='test-1')
        response = generic_service_method_success_test(self, 'proposal', 'list')
        self.assertEqual(response['response']['type'], 'Proposals',
            'System proposal list service method failed.')
        self.assertEqual(len(response['response']['content']['proposals']), 1,
            'Failed to return the correct number of proposals.')

    def test_proposal_get_method(self):
        ''' Add one private and one public proposal to the database then query. '''
        slug = 'test-1'
        db_loader.create_proposal(slug=slug)
        response = generic_service_method_success_test(self, 'proposal', 'get', params={'slug':slug})
        self.assertEqual(response['response']['type'], 'Proposal',
            'Proposal get service method failed.')
        self.assertEqual(response['response']['content']['slug'], slug,
            'Proposal get method returned the wrong proposal.')


    def test_proposal_put_method(self):

        ''' Add a proposal through the api and then update it. '''

        slug = 'savetheeverything'
        name_1 = 'Save the Everything!'
        pitch_1 = 'Save all the animals!'
        name_2 = 'Save everything!!'
        pitch_2 = 'Yeah, save all those things.'

        params = {
            'slug': slug,
            'name': name_1,
            'pitch': pitch_1,
            'category': ndb.Key('Category', slug).urlsafe(),
            'creator': ndb.Key('User', 'fakie').urlsafe(),
        }

        response = generic_service_method_success_test(self, 'proposal', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Proposal',
            'Proposal put service method failed to create a new proposal.')
        self.assertEqual(response['response']['content']['name'], name_1,
            'Proposal put failed to set the name.')
        self.assertEqual(response['response']['content']['pitch'], pitch_1,
            'Proposal put failed to set the description.')

        params['name'] = name_2
        params['pitch'] = pitch_2
        params['key'] = slug

        response = generic_service_method_success_test(self, 'proposal', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Proposal',
            'Proposal put service method failed.')
        self.assertEqual(response['response']['content']['name'], name_2,
            'Proposal put failed to change the name.')
        self.assertEqual(response['response']['content']['pitch'], pitch_2,
            'Proposal put failed to change the description.')


class CategoryServiceTestCase(unittest.TestCase):
    ''' Test cases for the category service.
    '''

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_category_list_method(self):

        ''' Add a category to the database then query. '''

        slug = 'test-slug'
        db_loader.create_category(slug=slug)
        response = generic_service_method_success_test(self, 'category', 'list')
        self.assertEqual(response['response']['type'], 'Categories',
            'System category list service method failed.')
        self.assertEqual(len(response['response']['content']['categories']), 1,
            'Failed to return the correct number of categories.')

    def test_category_get_method(self):

        ''' Add a category to the database then query. '''

        category_slug = 'test-slug'
        db_loader.create_category(slug=category_slug)
        response = generic_service_method_success_test(self, 'category', 'get', params={'slug':category_slug})
        self.assertEqual(response['response']['type'], 'Category',
            'Category get service method failed.')
        self.assertEqual(response['response']['content']['slug'], category_slug,
            'Category get method returned the wrong category.')

    def test_category_put_method(self):

        ''' Add a category through the api and then update it. '''

        slug = 'different'
        name_1 = 'Name'
        description_1 = 'Think.'
        name_2 = 'Different Name'
        description_2 = 'Think different.'

        params = {
            'slug': slug,
            'name': name_1,
            'description': description_1,
        }

        response = generic_service_method_success_test(self, 'category', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Category',
            'Category put service method failed to create a new category.')
        self.assertEqual(response['response']['content']['name'], name_1,
            'Category put failed to set the name.')
        self.assertEqual(response['response']['content']['description'], description_1,
            'Category put failed to set the description.')

        params['name'] = name_2
        params['description'] = description_2
        params['key'] = slug

        response = generic_service_method_success_test(self, 'category', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Category',
            'Category put service method failed.')
        self.assertEqual(response['response']['content']['name'], name_2,
            'Category put failed to change the name.')
        self.assertEqual(response['response']['content']['description'], description_2,
            'Category put failed to change the description.')

    def test_category_delete_method(self):

        ''' Add a category and then delete it through the api. '''

        slug = 'test-slug'
        db_loader.create_category(slug=slug)
        params = {
            'slug': slug,
        }
        response = generic_service_method_success_test(self, 'category', 'delete', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'Category put service method failed.')
        self.assertEqual(len(Category.query().fetch(1)), 0, 'Failed to delete category.')
