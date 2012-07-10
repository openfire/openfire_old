from openfire.models.project import Proposal, Project, Category
from openfire.models.assets import CustomURL
from openfire.models.user import User
from google.appengine.ext import ndb

'''
This module is used to create database entities for testing purposes.
'''

def create_category(slug='test', name='Test Category', description='some txt'):
    return Category(key=ndb.Key('Category', slug), slug=slug, name=name, description=description,
        ).put()


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


def create_user(username='fake', firstname='Fakie', lastname='McFakerton', bio='some bio'):
    return User(key=ndb.Key('User', username), username=username, firstname=firstname, lastname=lastname, bio=bio).put()
