from google.appengine.ext import ndb
from openfire.handlers import WebHandler
from openfire.models import user, project, assets, system, contribution, indexer


class DevModels(WebHandler):

    ''' Quickly insert some dev models for testing. This is NOT meant to be a full, permanent fixture. '''

    def get(self):

        ''' Insert a couple of categories, a couple of proposals + projects, a couple of users, and we're good. '''

        run = True
        flag = system.SystemProperty.get('fixture', 'openfire.dev.BaseDataFixture')
        if flag:
            run = (not flag.has_run)

        if run:

            ## indexer models
            if hasattr(indexer.Index, 'new'):

                indexer.IndexEvent(id='_init_').put()

                ## indexes
                meta_i = indexer.Index.new('_meta_')
                user_i = indexer.Index.new('user')
                update_i = indexer.Index.new('update')
                project_i = indexer.Index.new('project')
                category_i = indexer.Index.new('category')
                activity_i = indexer.Index.new('activity')

                indexes = ndb.put_multi([meta_i, user_i, update_i, project_i, category_i, activity_i])

                indexer.IndexEvent(id='_indexes_init_').put()

                ## entries
                user_i_entry = indexer.IndexEntry(id='user', parent=meta_i)
                update_i_entry = indexer.IndexEntry(id='update', parent=meta_i)
                project_i_entry = indexer.IndexEntry(id='project', parent=meta_i)
                category_i_entry = indexer.IndexEntry(id='category', parent=meta_i)
                activity_i_entry = indexer.IndexEntry(id='activity', parent=meta_i)

                index_entries = ndb.put_multi([user_i_entry, update_i_entry, project_i_entry, category_i_entry, activity_i_entry])

                indexer.IndexEvent(id='_entries_init_').put()

                ## mappings
                user_i_mapping = indexer.IndexMapping(id=user_i.key.urlsafe(), parent=user_i_entry)
                update_i_mapping = indexer.IndexMapping(id=update_i.key.urlsafe(), parent=update_i_entry)
                project_i_mapping = indexer.IndexMapping(id=project_i.key.urlsafe(), parent=project_i_entry)
                category_i_mapping = indexer.IndexMapping(id=category_i.key.urlsafe(), parent=category_i_entry)
                activity_i_mapping = indexer.IndexMapping(id=activity_i.key.urlsafe(), parent=activity_i_entry)

                index_mappings = ndb.put_multi([user_i_mapping, update_i_mapping, project_i_mapping, category_i_mapping, activity_i_mapping])

                indexer.IndexEvent(id='_mappings_init_').put()

            ## contribution types
            money = contribution.ContributionType(slug='money', name='Money', unit='dollar', plural='dollars', subunit='cent', subunit_plural='cents')
            time = contribution.ContributionType(slug='time', name='Time', unit='hour', plural='hours', subunit='minute', subunit_plural='minutes')
            code = contribution.ContributionType(slug='code', name='Code', unit='line', plural='lines')
            advocacy = contribution.ContributionType(slug='advocacy', name='Advocacy', unit='dollar', plural='dollars', subunit='cent', subunit_plural='cents')

            contribution_types = ndb.put_multi([money, time, code, advocacy])

            ## users first
            pug = user.User(key=ndb.Key(user.User, 'pug'), username='pug', firstname='David', lastname='Anderson', bio='hola yo soy pug').put()
            sam = user.User(key=ndb.Key(user.User, 'sam'), username='sam', firstname='Sam', lastname='Gammon', bio='fiesta ayayayay').put()
            david = user.User(key=ndb.Key(user.User, 'david'), username='david', firstname='David', lastname='Rekow', bio='hi i is david').put()
            ethan = user.User(key=ndb.Key(user.User, 'ethan'), username='ethan', firstname='Ethan', lastname='Leland', bio='i am mister ethan').put()

            users = [pug, sam, david, ethan]

            ## categories next
            politics = project.Category(key=ndb.Key(project.Category, 'politics'), slug='politics', name='Politics', description='Having to do with politics.', keywords=['policy', 'government']).put()
            transparency = project.Category(key=ndb.Key(project.Category, 'transparency', parent=politics), slug='transparency', name='Transparency', description='Having to do with open information.', keywords=['politics', 'policy', 'opennes', 'freedom'], parent=politics).put()
            money = project.Category(key=ndb.Key(project.Category, 'money'), slug='money', name='Money', description='Having to do with money or currency.', keywords=['currency', 'tender', 'money', 'debt', 'economies']).put()
            law = project.Category(key=ndb.Key(project.Category, 'law'), slug='law', name='Law', description='Having to do with law or policy.', keywords=['policy', 'law', 'government']).put()
            business = project.Category(key=ndb.Key(project.Category, 'business'), slug='business', name='Business', description='Having to do with commercial enterprise.', keywords=['corporations', 'startups']).put()

            categories = [politics, transparency, money, law, business]

            ## proposals third
            fatcatmap = project.Proposal(
                    name='fat cat map',
                    status='a',
                    category=transparency,
                    summary='ever wonder who your local congressman gets his money?',
                    pitch='cool fat pitch herr',
                    tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                    keywords=['transparency', 'politics', 'opendata', 'visualization'],
                    creator=sam,
                    owners=[sam, david],
                    public=True,
                    viewers=[pug, ethan],
                    goals=[
                        project.Goal(),
                        project.Goal(),
                        project.Goal()
                    ],
                    tiers=[
                        project.Tier(),
                        project.Tier(),
                        project.Tier()
                    ]
            ).put()

            seasteading = project.Proposal(
                    name='SeaSteading',
                    status='a',
                    category=law,
                    summary='ever take issue with H1B visa policy in the united states! well then help us buy a cruise ship.',
                    pitch='cool sea pitch herr',
                    tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                    keywords=['business', 'law', 'policy'],
                    creator=david,
                    owners=[david, ethan],
                    public=True,
                    viewers=[pug, sam],
                    goals=[
                        project.Goal(),
                        project.Goal(),
                        project.Goal()
                    ],
                    tiers=[
                        project.Tier(),
                        project.Tier(),
                        project.Tier()
                    ]
            ).put()

            urbsly = project.Proposal(
                    name='urbsly',
                    status='a',
                    category=business,
                    summary='ever hate on monsanto a bunch? duke on them some more with this thing',
                    pitch='cool urbs pitch herr',
                    tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                    keywords=['ecology', 'seeds-and-shit', 'yup'],
                    creator=ethan,
                    owners=[ethan, sam],
                    public=True,
                    viewers=[pug, david],
                    goals=[
                        project.Goal(),
                        project.Goal(),
                        project.Goal()
                    ],
                    tiers=[
                        project.Tier(),
                        project.Tier(),
                        project.Tier()
                    ]
            ).put()

            proposals = [fatcatmap, seasteading, urbsly]

            # then goals + tiers (project sub-artifacts)

            # fourth, projects
            fatcatmap = project.Project(
                    name='fat cat map',
                    status='o',
                    category=transparency,
                    proposal=fatcatmap,
                    summary='ever wonder who your local congressman gets his money?',
                    pitch='cool fat pitch herr',
                    tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                    keywords=['transparency', 'politics', 'opendata', 'visualization'],
                    creator=sam,
                    owners=[sam, david],
                    public=True,
                    viewers=[pug, ethan]
            ).put()

            seasteading = project.Project(
                    name='SeaSteading',
                    status='o',
                    category=law,
                    proposal=seasteading,
                    summary='ever take issue with H1B visa policy in the united states! well then help us buy a cruise ship.',
                    pitch='cool sea pitch herr',
                    tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                    keywords=['business', 'law', 'policy'],
                    creator=david,
                    owners=[david, ethan],
                    public=True,
                    viewers=[pug, sam]
            ).put()

            urbsly = project.Project(
                    name='urbsly',
                    status='o',
                    category=business,
                    proposal=urbsly,
                    summary='ever hate on monsanto a bunch? duke on them some more with this thing',
                    pitch='cool urbs pitch herr',
                    tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                    keywords=['ecology', 'seeds-and-shit', 'yup'],
                    creator=ethan,
                    owners=[ethan, sam],
                    public=True,
                    viewers=[pug, david]
            ).put()

            projects = [fatcatmap, seasteading, urbsly]

            # fif, assets, avatars + videos
            fcm_avatar = assets.Asset(key=ndb.Key(assets.Asset, 'fatcatmap.png'), url='fatcatmap.png', kind='i').put()
            fcm_video = assets.Asset(key=ndb.Key(assets.Asset, 'bnyiMnG62OI'), url='http://www.youtube.com/watch?v=bnyiMnG62OI', kind='v').put()
            ssd_avatar = assets.Asset(key=ndb.Key(assets.Asset, 'seasteading.png'), url='seasteading.png', kind='i').put()
            urb_avatar = assets.Asset(key=ndb.Key(assets.Asset, 'urbsly.png'), url='urbsly.png', kind='i').put()
            urb_video = assets.Asset(key=ndb.Key(assets.Asset, 'rQkTI7XXYvw'), url='http://www.youtube.com/watch?v=bnyiMnG62OI', kind='v').put()

            avatars = [

                    assets.Avatar(key=ndb.Key(assets.Avatar, 'current', parent=fatcatmap), version=1, active=True, url='fatcatmap.png', asset=fcm_avatar),
                    assets.Video(key=ndb.Key(assets.Avatar, 'mainvideo', parent=fatcatmap), url='https://www.youtube.com/embed/bnyiMnG62OI', asset=fcm_video, provider='youtube'),
                    assets.Avatar(key=ndb.Key(assets.Avatar, 'current', parent=seasteading), version=1, active=True, url='seasteading.png', asset=ssd_avatar),
                    assets.Avatar(key=ndb.Key(assets.Avatar, 'current', parent=urbsly), version=1, active=True, url='urbsly.png', asset=urb_avatar),
                    assets.Video(key=ndb.Key(assets.Avatar, 'mainvideo', parent=urbsly), url='https://www.youtube.com/embed/rQkTI7XXYvw', asset=urb_video, provider='youtube')

            ]

            ndb.put_multi(avatars)

            # finally, custom URLS

            ## projects first
            fcm_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'fatcatmap'), slug='fatcatmap', target=fatcatmap)
            ssd_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'seasteading'), slug='seasteading', target=seasteading)
            urb_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'urbsly'), slug='urbsly', target=urbsly)

            ## then users
            sam_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'sam'), slug='sam', target=sam)
            david_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'david'), slug='david', target=david)
            ethan_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'ethan'), slug='ethan', target=ethan)
            pug_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'pug'), slug='pug', target=pug)

            custom_urls = [fcm_url, ssd_url, urb_url, sam_url, david_url, ethan_url, pug_url]

            ndb.put_multi(custom_urls)

            s = system.SystemProperty.set('fixture', 'openfire.dev.BaseDataFixture', has_run=True)

        return self.redirect_to('landing')
