# -*- coding: utf-8 -*-
"""
Service tests.
"""

from google.appengine.ext import testbed, ndb, blobstore

from openfire.tests import OFTestCase
from openfire.models.user import Topic
from openfire.models.assets import CustomURL
from openfire.models.project import Category, Goal, Tier
import openfire.fixtures.fixture_util as db_loader


class SystemServiceTestCase(OFTestCase):

    ''' Test cases for user services. '''

    def test_echo_service_method(self):

        ''' Test an echo message. '''

        message_content = 'TESTING'
        echoParams = {'message': message_content}
        response = self.of_service_test('system', 'echo', params=echoParams)
        self.assertEqual(response['response']['content']['message'], message_content, 'System echo service method failed.')

    def test_hello_service_method(self):

        ''' Test the hello message. '''

        response = self.of_service_test('system', 'hello')
        self.assertTrue(response['response']['content']['message'].startswith('Hello'), 'System hello service failed.')


class ProjectServiceTestCase(OFTestCase):

    ''' Test cases for the project service. '''

    def test_project_list_method(self):

        ''' Add one private and one public project to the database then query. '''

        db_loader.create_project(status='p')
        project_key = db_loader.create_project()
        db_loader.create_tier(parent_key=project_key, name='test name')
        db_loader.create_goal(parent_key=project_key, amount=100)
        response = self.of_service_test('project', 'list')
        self.assertEqual(response['response']['type'], 'Projects',
            'System project list service method failed.')
        self.assertEqual(len(response['response']['content']['projects']), 1,
            'Failed to return the correct number of projects.')

    def test_project_get_method(self):

        ''' Add one private and one public project to the database then query. '''

        project_key = db_loader.create_project()
        key = project_key.urlsafe()
        response = self.of_service_test('project', 'get', params={'key':key})
        self.assertEqual(response['response']['type'], 'Project',
            'Project get service method failed.')
        self.assertEqual(response['response']['content']['key'], key,
            'Project get method returned the wrong project.')

    def test_project_put_method(self):

        ''' Add a project (not through api) and then update it. '''

        proposal_key = ndb.Key('Proposal', 'fake')
        category_key = ndb.Key('Category', 'everything')
        creator_key = ndb.Key('User', 'fakie')
        name_1 = 'Save the Everything!'
        pitch_1 = 'Save all the animals!'
        name_2 = 'Save everything!!'
        pitch_2 = 'Yeah, save all those things.'

        project_key = db_loader.create_project(name=name_1, pitch=pitch_1,
                    proposal_key=proposal_key, category_key=category_key, creator_key=creator_key)

        params = {
            'key': project_key.urlsafe(),
            'name': name_2,
            'pitch': pitch_2,
        }

        response = self.of_service_test('project', 'put', params=params)
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
        response = self.of_service_test('project', 'comment', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_comments_method(self):
        ''' Test something. '''
        response = self.of_service_test('project', 'comments', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_post_method(self):
        ''' Test something. '''
        response = self.of_service_test('project', 'post', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_posts_method(self):
        ''' Test something. '''
        response = self.of_service_test('project', 'posts', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_media_method(self):
        ''' Test something. '''
        response = self.of_service_test('project', 'media', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_add_media_method(self):
        ''' Test something. '''
        response = self.of_service_test('project', 'add_medai', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_follow_method(self):
        ''' Test something. '''
        response = self.of_service_test('project', 'follow', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_followers_method(self):
        ''' Test something. '''
        response = self.of_service_test('project', 'followers', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_backers_method(self):
        ''' Test something. '''
        response = self.of_service_test('project', 'backers', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_back_method(self):
        ''' Test something. '''
        response = self.of_service_test('project', 'back', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_suspend_method(self):
        ''' Test something. '''
        response = self.of_service_test('project', 'suspend', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')

    def test_project_shutdown_method(self):
        ''' Test something. '''
        response = self.of_service_test('project', 'shutdown', params={})
        self.assertEqual(response['response']['type'], '',
            'Project  service method failed.')
    """


    #############################################
    # Project Goal Tests.
    #############################################

    def test_project_get_goal_method(self):

        ''' Add a project and a goal then query for it. '''

        project_key = db_loader.create_project()
        goal_key = db_loader.create_goal(parent_key=project_key).key
        params = {'key': self.encrypt(goal_key.urlsafe())}
        response = self.of_service_test('project', 'get_goal', params=params)
        self.assertEqual(response['response']['type'], 'Goal',
            'System project get goal service method failed.')
        self.assertEqual(response['response']['content']['key'], goal_key.urlsafe(),
            'Failed to return the correct project goal.')

    def test_project_list_goals_method(self):

        ''' Add a project and a few goals then query for them. '''

        project_key = db_loader.create_project()
        db_loader.create_goal(parent_key=project_key)
        db_loader.create_goal(parent_key=project_key)
        db_loader.create_goal(parent_key=project_key)
        params = {'project': self.encrypt(project_key.urlsafe())}
        response = self.of_service_test('project', 'list_goals', params=params)
        self.assertEqual(response['response']['type'], 'Goals',
            'Project list goals service method failed.')
        self.assertEqual(len(response['response']['content']['goals']), 3,
            'Project list goals returned the wrong number of goals.')

    def test_project_put_goal_method(self):

        ''' Add a project through the api and then edit it. '''

        description_1 = 'TEST DESCRIPTION'
        description_2 = 'SOMETHING NEW'

        project_key = db_loader.create_project()
        contribution_type_key = db_loader.create_contribution_type()
        goal_dict = {
            'target': project_key.urlsafe(),
            'contribution_type': contribution_type_key.urlsafe(),
            'amount': 1000,
            'description': description_1,
            'backer_count': 0,
            'progress': 23,
            'met': False,
        }

        self.assertEqual(len(Goal.query().fetch()), 0, 'Goals existed before put test.')

        response = self.of_service_test('project', 'put_goal', params=goal_dict)

        self.assertEqual(response['response']['type'], 'Goal', 'Project list goals service method failed.')
        goals = Goal.query().fetch()
        self.assertEqual(len(goals), 1, 'Failed to actually put goal.')
        self.assertEqual(goals[0].description, description_1, 'Failed to save goal description.')

        goal_key = response['response']['content']['key']
        goal_dict['key'] = goal_key
        goal_dict['description'] = description_2

        change_dict = {
            'key': goal_key,
            'target': project_key.urlsafe(),
            'description': description_2,
        }

        response = self.of_service_test('project', 'put_goal', params=change_dict)

        self.assertEqual(response['response']['type'], 'Goal', 'Project list goals service method failed.')
        goals = Goal.query().fetch()
        self.assertEqual(len(goals), 1, 'Failure. Put another goal instead of editing existing one.')
        self.assertEqual(goals[0].description, description_2, 'Failed to update goal description.')


    def test_project_delete_goal_method(self):

        ''' Add a project and a goal then delete it. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)
        self.assertTrue(goal, 'Failed to init project goal object for delete test.')

        params = {'key': self.encrypt(goal.key.urlsafe())}
        response = self.of_service_test('project', 'delete_goal', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'System project get goal service method failed.')
        goal = goal.key.get()
        self.assertFalse(goal, 'Failed to delete project goal.')


    #############################################
    # Project Tier Tests.
    #############################################

    def test_project_get_tier_method(self):

        ''' Add a project and a tier then query for it. '''

        project_key = db_loader.create_project()
        tier_key = db_loader.create_tier(parent_key=project_key).key
        params = {'key': self.encrypt(tier_key.urlsafe())}
        response = self.of_service_test('project', 'get_tier', params=params)
        self.assertEqual(response['response']['type'], 'Tier',
            'System project get tier service method failed.')
        self.assertEqual(response['response']['content']['key'], tier_key.urlsafe(),
            'Failed to return the correct project tier.')

    def test_project_list_tiers_method(self):

        ''' Add a project and a few tiers then query for them. '''

        project_key = db_loader.create_project()
        db_loader.create_tier(parent_key=project_key)
        db_loader.create_tier(parent_key=project_key)
        db_loader.create_tier(parent_key=project_key)
        params = {'project': self.encrypt(project_key.urlsafe())}
        response = self.of_service_test('project', 'list_tiers', params=params)
        self.assertEqual(response['response']['type'], 'Tiers',
            'Project list tiers service method failed.')
        self.assertEqual(len(response['response']['content']['tiers']), 3,
            'Project list tiers returned the wrong number of tiers.')

    def test_project_put_tier_method(self):

        ''' Add a project through the api and then edit it. '''

        description_1 = 'TEST DESCRIPTION'
        description_2 = 'SOMETHING NEW'

        project_key = db_loader.create_project()
        contribution_type_key = db_loader.create_contribution_type()
        tier_dict = {
            'target': project_key.urlsafe(),
            'name': 'NAME',
            'contribution_type': contribution_type_key.urlsafe(),
            'amount': 1000,
            'description': description_1,
            'delivery': '02-12-2013',
            'backer_count': 23,
            'backer_limit': 100,
        }

        self.assertEqual(len(Tier.query().fetch()), 0, 'Tiers existed before put test.')

        response = self.of_service_test('project', 'put_tier', params=tier_dict)

        self.assertEqual(response['response']['type'], 'Tier', 'Project list tiers service method failed.')
        tiers = Tier.query().fetch()
        self.assertEqual(len(tiers), 1, 'Failed to actually put tier.')
        self.assertEqual(tiers[0].description, description_1, 'Failed to save tier description.')

        tier_key = response['response']['content']['key']

        change_dict = {
            'key': tier_key,
            'target': project_key.urlsafe(),
            'description': description_2,
            'delivery': 'YESTERDAY',
        }

        response = self.of_service_test('project', 'put_tier', params=change_dict)

        self.assertEqual(response['response']['type'], 'Tier', 'Project list tiers service method failed.')
        tiers = Tier.query().fetch()
        self.assertEqual(len(tiers), 1, 'Failure. Put another tier instead of editing existing one.')
        self.assertEqual(tiers[0].description, description_2, 'Failed to update tier description.')
        self.assertEqual(tiers[0].delivery, 'YESTERDAY', 'Failed to update tier delivery.')

    def test_project_delete_tier_method(self):

        ''' Add a project and a tier then delete it. '''

        project_key = db_loader.create_project()
        tier_key = db_loader.create_tier(parent_key=project_key).key
        self.assertTrue(tier_key.get(), 'Failed to init project tier object for delete test.')

        params = {'key': self.encrypt(tier_key.urlsafe())}
        response = self.of_service_test('project', 'delete_tier', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'System project get tier service method failed.')
        self.assertFalse(tier_key.get(), 'Failed to delete project tier.')


class ProposalServiceTestCase(OFTestCase):

    ''' Test cases for the proposal service. '''

    def test_proposal_list_method(self):

        ''' Add a proposal to the database then query. '''

        # Add a blank proposal and make sure it exists.
        db_loader.create_proposal()
        response = self.of_service_test('proposal', 'list')
        self.assertEqual(response['response']['type'], 'Proposals',
            'System proposal list service method failed.')
        self.assertEqual(len(response['response']['content']['proposals']), 1,
            'Failed to return the correct number of proposals.')

        # Add a proposal with a goal and make sure it still works.
        db_loader.create_proposal(goals=[{'amount':100}])
        response = self.of_service_test('proposal', 'list')
        self.assertEqual(response['response']['type'], 'Proposals',
            'System proposal list service method failed when adding a goal.')
        self.assertEqual(len(response['response']['content']['proposals']), 2,
            'Failed to return the correct number of proposals when adding a goal.')

        # Add a proposal with a tier and make sure it still works.
        db_loader.create_proposal(tiers=[{'name':'some tier'}])
        response = self.of_service_test('proposal', 'list')
        self.assertEqual(response['response']['type'], 'Proposals',
            'System proposal list service method failed when adding a tier.')
        self.assertEqual(len(response['response']['content']['proposals']), 3,
            'Failed to return the correct number of proposals when adding a tier.')


    def test_proposal_get_method(self):

        ''' Add one private and one public proposal to the database then query. '''

        proposal_key = db_loader.create_proposal()
        key = proposal_key.urlsafe()
        response = self.of_service_test('proposal', 'get', params={'key':self.encrypt(key)})
        self.assertEqual(response['response']['type'], 'Proposal',
            'Proposal get service method failed.')
        self.assertEqual(response['response']['content']['key'], key,
            'Proposal get method returned the wrong proposal.')


    def test_proposal_put_method(self):

        ''' Add a proposal through the api and then update it. '''

        name_1 = 'Save the Everything!'
        pitch_1 = 'Save all the animals!'
        name_2 = 'Save everything!!'
        pitch_2 = 'Yeah, save all those things.'

        params = {
            'name': name_1,
            'pitch': pitch_1,
            'category': ndb.Key('Category', 'everything').urlsafe(),
            'creator': ndb.Key('User', 'fakie').urlsafe(),
        }

        response = self.of_service_test('proposal', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Proposal',
            'Proposal put service method failed to create a new proposal.')
        self.assertEqual(response['response']['content']['name'], name_1,
            'Proposal put failed to set the name.')
        self.assertEqual(response['response']['content']['pitch'], pitch_1,
            'Proposal put failed to set the description.')

        params['name'] = name_2
        params['pitch'] = pitch_2
        params['key'] = self.encrypt(response['response']['content']['key'])

        response = self.of_service_test('proposal', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Proposal',
            'Proposal put service method failed.')
        self.assertEqual(response['response']['content']['name'], name_2,
            'Proposal put failed to change the name.')
        self.assertEqual(response['response']['content']['pitch'], pitch_2,
            'Proposal put failed to change the description.')


class CategoryServiceTestCase(OFTestCase):

    ''' Test cases for the category service. '''

    def test_category_list_method(self):

        ''' Add a category to the database then query. '''

        slug = 'test-slug'
        db_loader.create_category(slug=slug)
        response = self.of_service_test('category', 'list')
        self.assertEqual(response['response']['type'], 'Categories',
            'System category list service method failed.')
        self.assertEqual(len(response['response']['content']['categories']), 1,
            'Failed to return the correct number of categories.')

    def test_category_get_method(self):

        ''' Add a category to the database then query. '''

        category_slug = 'test-slug'
        db_loader.create_category(slug=category_slug)
        response = self.of_service_test('category', 'get', params={'slug':category_slug})
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

        response = self.of_service_test('category', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Category',
            'Category put service method failed to create a new category.')
        self.assertEqual(response['response']['content']['name'], name_1,
            'Category put failed to set the name.')
        self.assertEqual(response['response']['content']['description'], description_1,
            'Category put failed to set the description.')

        params['name'] = name_2
        params['description'] = description_2
        params['key'] = self.encrypt(response['response']['content']['key'])

        response = self.of_service_test('category', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Category',
            'Category put service method failed.')
        self.assertEqual(response['response']['content']['name'], name_2,
            'Category put failed to change the name.')
        self.assertEqual(response['response']['content']['description'], description_2,
            'Category put failed to change the description.')

    def test_category_delete_method(self):

        ''' Add a category and then delete it through the api. '''

        slug = 'test-slug'
        category_key = db_loader.create_category(slug=slug)
        params = {
            'key': self.encrypt(category_key.urlsafe()),
        }
        response = self.of_service_test('category', 'delete', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'Category put service method failed.')
        self.assertEqual(len(Category.query().fetch(1)), 0, 'Failed to delete category.')


class CustomUrlServiceTestCase(OFTestCase):

    ''' Test cases for the custom_url service. '''

    def test_custom_url_list_method(self):

        ''' Add a custom_url to the database then query. '''

        slug = 'test-slug'
        target_key = db_loader.create_project()
        db_loader.create_custom_url(slug=slug, target_key=target_key)
        response = self.of_service_test('url', 'list')
        self.assertEqual(response['response']['type'], 'CustomUrls',
            'System custom_url list service method failed.')
        self.assertEqual(len(response['response']['content']['urls']), 1,
            'Failed to return the correct number of urls.')

    def test_custom_url_get_method(self):

        ''' Add a custom_url to the database then query. '''

        custom_url_slug = 'test-slug'
        target_key = db_loader.create_project()
        db_loader.create_custom_url(slug=custom_url_slug, target_key=target_key)
        response = self.of_service_test('url', 'get', params={'slug':custom_url_slug})
        self.assertEqual(response['response']['type'], 'CustomUrl',
            'CustomUrl get service method failed.')
        self.assertEqual(response['response']['content']['slug'], custom_url_slug,
            'CustomUrl get method returned the wrong custom url.')

    def test_custom_url_put_method(self):

        ''' Add a custom url through the api and then try again to get an error. '''

        target = db_loader.create_project()
        params = {
            'slug': 'test',
            'target': self.encrypt(target.urlsafe()),
        }

        response = self.of_service_test('url', 'put', params=params)
        self.assertEqual(response['response']['type'], 'CustomUrl',
            'CustomUrl put service method failed to create a new custom_url.')
        self.assertEqual(target.get().customurl.urlsafe(), response['response']['content']['key'],
            'Failed to set custom url on target during put.')

        response = self.of_service_test('url', 'put', params=params, should_fail=True)
        self.assertEqual(response['response']['content']['state'], 'APPLICATION_ERROR', 'Allowed overwriting of a custom url.')

    def test_custom_url_delete_method(self):

        ''' Add a custom_url and then delete it through the api. '''

        target_key = db_loader.create_project()
        custom_url_key = db_loader.create_custom_url(slug='test-slug', target_key=target_key)
        params = {
            'key': self.encrypt(custom_url_key.urlsafe()),
        }
        response = self.of_service_test('url', 'delete', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'CustomUrl delete service method failed.')
        self.assertEqual(len(CustomURL.query().fetch(1)), 0, 'Failed to delete custom url.')

    def test_custom_url_check_method(self):

        ''' Add a custom_url and then check availability. '''

        slug = 'test-slug'
        target_key = db_loader.create_project()
        params = {'slug': slug}
        response = self.of_service_test('url', 'check', params=params)
        self.assertEqual(response['response']['type'], 'CustomUrlCheck',
            'CustomUrl check service method failed.')
        self.assertEqual(response['response']['content']['taken'], False, 'Custom url is taken that was never assigned.')

        db_loader.create_custom_url(slug=slug, target_key=target_key)
        response = self.of_service_test('url', 'check', params=params)
        self.assertEqual(response['response']['content']['taken'], True, 'Custom url is not taken that was assigned.')


class MediaServiceTestCase(OFTestCase):

    ''' Test cases for the media service. '''

    def setUp(self):
        # This needs to be run with the normal testbed.
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_blobstore_stub()
        self.testbed.init_images_stub()
        self.testbed.init_urlfetch_stub()

        blobstub = self.testbed.get_stub(testbed.BLOBSTORE_SERVICE_NAME)
        blobstub.CreateBlob('blob', 'blobdata')
        self.blob_key = blobstore.BlobKey('blob')

    def test_media_generate_endpoint_method(self):

        ''' Add a custom_url to the database then query. '''

        response = self.of_service_test('media', 'generate_endpoint')
        self.assertEqual(response['response']['type'], 'Endpoint',
            'Failed to return a endpoint message type.')

        upload_url = response['response']['content']['endpoints'][0]
        self.assertTrue(upload_url, 'Failed to generate a media upload url.')


class TopicServiceTestCase(OFTestCase):

    ''' Test cases for the topic service. '''

    def test_topic_list_method(self):

        ''' Add a topic to the database then query. '''

        slug = 'test-slug'
        db_loader.create_topic(slug=slug)
        response = self.of_service_test('topic', 'list')
        self.assertEqual(response['response']['type'], 'Topics',
            'System topic list service method failed.')
        self.assertEqual(len(response['response']['content']['topics']), 1,
            'Failed to return the correct number of topics.')

    def test_topic_get_method(self):

        ''' Add a topic to the database then query. '''

        topic_slug = 'test-slug'
        db_loader.create_topic(slug=topic_slug)
        response = self.of_service_test('topic', 'get', params={'slug':topic_slug})
        self.assertEqual(response['response']['type'], 'Topic',
            'Topic get service method failed.')
        self.assertEqual(response['response']['content']['slug'], topic_slug,
            'Topic get method returned the wrong topic.')

    def test_topic_put_method(self):

        ''' Add a topic through the api and then update it. '''

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

        response = self.of_service_test('topic', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Topic',
            'Topic put service method failed to create a new topic.')
        self.assertEqual(response['response']['content']['name'], name_1,
            'Topic put failed to set the name.')
        self.assertEqual(response['response']['content']['description'], description_1,
            'Topic put failed to set the description.')

        params['name'] = name_2
        params['description'] = description_2
        params['key'] = self.encrypt(response['response']['content']['key'])

        response = self.of_service_test('topic', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Topic',
            'Topic put service method failed.')
        self.assertEqual(response['response']['content']['name'], name_2,
            'Topic put failed to change the name.')
        self.assertEqual(response['response']['content']['description'], description_2,
            'Topic put failed to change the description.')

    def test_topic_delete_method(self):

        ''' Add a topic and then delete it through the api. '''

        slug = 'test-slug'
        topic_key = db_loader.create_topic(slug=slug)
        params = {
            'key': self.encrypt(topic_key.urlsafe()),
        }
        response = self.of_service_test('topic', 'delete', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'Topic put service method failed.')
        self.assertEqual(len(Topic.query().fetch(1)), 0, 'Failed to delete topic.')


class UserServiceTestCase(OFTestCase):

    ''' Test cases for the user service. '''

    def test_user_profile_method(self):

        ''' Test the user profile service method. '''

        topic1_key = db_loader.create_topic(slug='topic1')
        topic2_key = db_loader.create_topic(slug='topic2')
        user_key = db_loader.create_user(email=['fakie@mcfakerton.com'], topics=[topic1_key, topic2_key])
        user = user_key.get()
        params = {
            'user': user.username
        }

        # Test profile get.
        response = self.of_service_test('user', 'profile', params=params)
        self.assertEqual(response['response']['type'], 'Profile',
            'Failed to return profile response from user profile service.')
        content = response['response']['content']
        self.assertEqual(content['username'], user.username,
                'Failed to return the correct username in the profile content service.')
        self.assertEqual(content['firstname'], user.firstname,
                'Failed to return the correct firstname in the profile content service.')
        self.assertEqual(content['lastname'], user.lastname,
                'Failed to return the correct lastname in the profile content service.')
        self.assertEqual(content['bio'], user.bio,
                'Failed to return the correct bio in the profile content service.')
        self.assertEqual(len(content['email']), 1,
                'Failed to return the correct number of emails in the profile content service.')
        self.assertEqual(len(content['topics']), 2,
                'Failed to return the correct number of topics in the profile content service.')

        # Test profile update of bio and location fields.
        params['profile'] = {
            'bio': 'Some new bio',
            'location': 'Some new location',
        }
        response = self.of_service_test('user', 'profile', params=params)
        self.assertEqual(response['response']['type'], 'Profile',
            'Failed to return profile response from user profile service.')

        # Make sure the response was correct.
        content = response['response']['content']
        self.assertEqual(content['username'], params['user'],
                'Failed to return the correct username when updating user profile via service.')

        # Make sure the user was updated.
        user = user_key.get()
        self.assertEqual(user.bio, params['profile']['bio'],
                'Failed to update the user bio via the user profile service.')
        self.assertEqual(user.location, params['profile']['location'],
                'Failed to update the user location via the user profile service.')

        # Make sure the response was correct.
        self.assertEqual(content['bio'], user.bio,
                'Failed to return the correct bio when updating user profile via service.')
        self.assertEqual(content['location'], user.location,
                'Failed to return the correct location when updating user profile via service.')

        # Make sure you cannot update username or firstname.
        params['profile'] = {
            'username': 'NONONO',
            'firstname': 'NONONO',
            'lastname': 'NONONO',
        }
        response = self.of_service_test('user', 'profile', params=params)
        self.assertEqual(response['response']['type'], 'Profile',
            'Failed to return profile response from user profile service.')

        # Make sure things did not change.
        user = user_key.get()
        self.assertNotEqual(params['profile']['username'], user.username,
                'Should not be able to update username via the user profile service.')
        self.assertNotEqual(params['profile']['firstname'], user.firstname,
                'Should not be able to update firstname via the user profile service.')
        self.assertNotEqual(params['profile']['lastname'], user.lastname,
                'Should not be able to update lastname via the user profile service.')


    def test_user_set_topics_method(self):

        ''' Test the user set_topics service method. '''

        user_key = db_loader.create_user()
        user = user_key.get()
        params = {
            'user': user.username
        }

        topic1_key = db_loader.create_topic(slug='topic1')
        topic2_key = db_loader.create_topic(slug='topic2')
        topic3_key = db_loader.create_topic(slug='topic3')
        params = {
            'user': user.username,
            'topics': [],
        }

        # Test setting a single topic.
        params['topics'] = [topic1_key.urlsafe()]
        response = self.of_service_test('user', 'set_topics', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
                'Failed to return echo response from user set_topics service.')

        # Make sure the topic was set.
        user = user_key.get()
        self.assertEqual(len(user.topics), 1,
                'Failed to set a topic for a user using the set_topic service')
        self.assertEqual(user.topics[0], topic1_key,
                'Failed to set the correct topic for a user using the set_topic service')

        # Test setting multiple topics.
        params['topics'] = [topic1_key.urlsafe(), topic2_key.urlsafe(), topic3_key.urlsafe()]
        response = self.of_service_test('user', 'set_topics', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
                'Failed to return echo response from user set_topics service.')

        # Make sure the topics were set in order.
        user = user_key.get()
        self.assertEqual(len(user.topics), 3,
                'Failed to set topics for a user using the set_topic service')
        self.assertEqual(user.topics[0], topic1_key,
                'Failed to set correct topic order for a user using the set_topic service')
        self.assertEqual(user.topics[1], topic2_key,
                'Failed to set correct topic order for a user using the set_topic service')
        self.assertEqual(user.topics[2], topic3_key,
                'Failed to set correct topic order for a user using the set_topic service')

        # Test setting topics to none.
        params['topics'] = None
        response = self.of_service_test('user', 'set_topics', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
                'Failed to return echo response from user set_topics service.')

        # Make sure the topics were reset.
        user = user_key.get()
        self.assertEqual(len(user.topics), 0,
                'Failed to set topics to none for a user using the set_topic service')

        # Test setting multiple topics to test order.
        params['topics'] = [topic3_key.urlsafe(), topic2_key.urlsafe(), topic1_key.urlsafe()]
        response = self.of_service_test('user', 'set_topics', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
                'Failed to return echo response from user set_topics service.')

        # Make sure the topics were set in order.
        user = user_key.get()
        self.assertEqual(len(user.topics), 3,
                'Failed to set topics for a user using the set_topic service')
        self.assertEqual(user.topics[0], topic3_key,
                'Failed to set correct topic order for a user using the set_topic service')
        self.assertEqual(user.topics[1], topic2_key,
                'Failed to set correct topic order for a user using the set_topic service')
        self.assertEqual(user.topics[2], topic1_key,
                'Failed to set correct topic order for a user using the set_topic service')


    def test_user_account_method(self):

        ''' Test the user account service method. '''

        user_key = db_loader.create_user()
        user = user_key.get()
        params = {
            'user': user.username
        }
        response = self.of_service_test('user', 'account', params=params)
        self.assertEqual(response['response']['type'], 'Account',
            'Failed to return account response from user account service.')
        #content = response['response']['content']


    def test_user_follow_method(self):

        ''' Test the user follow service method. '''

        user_key = db_loader.create_user()
        user = user_key.get()
        params = {
            'user': user.username
        }
        response = self.of_service_test('user', 'follow', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'Failed to return echo response from user follow service.')
        #content = response['response']['content']


    def test_user_followers_method(self):

        ''' Test the user followers service method. '''

        user_key = db_loader.create_user()
        user = user_key.get()
        params = {
            'user': user.username
        }
        response = self.of_service_test('user', 'followers', params=params)
        self.assertEqual(response['response']['type'], 'FollowersResponse',
            'Failed to return followers response from user followers service.')
        #content = response['response']['content']


class SearchServiceTestCase(OFTestCase):

    ''' Test cases for the search service. '''

    def test_search_autocomplete_method(self):

        ''' Add a topic to the database then query through the auto complete service. '''

        slug = 'test'
        db_loader.create_topic(slug=slug)
        params = {
            'query': slug,
            'index': 'topic',
        }
        response = self.of_service_test('search', 'autocomplete', params=params)
        self.assertEqual(response['response']['type'], 'SearchResponse',
            'Search autocomplete service method failed to return proper response.')
        self.assertEqual(len(response['response']['content']['ids']), 1,
            'Failed to return the correct number of topics through autocomplete.')
        self.assertEqual(response['response']['content']['ids'][0], slug,
            'Failed to return the correct topic id through autocomplete.')

    def test_search_topic_autocomplete_method(self):

        ''' Add a topic to the database then query through the topic auto complete service. '''

        slug = 'test'
        topic_key = db_loader.create_topic(slug=slug)
        params = {
            'query': slug,
        }

        # Test a positive response.
        response = self.of_service_test('search', 'topic_autocomplete', params=params)
        self.assertEqual(response['response']['type'], 'Topics',
            'Topic autocomplete service method failed to return proper response.')
        self.assertEqual(len(response['response']['content']['topics']), 1,
            'Failed to return the correct number of topics through topic autocomplete.')
        self.assertEqual(response['response']['content']['topics'][0]['key'], topic_key.urlsafe(),
            'Failed to return the correct topic key through autocomplete.')
        self.assertEqual(response['response']['content']['topics'][0]['slug'], slug,
            'Failed to return the correct topic slug through autocomplete.')

        # Test a negative response.
        params['query'] = 'NOWAY'
        response = self.of_service_test('search', 'topic_autocomplete', params=params)
        self.assertEqual(response['response']['type'], 'Topics',
            'Topic autocomplete service method failed to return proper response.')
        self.assertEqual(len(response['response']['content']), 0,
            'Failed to return the correct number of topics (0) through topic autocomplete.')
