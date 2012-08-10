from openfire.models.project import Proposal, Project, Category, Tier, Goal
from openfire.models.contribution import ContributionType
from openfire.models.assets import CustomURL
from openfire.models.user import User, Topic
from google.appengine.ext import ndb

'''
This module is used to create database entities for testing purposes.
'''

def create_category(slug='test', name='Test Category', description='some txt'):
    return Category(key=ndb.Key('Category', slug), slug=slug, name=name, description=description,
        ).put()


def create_topic(slug='test', name='Test Topic', description='some txt'):
    return Topic(key=ndb.Key('Topic', slug), slug=slug, name=name, description=description).put()


def create_proposal(name='Test Proposal', status='s', public=True,
                    summary="SUMMARY", pitch="PITCH", tech="TECH", keywords=["KEYWORDS"],
                    category=ndb.Key('Category', 'test_category_key'),
                    creator=ndb.Key('User', 'test_user_key'),
                    ):
    return Proposal(name=name, status=status, public=public,
                    summary=summary, pitch=pitch, tech=tech, keywords=keywords,
                    category=category, creator=creator
                    ).put()


def create_project(name='Test Project', status='o', public=True,
                    summary="SUMMARY", pitch="PITCH", tech="TECH", keywords=["KEYWORDS"],
                    proposal=ndb.Key('Proposal', 'test_proposal_key'),
                    category=ndb.Key('Category', 'test_category_key'),
                    creator=ndb.Key('User', 'test_user_key'),
                    ):
    return Project(name=name, status=status, public=public, summary=summary,
                    pitch=pitch, tech=tech, keywords=keywords, proposal=proposal,
                    category=category, creator=creator
                    ).put()


def create_custom_url(slug='test', target_kind='Project', target_id='1'):
    return CustomURL(key=ndb.Key('CustomURL', slug), slug=slug, target=ndb.Key(target_kind, target_id)).put()


def create_user(username='fake', firstname='Fakie', lastname='McFakerton', bio='some bio',
        location='somewhere', topics=[], activated=True, public=True):
    return User(key=ndb.Key('User', username), username=username, firstname=firstname,
                lastname=lastname, bio=bio, location=location, topics=topics, activated=activated,
                public=public).put()


def create_goal(target_id='fake', contribution_type_id='fake', amount=100, description='DESCRIPTION', backer_count=0, progress=50, met=False):

    target = ndb.Key('Project', target_id)
    contribution_type = ndb.Key('ContributionType', contribution_type_id)
    goal = Goal(target=target, contribution_type=contribution_type, amount=amount, description=description, backer_count=backer_count, progress=progress, met=met, parent=target).put()
    if target and target.get():
        target = target.get()
        target.goals.append(goal)
        target.put()
    return goal


def create_tier(target_id='fake', name='NAME', contribution_type_id='fake', amount=100, description='DESCRIPTION', delivery="tomorrow", backer_count=100, backer_limit=100):

    target = ndb.Key('Project', target_id)
    contribution_type = ndb.Key('ContributionType', contribution_type_id)
    tier = Tier(target=target, name=name, contribution_type=contribution_type, amount=amount, description=description, delivery=delivery, backer_count=backer_count, backer_limit=backer_limit, parent=target).put()
    if target and target.get():
        target = target.get()
        target.tiers.append(tier)
    return tier


def create_contribution_type(slug='slug', name='NAME', unit='CASH', plural='CASH', subunit='DOLLAR', subunit_plural='DOLLARS'):
    return ContributionType(id=slug, slug=slug, name=name,  unit=unit, plural=plural, subunit=subunit, subunit_plural=subunit_plural).put()
