import time
import datetime

from google.appengine.ext import ndb

from openfire.tests import OFTestCase
from openfire.models.project import Proposal, Goal, Tier, NextStep
import openfire.fixtures.fixture_util as db_loader


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
        db_loader.create_proposal(initial_goal={'amount':100})
        response = self.of_service_test('proposal', 'list')
        self.assertEqual(response['response']['type'], 'Proposals',
            'System proposal list service method failed when adding a goal.')
        self.assertEqual(len(response['response']['content']['proposals']), 2,
            'Failed to return the correct number of proposals when adding a goal.')

    def test_proposal_submitted_method(self):

        ''' Add a proposal to the database then query for submitted proposals. '''

        # Add a blank proposal and make sure it exists.
        proposal_key = db_loader.create_proposal(status='s')
        response = self.of_service_test('proposal', 'submitted')
        self.assertEqual(response['response']['type'], 'Proposals',
            'System proposal submitted service method failed.')
        self.assertEqual(len(response['response']['content']['proposals']), 1,
            'Failed to return the correct number of submitted proposals.')
        self.assertEqual(response['response']['content']['proposals'][0]['key'], proposal_key.urlsafe(),
            'Failed to return the correct submitted proposal.')

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

        user_key = db_loader.create_user()

        '''
        ' Need to learn how to log in during tests. [OF-155]
        login_dict = {
            'username': 'fakie',
            'password': 'fakieiscool'
        }
        self.of_handler_test('/login', is_post=True, post_data=login_dict)
        '''

        name_1 = 'Save the Everything!'
        pitch_1 = 'Save all the animals!'
        name_2 = 'Save everything!!'
        pitch_2 = 'Yeah, save all those things.'

        params = {
            'name': name_1,
            'pitch': pitch_1,
            'category': ndb.Key('Category', 'everything').urlsafe(),
            'creator': user_key.urlsafe(),
            'initial_goal': {
                'amount': 1000,
                'description': 'Save one thing.',
                'funding_day_limit': 100,
                'deliverable_description': 'We will save something',
                'deliverable_date': datetime.datetime.now().isoformat(),
            },
            'future_goal': {
                'summary': 'Save every animal on the planet.',
                'description': 'Use experts and crowd funding to save every animal on the planet.',
            },
            'initial_tiers': [
                {
                    'amount': 10,
                    'name': 'Helper',
                    'description': 'Help out',
                },
                {
                    'amount': 100,
                    'name': 'Better',
                    'description': 'Help out more',
                },
            ],
            'initial_next_steps': [
                {
                    'summary': 'Next step 1',
                    'description': 'Some description',
                },
                {
                    'summary': 'Next step 2',
                    'description': 'Some other description',
                },
            ],
        }

        response = self.of_service_test('proposal', 'put', params=params)
        self.assertEqual(response['response']['type'], 'Proposal',
            'Proposal put service method failed to create a new proposal.')
        self.assertTrue(response['response']['content'].get('name', False),
            'Proposal put failed to set the name value.')
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

    def test_proposal_promote_method(self):

        ''' Add a proposal through the api and then promote it. '''

        user_key = db_loader.create_user()
        proposal_params = {
            'name': 'Save the Everything',
            'pitch': 'Save it. All of it.',
            'category': ndb.Key('Category', 'conservation').urlsafe(),
            'creator': user_key.urlsafe(),
            'initial_goal': {
                'amount': 1000,
                'description': 'Save one thing.',
                'funding_day_limit': 100,
                'deliverable_description': 'We will save something',
                'deliverable_date': datetime.datetime.now().isoformat(),
            },
            'future_goal': {
                'summary': 'Save every animal on the planet.',
                'description': 'Use experts and crowd funding to save every animal on the planet.',
            },
            'initial_tiers': [
                {
                    'amount': 10,
                    'name': 'Helper',
                    'description': 'Help out',
                },
                {
                    'amount': 100,
                    'name': 'Better',
                    'description': 'Help out more',
                },
            ],
            'initial_next_steps': [
                {
                    'summary': 'Next step 1',
                    'description': 'Some description',
                },
                {
                    'summary': 'Next step 2',
                    'description': 'Some other description',
                },
            ],
        }

        response = self.of_service_test('proposal', 'put', params=proposal_params)
        self.assertEqual(response['response']['type'], 'Proposal',
            'Failed to put proposal when testing promote proposal.')
        proposal_key = response['response']['content']['key']
        self.assertTrue(proposal_key, 'Failed to return a new proposal when testing promote proposal.')

        promote_params = {'key': proposal_key}
        response = self.of_service_test('proposal', 'promote', params=promote_params)
        self.assertEqual(response['response']['type'], 'Project',
            'Proposal get service method failed.')
        content = response['response']['content']
        self.assertTrue(content['active_goal'], 'Failed to set active goal on promote.')
        goal = ndb.Key(urlsafe=content['active_goal']).get()
        self.assertTrue(goal, 'Failed to set valid active goal on promote.')
        self.assertEqual(len(goal.tiers), 2, 'Failed to set active goal tiers on promote.')
        self.assertEqual(len(goal.next_steps), 2, 'Failed to set active goal next steps on promote.')
        self.assertTrue(content['future_goal'], 'Failed to set future goal on promote.')
        future_goal = ndb.Key(urlsafe=content['future_goal']).get()
        self.assertTrue(future_goal, 'Failed to set valid future goal on promote.')

    def test_proposal_suspend_method(self):

        ''' Add one proposal to the database then suspend it. '''

        proposal_key = db_loader.create_proposal()
        key = proposal_key.urlsafe()
        response = self.of_service_test('proposal', 'suspend', params={'key':self.encrypt(key)})
        self.assertEqual(response['response']['type'], 'Echo',
            'Proposal suspend service method failed.')
        self.assertEqual(proposal_key.get().status, 'p',
            'Proposal suspend method did not suspend proposal.')

    def test_proposal_reject_method(self):

        ''' Add one proposal to the database then reject it. '''

        proposal_key = db_loader.create_proposal()
        key = proposal_key.urlsafe()
        response = self.of_service_test('proposal', 'reject', params={'key':self.encrypt(key)})
        self.assertEqual(response['response']['type'], 'Echo',
            'Proposal reject service method failed.')
        self.assertEqual(proposal_key.get().status, 'd',
            'Proposal reject method did not reject proposal.')

    def test_proposal_reopen_method(self):

        ''' Add one proposal to the database then reopen it. '''

        proposal_key = db_loader.create_proposal(status='p')
        key = proposal_key.urlsafe()
        response = self.of_service_test('proposal', 'reopen', params={'key':self.encrypt(key)})
        self.assertEqual(response['response']['type'], 'Proposal',
            'Proposal reopen service method failed.')
        self.assertEqual(proposal_key.get().status, 'f',
            'Proposal reopen method did not reopen proposal.')

    def test_proposal_add_viewer_method(self):

        ''' Add one proposal to the database then add a viewer to it. '''

        proposal_key = db_loader.create_proposal(status='p')
        user_key = db_loader.create_user()
        params = {'user': user_key.urlsafe(), 'target': proposal_key.urlsafe()}
        response = self.of_service_test('proposal', 'add_viewer', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'Proposal add viewer service method failed.')
        self.assertEqual(len(proposal_key.get().viewers), 1,
            'Proposal add viewer method did not add one viewer.')
        self.assertEqual(proposal_key.get().viewers[0], user_key,
            'Proposal add viewer method did not add correct viewer.')

    def test_proposal_remove_viewer_method(self):

        ''' Add one proposal to the database with a viewer then remove the viewer. '''

        user_key = db_loader.create_user()
        proposal_key = db_loader.create_proposal(status='p', viewers_keys=[user_key])
        params = {'user': user_key.urlsafe(), 'target': proposal_key.urlsafe()}
        response = self.of_service_test('proposal', 'remove_viewer', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'Proposal remove viewer service method failed.')
        self.assertEqual(len(proposal_key.get().viewers), 0,
            'Proposal remove viewer method did not remove one viewer.')
