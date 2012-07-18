from google.appengine.ext import ndb
from webapp2_extras import security as wsec

from openfire.models.user import User, EmailAddress, Permissions
from openfire.models.contribution import ContributionType
from openfire.models.project import Proposal, Project, Category, Tier, Goal
from openfire.models.assets import Asset, Avatar, Video, Image, CustomURL
from openfire.models.indexer import index

import logging

'''
This module is used to create database entities for testing purposes.
'''

def build_indexes(index_list):

    ''' Build record indexes. '''

    index.IndexEvent(id='_init_').put()

    meta_i = index.Index.new('_meta_')
    meta_i.put()

    ## indexes
    index_dict = {}
    for i in index_list:
        index_dict[i] = index.Index.new(i)
    ndb.put_multi(index_dict.values())
    index.IndexEvent(id='_indexes_init_').put()

    ## entries
    entry_dict = {}
    for i in index_list:
        entry_dict[i] = meta_i.add(i)
    ndb.put_multi(entry_dict.values())
    index.IndexEvent(id='_entries_init_').put()

    ## mappings
    mapping_dict = {}
    for i in index_list:
        mapping_dict[i] = entry_dict[i].map(index_dict[i].key)
    ndb.put_multi(mapping_dict.values())
    index.IndexEvent(id='_mappings_init_').put()


def create_contribution_type(slug='slug', name='NAME', unit='CASH', plural='CASH', subunit='DOLLAR', subunit_plural='DOLLARS'):

    ''' Create a new contribution type. '''

    return ContributionType(id=slug, slug=slug, name=name,  unit=unit, plural=plural, subunit=subunit, subunit_plural=subunit_plural).put()


def create_user(username='fakie', password='fakieiscool', firstname='Fakie', lastname='McFakerton', location='San Francisco, CA', bio='some bio', email=None, create_permissions=False):

    '''
    Create a new user.
    The password should be passed in a plaintext, and will be encrypted here.
    The email field is optional, and if provided an email object will be added as well.
    '''

    pwd = wsec.hash_password(password, 'sha256',
            wsec.generate_random_string(length=32, pool=wsec.ASCII_PRINTABLE),
            'openfire-internal')
    user_key = User(key=ndb.Key('User', email), username=username, firstname=firstname, lastname=lastname,
            location=location, bio=bio, password=pwd).put()
    if email:
        create_email_address(address=email, parent_key=user_key, user_key=user_key)

    if create_permissions:
        create_user_permissions(parent_key=user_key, user_key=user_key)

    return user_key


def create_email_address(address='fakie@mcfakerton.com', parent_key=ndb.Key('User', 'fakie'),
            user_key=ndb.Key('User', 'fakie'), label='d', notify=True, jabber=True, gravatar=True):

    ''' Create a user email address and append it to the user array. '''

    email_key = EmailAddress(id=address, parent=parent_key, user=user_key, address=address, label=label, notify=notify, jabber=jabber, gravatar=gravatar).put()
    try:
        user_obj = user_key.get()
        user_obj.email.append(email_key)
        user_obj.put()
    except:
        # TODO: What should we do when this fails?
        logging.critical('Failed to save the user object when creating an email address fixture.')
    return email_key


def create_user_permissions(id='global', parent_key=ndb.Key('User', 'fakie'), user_key=ndb.Key('User', 'fakie'),
            moderator=True, admin=True, developer=True):

    ''' Create a user permissions and append it to the user array. '''

    perm_key = Permissions(id=id, parent=parent_key, user=user_key, moderator=moderator, admin=admin,
            developer=developer).put()
    try:
        user_obj = user_key.get()
        user_obj.permissions.append(perm_key)
        user_obj.put()
    except:
        # TODO: What should we do when this fails?
        logging.critical('Failed to save the user object when creating a permission fixture.')
    return perm_key


def create_category(slug='test', name='Test Category', description='some txt', keywords=['fake'], parent_key=None):

    ''' Create a category. '''

    category = None
    if parent_key:
        category = Category(key=ndb.Key('Category', slug, parent=parent_key), slug=slug, name=name,
                description=description, keywords=keywords, parent=parent_key)
    else:
        category = Category(key=ndb.Key('Category', slug), slug=slug, name=name, description=description,
                keywords=keywords)
    if not category:
        logging.critical('Failed to save a category fixture.')
        return None
    return category.put()


def create_goal(parent_key=None, contribution_type_id='fake', amount=1, description='DESCRIPTION',
        backer_count=0, progress=50, met=False):

    ''' Create a new funding goal. If parent is None, do not put the object (for proposals).'''

    contribution_type = ndb.Key('ContributionType', contribution_type_id)
    goal = Goal(contribution_type=contribution_type, amount=amount, description=description,
            backer_count=backer_count, progress=progress, met=met, parent=parent_key)
    parent_obj = None
    if parent_key:
        goal.parent = parent_key
        goal.put()
        parent_obj = parent_key.get()
        if parent_obj:
            parent_obj.goals.append(goal.key)
            parent_obj.put()
    return goal


def create_tier(parent_key=None, name='NAME', contribution_type_id='cash', amount=1,
        description='DESCRIPTION', delivery="tomorrow", backer_count=0, backer_limit=100):

    ''' Create a new contribution tier. If parent is None, do not put the object (for proposals).'''

    contribution_type = ndb.Key('ContributionType', contribution_type_id)
    tier = Tier(name=name, contribution_type=contribution_type, amount=amount, description=description,
            delivery=delivery, backer_count=backer_count, backer_limit=backer_limit, parent=parent_key)
    parent_obj = None
    if parent_key:
        tier.parent = parent_key
        tier.put()
        parent_obj = parent_key.get()
        if parent_obj:
            parent_obj.tiers.append(tier.key)
            parent_obj.put()
    return tier


def create_proposal(name='Test Proposal', status='s', public=True,
            summary='SUMMARY', pitch='PITCH', tech='TECH', keywords=['KEYWORDS'],
            category=ndb.Key('Category', 'test_category_key'),
            creator=ndb.Key('User', 'test_user_key'),
            owners=[], viewers=[], goals=[], tiers=[]):

    ''' Create a proposal. '''

    goal_list = []
    for goal in goals:
        goal_list.append(create_goal(**goal))
    tier_list = []
    for tier in tiers:
        tier_list.append(create_tier(**tier))
    return Proposal(name=name, status=status, public=public,
                    summary=summary, pitch=pitch, tech=tech, keywords=keywords,
                    category=category, creator=creator, goals=goal_list, tiers=tier_list,
                    viewers=viewers, owners=owners).put()


def create_project(name='Test Project', status='o', public=True, summary='SUMMARY', pitch='PITCH',
            tech='TECH', keywords=['KEYWORDS'], progress=0, money=0,
            proposal=ndb.Key('Proposal', 'test_proposal_key'), category=ndb.Key('Category', 'test_category_key'),
            creator=ndb.Key('User', 'test_user_key'), owners=[], viewers=[]):

    ''' Create a project. '''

    return Project(name=name, status=status, public=public, summary=summary, pitch=pitch, tech=tech,
            keywords=keywords, progress=progress, money=money, proposal=proposal, category=category,
            creator=creator, owners=owners, viewers=viewers).put()


def create_avatar(parent_key=None, url='', name='', mime='', pending=False, version=1, active=True, approved=True):

    ''' Create an avatar and assign it to a project or user. '''

    if not parent_key:
        logging.critical('parent_key is required when creating an avatar.')
        return
    parent = parent_key.get()
    if not parent:
        logging.critical('Parent could not be found when creating avatar fixture.')
        return

    asset_key = Asset(url=url, name=name, mime=mime, pending=pending, kind='a').put()
    avatar_key = Avatar(key=ndb.Key(Avatar, asset_key.urlsafe(), parent=parent_key),
            version=version, active=active, url=url, asset=asset_key, approved=approved).put()
    parent.avatar = avatar_key
    parent.put()


def create_image(parent_key=None, url='', name='', mime='', pending=False, approved=True):

    ''' Create an image and add it to a project. '''

    if not parent_key:
        logging.critical('Parent is required when creating an image.')
        return
    parent = parent_key.get()
    if not parent:
        logging.critical('Parent could not be found when creating an image fixture.')
        return

    asset_key = Asset(url=url, name=name, mime=mime, pending=pending, kind='i').put()
    image_key = Image(key=ndb.Key(Image, asset_key.urlsafe(), parent=parent_key),
            url=url, asset=asset_key, approved=approved).put()
    parent.images.append(image_key)
    parent.put()


def create_video(parent_key=None, url='', name='', mime='', provider='', pending=False, approved=True, featured=True):

    ''' Create an video and assign it to a project. '''

    if not parent_key:
        logging.critical('Parent is required when creating an video.')
        return
    parent = parent_key.get()
    if not parent:
        logging.critical('Parent could not be found when creating a video fixture.')
        return

    asset_key = Asset(url=url, name=name, mime=mime, pending=pending, kind='v').put()
    video_key = Video(key=ndb.Key(Video, 'mainvideo', parent=parent_key),
            provider=provider, url=url, asset=asset_key, approved=approved, featured=featured).put()
    parent.video = video_key
    parent.put()


def create_custom_url(slug='test', target_key=None):

    ''' Create a custom url, provided a target kind and id. '''

    if not target_key:
        logging.critical('target_key is required when creating a custom url.')
        return
    target = target_key.get()
    if not target:
        logging.critical('Could not find target to set customurl field for in fixture.')
        return
    url_key = CustomURL(key=ndb.Key('CustomURL', slug), slug=slug, target=target_key).put()
    target.customurl = url_key
    target.put()
    return url_key
