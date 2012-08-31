from __future__ import with_statement
import os
import config
from google.appengine.ext import ndb
from google.appengine.api import files, images, urlfetch
from webapp2_extras import security as wsec

from openfire.models.user import User, EmailAddress, Permissions, Topic
from openfire.models.contribution import ContributionType
from openfire.models.project import Proposal, Project, Category, Tier, Goal
from openfire.models.assets import Asset, Avatar, Video, Image, CustomURL
from openfire.models.indexer import index

import logging

'''
This module is used to create database entities for testing purposes.
'''


def fetch_url_to_blobstore(url):

    '''
    This is a helper method to upload a local file to the blobstore.
    Returns a BlobKey object.
    '''

    logging.info('DOWNLOADING URL FILE to blobstore. At url "%s".' % url)

    # Fetch the url.
    result = urlfetch.fetch(url)
    if result.status_code != 200:
        return None

    # Create the blob.
    blob_name = files.blobstore.create(mime_type=result.headers['content-type'])
    with files.open(blob_name, 'a') as blob:
        blob.write(result.content)
    files.finalize(blob_name)

    # Return the blob key.
    return files.blobstore.get_blob_key(blob_name)


def upload_local_file_to_blobstore(filename, mime_type):

    '''
    This is a helper method to upload a local file to the blobstore.
    It is not currently in use since we are having trouble loading local files
    in google app engine.

    Returns a BlobKey object.
    '''

    logging.info('UPLOADING FILE to blobstore. At filename "%s".' % filename)
    print 'Uploading file to blobstore. At filename "%s".' % filename

    # Upload to blob.
    blob_name = files.blobstore.create(mime_type=mime_type)

    print 'Blob name: "%s".' % blob_name

    # Open blob and write the file to it.
    if os.name == 'nt':
        mode = 'rb'
        file_data = b""
    else:
        mode = 'r'
        file_data = ""

    with open(filename, mode) as local_file:
        logging.info('Local file: "%s".' % local_file)
        print 'Local file: "%s".' % local_file
        file_data = local_file.read()

    logging.info('Found file data with length "%s".' % len(file_data))
    print 'Found file data with length "%s".' % len(file_data)

    logging.info('Opening blob...')
    print 'Opening blob...'
    with files.open(blob_name, 'a') as blob:

        logging.info('Blob file: "%s".' % blob)
        print 'Blob file: "%s".' % blob

        blob.write(file_data)

    logging.info('Done writing...')
    print 'Done writing...'

    # Finalize the blob.
    files.finalize(blob_name)

    logging.info('Finalized.')
    print 'Finalized.'

    # Get the file's blob key
    blob_key = files.blobstore.get_blob_key(blob_name)

    logging.info('Uploaded blob key: "%s".' % blob_key)
    print 'Uploaded blob key: "%s".' % blob_key

    return blob_key


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


def create_contribution_type(slug='slug', name='NAME', unit='CASH', plural='CASH', subunit='DOLLAR', subunit_plural='DOLLARS'):

    ''' Create a new contribution type. '''

    return ContributionType(id=slug, slug=slug, name=name,  unit=unit, plural=plural, subunit=subunit, subunit_plural=subunit_plural).put()


def create_topic(slug='test', name='Test Topic', description='some txt'):

    ''' Create a topic. '''

    return Topic(key=ndb.Key('Topic', slug), slug=slug, name=name, description=description).put()


def create_user(username='fakie', password='fakieiscool', firstname='Fakie', lastname='McFakerton', location='San Francisco, CA', bio='some bio', email=None, create_permissions=False, activated=True, topics=[], public=True):

    '''
    Create a new user.
    The password should be passed in a plaintext, and will be encrypted here.
    The email field is optional, and if provided an email object will be added as well.
    '''

    _securityConfig = config.config.get('openfire.security')
    pwd = wsec.hash_password(  password,
                               _securityConfig.get('config', {}).get('wsec', {}).get('hash', 'sha256'),
                               _securityConfig.get('config', {}).get('random', {}).get('blocks', {}).get('salt', '__salt__'),
                               _securityConfig.get('config', {}).get('random', {}).get('blocks', {}).get('pepper', '__pepper__'))

    if isinstance(email, list):
        emails = email[:]
        email = email[0]
    else:
        emails = False

    user_key = User(key=ndb.Key('User', username), username=username, firstname=firstname, lastname=lastname,
            location=location, bio=bio, password=pwd, activated=activated, public=public, topics=topics).put()

    if emails:
        for email in emails:
            create_email_address(address=email, parent_key=user_key, user_key=user_key)

    elif email and not emails:
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
            category_key=ndb.Key('Category', 'test_category_key'),
            creator_key=ndb.Key('User', 'test_user_key'),
            owners_keys=[], viewers_keys=[], goals=[], tiers=[]):

    ''' Create a proposal. '''

    goal_list = []
    for goal in goals:
        goal_list.append(create_goal(**goal))
    tier_list = []
    for tier in tiers:
        tier_list.append(create_tier(**tier))
    return Proposal(name=name, status=status, public=public,
                    summary=summary, pitch=pitch, tech=tech, keywords=keywords,
                    category=category_key, creator=creator_key, goals=goal_list, tiers=tier_list,
                    viewers=viewers_keys, owners=owners_keys).put()


def create_project(name='Test Project', status='o', public=True, summary='SUMMARY', pitch='PITCH',
            tech='TECH', keywords=['KEYWORDS'], progress=0, money=0,
            proposal_key=ndb.Key('Proposal', 'test_proposal_key'), category_key=ndb.Key('Category', 'test_category_key'),
            creator_key=ndb.Key('User', 'test_user_key'), owners_keys=[], viewers_keys=[]):

    ''' Create a project. '''

    return Project(name=name, status=status, public=public, summary=summary, pitch=pitch, tech=tech,
            keywords=keywords, progress=progress, money=money, proposal=proposal_key, category=category_key,
            creator=creator_key, owners=owners_keys, viewers=viewers_keys).put()


def create_avatar(parent_key=None, url='', name='', mime='', pending=False, version=1, active=True,
            approved=True, blob_file=None, mime_type='image/png'):

    '''
    Create an avatar and assign it to a project or user.

    If blob_file is set to a local file, it will be uploaded to the blobstore and
    the serving url will be set.
    '''

    if not parent_key:
        logging.critical('parent_key is required when creating an avatar.')
        return

    parent = parent_key.get()
    if not parent:
        logging.critical('Parent could not be found when creating avatar fixture.')
        return

    blob_key = None
    serving_url = url
    if blob_file:
        # Upload the file to the blobstore.
        try:
            # Try to fetch the file from a url.
            blob_key = fetch_url_to_blobstore(blob_file)
        except:
            # Fall back to loading from a local copy.
            local_file = os.path.join(os.path.dirname(__file__), '..', 'fixtures', 'img_links', name)
            blob_key = upload_local_file_to_blobstore(local_file, mime_type)

        # Get the serving url for the image.
        serving_url = images.get_serving_url(blob_key, secure_url=True)

        # TODO: Should we remove the http:// portion of the url?
        #serving_url = serving_url.split('://')[1]

    if blob_key:
        asset_key = Asset(url=serving_url, name=name, mime=mime, pending=pending, kind='a', blob=blob_key).put()
    else:
        asset_key = Asset(url=serving_url, name=name, mime=mime, pending=pending, kind='a').put()

    avatar_key = Avatar(key=ndb.Key(Avatar, asset_key.urlsafe(), parent=parent_key),
            version=version, active=active, url=serving_url, asset=asset_key, approved=approved).put()
    parent.avatar = avatar_key
    parent.put()


def create_image(parent_key=None, url='', name='', mime='', pending=False,
            approved=True, blob_file=None, mime_type='image/png'):

    ''' Create an image and add it to a project. '''

    if not parent_key:
        logging.critical('Parent is required when creating an image.')
        return
    parent = parent_key.get()

    if not parent:
        logging.critical('Parent could not be found when creating an image fixture.')
        return

    blob_key = None
    serving_url = url
    if blob_file:
        # Upload the file to the blobstore.
        blob_key = fetch_url_to_blobstore(blob_file)

        # Get the serving url for the image.
        serving_url = images.get_serving_url(blob_key, secure_url=True)

        # TODO: Should we remove the http:// portion of the url?
        #serving_url = serving_url.split('://')[1]

    if blob_key:
        asset_key = Asset(url=serving_url, name=name, mime=mime, pending=pending, kind='i', blob=blob_key).put()
    else:
        asset_key = Asset(url=serving_url, name=name, mime=mime, pending=pending, kind='i').put()
    image_key = Image(key=ndb.Key(Image, asset_key.urlsafe(), parent=parent_key),
            url=serving_url, asset=asset_key, approved=approved).put()
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
