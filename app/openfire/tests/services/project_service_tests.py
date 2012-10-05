import time
import datetime

from google.appengine.ext import ndb

from openfire.tests import OFTestCase
from openfire.models.project import Goal, Tier, NextStep
import openfire.fixtures.fixture_util as db_loader


class ProjectServiceTestCase(OFTestCase):

    ''' Test cases for the project service. '''

    def test_project_list_method(self):

        ''' Add one private and one public project to the database then query. '''

        db_loader.create_project(status='p')
        db_loader.create_project()
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

        user_key = db_loader.create_user()
        proposal_key = ndb.Key('Proposal', 'fake')
        category_key = ndb.Key('Category', 'everything')
        creator_key = user_key
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

    def test_project_go_live_method(self):

        ''' Add a project to the database then make it go live. '''

        project_key = db_loader.create_project(status='p')
        response = self.of_service_test('project', 'go_live', params={'key':project_key.urlsafe()})
        self.assertEqual(response['response']['type'], 'Echo',
            'Project go live service method failed.')
        self.assertEqual(project_key.get().status, 'o',
            'Project go live method did not set the project as live.')

    def test_project_suspend_method(self):

        ''' Add a project to the database then make it suspend. '''

        project_key = db_loader.create_project(status='o')
        response = self.of_service_test('project', 'suspend', params={'key':project_key.urlsafe()})
        self.assertEqual(response['response']['type'], 'Echo',
            'Project suspend service method failed.')
        self.assertEqual(project_key.get().status, 's',
            'Project suspend method did not set the project as suspended.')

    def test_project_shutdown_method(self):

        ''' Add a project to the database then make it shutdown. '''

        project_key = db_loader.create_project(status='o')
        response = self.of_service_test('project', 'shutdown', params={'key':project_key.urlsafe()})
        self.assertEqual(response['response']['type'], 'Echo',
            'Project shutdown service method failed.')
        self.assertEqual(project_key.get().status, 'c',
            'Project shutdown method did not set the project as shut down.')

    def test_project_cancel_method(self):

        ''' Add a project to the database then make it cancel. '''

        project_key = db_loader.create_project(status='o')
        response = self.of_service_test('project', 'cancel', params={'key':project_key.urlsafe()})
        self.assertEqual(response['response']['type'], 'Echo',
            'Project cancel service method failed.')
        self.assertEqual(project_key.get().status, 'x',
            'Project cancel method did not set the project as canceled.')



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

    def test_project_active_goal_method(self):

        ''' Add a project and a goal then query for it. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)
        params = {'project': self.encrypt(project_key.urlsafe())}
        response = self.of_service_test('project', 'active_goal', params=params)
        self.assertEqual(response['response']['type'], 'Goal',
            'System project get goal service method failed.')
        self.assertEqual(response['response']['content']['key'], goal.key.urlsafe(),
            'Failed to return the correct project goal.')

    def test_project_completed_goals_method(self):

        ''' Add a project and a few completed goals and one active goal and then query. '''

        project_key = db_loader.create_project()
        db_loader.create_goal(parent_key=project_key)
        db_loader.create_goal(parent_key=project_key, met=True)
        db_loader.create_goal(parent_key=project_key, met=True)
        db_loader.create_goal(parent_key=project_key, met=True)
        params = {'project': self.encrypt(project_key.urlsafe())}
        response = self.of_service_test('project', 'completed_goals', params=params)
        self.assertEqual(response['response']['type'], 'Goals',
            'Project list goals service method failed.')
        self.assertEqual(len(response['response']['content']['goals']), 3,
            'Project list goals returned the wrong number of completed goals.')

    def test_project_future_goal_method(self):

        ''' Add a project and a future goal then query for it. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_future_goal(parent_key=project_key)
        params = {'project': self.encrypt(project_key.urlsafe())}
        response = self.of_service_test('project', 'future_goal', params=params)
        self.assertEqual(response['response']['type'], 'FutureGoal',
            'System project get goal service method failed.')
        self.assertEqual(response['response']['content']['key'], goal.key.urlsafe(),
            'Failed to return the correct project goal.')

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

    def test_project_put_future_goal_method(self):

        ''' Add a future goal and then edit it. '''

        summary_1 = 'TEST SUMMARY'
        summary_2 = 'NEW SUMMARY'
        description_1 = 'TEST DESCRIPTION'
        description_2 = 'SOMETHING NEW'

        project_key = db_loader.create_project()
        future_goal = db_loader.create_future_goal(
            parent_key=project_key,
            summary=summary_1,
            description=description_1,
        )
        future_goal_put_dict = {
            'description': description_2,
            'summary': summary_2,
            'key': future_goal.key.urlsafe(),
        }

        # Get the goal and make sure the summary matches #1.
        response = self.of_service_test('project', 'future_goal', params={'project': project_key.urlsafe()})
        content = response['response']['content']
        self.assertEqual(response['response']['type'], 'FutureGoal', 'Did not get future goal back before put.')
        self.assertEqual(content['key'], future_goal.key.urlsafe(), 'Failed to get correct future_goal key before put.')
        self.assertEqual(content['summary'], summary_1, 'Failed to get correct summary from future_goal before put.')
        self.assertEqual(content['description'], description_1, 'Failed to get correct description from future_goal before put.')

        # Put the new goal values.
        response = self.of_service_test('project', 'put_future_goal', params=future_goal_put_dict)
        content = response['response']['content']
        self.assertEqual(response['response']['type'], 'FutureGoal', 'Did not get future goal back after put.')
        self.assertEqual(content['key'], future_goal.key.urlsafe(), 'Failed to get correct future_goal key after put.')
        self.assertEqual(content['summary'], summary_2, 'Failed to get correct summary from future_goal after put.')
        self.assertEqual(content['description'], description_2, 'Failed to get correct description from future_goal after put.')

    def test_project_delete_goal_method(self):

        ''' Add a project and a goal then delete it. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)
        self.assertTrue(goal, 'Failed to init project goal object for delete test.')

        params = {'key': self.encrypt(goal.key.urlsafe())}
        response = self.of_service_test('project', 'delete_goal', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'System project delete goal service method failed.')
        goal = goal.key.get()
        self.assertFalse(goal, 'Failed to delete project goal.')

    def test_project_propose_goal_method(self):

        ''' Propose a project goal and check for it in the database. '''

        project_key = db_loader.create_project()
        goal_dict = {
            'project': project_key.urlsafe(),
            'amount': 1000,
            'description': 'DESCRIPTION',
            'funding_day_limit': 100,
            'deliverable_description': 'DELIVERABLE',
            'deliverable_date': datetime.datetime.now().isoformat(),
        }

        self.assertEqual(Goal.query().count(), 0, 'Goals existed before propose test.')

        response = self.of_service_test('project', 'propose_goal', params=goal_dict)
        self.assertEqual(response['response']['type'], 'Goal',
            'System project get goal service method failed.')

        goal_query = Goal.query()
        self.assertNotEqual(goal_query.count(), 0, 'No goal created from put test.')
        self.assertEqual(goal_query.count(), 1, 'More than one goal created from put test.')

        goal = goal_query.fetch()[0]
        self.assertEqual(goal.amount, goal_dict['amount'],
            'Wrong amount set on proposed goal.')
        self.assertEqual(goal.description, goal_dict['description'],
            'Wrong description set on proposed goal.')
        self.assertEqual(goal.deliverable_description, goal_dict['deliverable_description'],
            'Wrong deliverable_description set on proposed goal.')
        self.assertEqual(goal.funding_day_limit, goal_dict['funding_day_limit'],
            'Wrong funding days set on proposed goal.')
        self.assertEqual(goal_dict['deliverable_date'], goal_dict['deliverable_date'],
            'Wrong deliverable_date set on proposed goal.')

    def test_project_proposed_goals_method(self):

        ''' Add a project and a few completed goals and one active goal and then query. '''

        project_key = db_loader.create_project()
        db_loader.create_goal(parent_key=project_key, approved=False)
        db_loader.create_goal(parent_key=project_key, approved=False)
        db_loader.create_goal(parent_key=project_key, approved=False)
        params = {'project': self.encrypt(project_key.urlsafe())}
        response = self.of_service_test('project', 'proposed_goals', params=params)
        self.assertEqual(response['response']['type'], 'Goals',
            'Project list proposed goals service method failed.')
        self.assertEqual(len(response['response']['content']['goals']), 3,
            'Project list proposed goals returned the wrong number of proposed goals.')

    def test_project_approve_goal_method(self):

        ''' Approve a project goal. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)

        params = {'key': self.encrypt(goal.key.urlsafe())}
        response = self.of_service_test('project', 'approve_goal', params=params)
        self.assertEqual(response['response']['type'], 'Goal',
            'System project approve goal service method failed.')
        goal = goal.key.get()
        self.assertTrue(goal.approved, 'Failed to set goal to approved.')
        self.assertEqual(goal.key, project_key.get().active_goal, 'Failed to set goal as active.')

    def test_project_reject_goal_method(self):

        ''' Approve a project goal. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)

        params = {'key': self.encrypt(goal.key.urlsafe())}
        response = self.of_service_test('project', 'reject_goal', params=params)
        self.assertEqual(response['response']['type'], 'Goal',
            'System project reject goal service method failed.')
        goal = goal.key.get()
        self.assertTrue(goal.rejected, 'Failed to set goal to rejected.')
        self.assertFalse(goal.approved, 'Incorrectly to set goal to accepted.')


    #############################################
    # Project Tier Tests.
    #############################################

    def test_project_get_tier_method(self):

        ''' Add a project and a tier then query for it. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)
        tier = db_loader.create_tier(parent_key=goal.key)
        params = {'key': self.encrypt(tier.key.urlsafe())}
        response = self.of_service_test('project', 'get_tier', params=params)
        self.assertEqual(response['response']['type'], 'Tier',
            'System project get tier service method failed.')
        self.assertEqual(response['response']['content']['key'], tier.key.urlsafe(),
            'Failed to return the correct project goal tier.')

    def test_project_list_tiers_method(self):

        ''' Add a project and a few tiers then query for them. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)
        db_loader.create_tier(parent_key=goal.key)
        db_loader.create_tier(parent_key=goal.key)
        db_loader.create_tier(parent_key=goal.key)
        params = {'goal': self.encrypt(goal.key.urlsafe())}
        response = self.of_service_test('project', 'list_tiers', params=params)
        self.assertEqual(response['response']['type'], 'Tiers',
            'Project list tiers service method failed.')
        self.assertEqual(len(response['response']['content']['tiers']), 3,
            'Project list tiers returned the wrong number of tiers.')

    def test_project_put_tier_method(self):

        ''' Add a project tier through the api and then edit it. '''

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

        ''' Add a project goal and tier then delete it. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)
        tier = db_loader.create_tier(parent_key=goal.key)
        self.assertTrue(tier.key.get(), 'Failed to init project tier object for delete test.')

        params = {'key': self.encrypt(tier.key.urlsafe())}
        response = self.of_service_test('project', 'delete_tier', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'System project delete tier service method failed.')
        self.assertFalse(tier.key.get(), 'Failed to delete project goal tier.')


    #############################################
    # Project Next Step Tests.
    #############################################

    def test_project_get_next_step_method(self):

        ''' Add a project and a next_step then query for it. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)
        next_step = db_loader.create_next_step(parent_key=goal.key)
        params = {'key': self.encrypt(next_step.key.urlsafe())}
        response = self.of_service_test('project', 'get_next_step', params=params)
        self.assertEqual(response['response']['type'], 'NextStep',
            'System project get next step service method failed.')
        self.assertEqual(response['response']['content']['key'], next_step.key.urlsafe(),
            'Failed to return the correct project goal next step.')

    def test_project_list_next_steps_method(self):

        ''' Add a project and a few next steps then query for them. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)
        db_loader.create_next_step(parent_key=goal.key)
        db_loader.create_next_step(parent_key=goal.key)
        db_loader.create_next_step(parent_key=goal.key)
        params = {'goal': self.encrypt(goal.key.urlsafe())}
        response = self.of_service_test('project', 'list_next_steps', params=params)
        self.assertEqual(response['response']['type'], 'NextSteps',
            'Project list next steps service method failed.')
        self.assertEqual(len(response['response']['content']['next_steps']), 3,
            'Project list next steps returned the wrong number of next_steps.')

    def test_project_put_next_step_method(self):

        ''' Add a project next step through the api and then edit it. '''

        summary_1 = 'NEXT STEP SUMMARY'
        summary_2 = 'YRAMMUS PETS TXEN'
        description_1 = 'NEXT TEST DESCRIPTION'
        description_2 = 'SOMETHING NEXT'

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)
        next_step_dict = {
            'key': goal.key.urlsafe(),
            'summary': summary_1,
            'description': description_1,
        }

        self.assertEqual(NextStep.query().count(), 0, 'Next steps existed before put test.')

        response = self.of_service_test('project', 'put_next_step', params=next_step_dict)

        self.assertEqual(response['response']['type'], 'NextStep', 'Project list next steps service method failed.')
        next_steps = NextStep.query().fetch()
        self.assertEqual(len(next_steps), 1, 'Failed to actually put next step.')
        self.assertEqual(next_steps[0].summary, summary_1, 'Failed to save next step summary.')
        self.assertEqual(next_steps[0].description, description_1, 'Failed to save next step description.')

        next_step_key = response['response']['content']['key']

        change_dict = {
            'key': next_step_key,
            'summary': summary_2,
            'description': description_2,
        }

        response = self.of_service_test('project', 'put_next_step', params=change_dict)
        self.assertEqual(response['response']['type'], 'NextStep', 'Project list next_steps service method failed.')

        next_steps = NextStep.query().fetch()
        self.assertEqual(len(next_steps), 1, 'Failure. Put another next step instead of editing existing one.')
        self.assertEqual(next_steps[0].summary, summary_2, 'Failed to update next step summary.')
        self.assertEqual(next_steps[0].description, description_2, 'Failed to update next step description.')

    def test_project_delete_next_step_method(self):

        ''' Add a project and a next_step then delete it. '''

        project_key = db_loader.create_project()
        goal = db_loader.create_goal(parent_key=project_key)
        next_step = db_loader.create_next_step(parent_key=goal.key)
        self.assertTrue(next_step.key.get(), 'Failed to init project next step object for delete test.')

        params = {'key': self.encrypt(next_step.key.urlsafe())}
        response = self.of_service_test('project', 'delete_next_step', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'System project delete next step service method failed.')
        self.assertFalse(next_step.key.get(), 'Failed to delete project goal next step.')


    #############################################
    # Project Add/Remove Viewer Tests.
    #############################################

    def test_project_add_viewer_method(self):

        ''' Add one project to the database then add a viewer to it. '''

        project_key = db_loader.create_project(status='o')
        user_key = db_loader.create_user()
        params = {'user': user_key.urlsafe(), 'target': project_key.urlsafe()}
        response = self.of_service_test('project', 'add_viewer', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'Project add viewer service method failed.')
        self.assertEqual(len(project_key.get().viewers), 1,
            'Project add viewer method did not add one viewer.')
        self.assertEqual(project_key.get().viewers[0], user_key,
            'Project add viewer method did not add correct viewer.')

    def test_project_remove_viewer_method(self):

        ''' Add one project to the database with a viewer then remove the viewer. '''

        user_key = db_loader.create_user()
        project_key = db_loader.create_project(status='p', viewers_keys=[user_key])
        params = {'user': user_key.urlsafe(), 'target': project_key.urlsafe()}
        response = self.of_service_test('project', 'remove_viewer', params=params)
        self.assertEqual(response['response']['type'], 'Echo',
            'Project remove viewer service method failed.')
        self.assertEqual(len(project_key.get().viewers), 0,
            'Project remove viewer method did not remove one viewer.')
