import datetime
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from apptools import BaseHandler

from openfire.models import system, contribution
from openfire.models import user, project, assets
from openfire.models.indexer import index, entry, map as mapping


class TestMultipart(BaseHandler):

    ''' Test multipart uploads. '''

    def get(self):

        ''' Return the form. '''

        from google.appengine.ext import blobstore
        return self.render('test/multipart.html', endpoint=blobstore.create_upload_url('/_test/multipart/passthrough'))



class TestPassthrough(blobstore_handlers.BlobstoreUploadHandler):

    ''' Test the blobstore passthrough. '''

    def post(self):

        ''' Passthrough. '''

        import pdb; pdb.set_trace()

        uploads = self.get_uploads()

        return self.response.write('<pre>' + str(self.request) + '</pre>')


class DevModels(BaseHandler):

    ''' Quickly insert some dev models for testing. This is NOT meant to be a full, permanent fixture. '''

    force_load_session = False

    def get(self):

        ''' Insert a couple of categories, a couple of proposals + projects, a couple of users, and we're good. '''

        run = True
        flag = system.SystemProperty.get('fixture', 'openfire.dev.BaseDataFixture')
        if flag:
            run = (not flag.has_run)

        if run:

            ## indexer models
            if hasattr(index.Index, 'new'):

                index.IndexEvent(id='_init_').put()

                ## indexes
                meta_i = index.Index.new('_meta_')
                user_i = index.Index.new('user')
                update_i = index.Index.new('update')
                project_i = index.Index.new('project')
                category_i = index.Index.new('category')
                activity_i = index.Index.new('activity')

                ndb.put_multi([meta_i, user_i, update_i, project_i, category_i, activity_i])

                index.IndexEvent(id='_indexes_init_').put()

                ## entries
                user_i_entry = meta_i.add('user')
                update_i_entry = meta_i.add('update')
                project_i_entry = meta_i.add('project')
                category_i_entry = meta_i.add('category')
                activity_i_entry = meta_i.add('activity')

                ndb.put_multi([user_i_entry, update_i_entry, project_i_entry, category_i_entry, activity_i_entry])

                index.IndexEvent(id='_entries_init_').put()

                ## mappings
                user_i_mapping = user_i_entry.map(user_i.key)
                update_i_mapping = update_i_entry.map(update_i.key)
                project_i_mapping = project_i_entry.map(project_i.key)
                category_i_mapping = category_i_entry.map(category_i.key)
                activity_i_mapping = activity_i_entry.map(activity_i.key)

                ndb.put_multi([user_i_mapping, update_i_mapping, project_i_mapping, category_i_mapping, activity_i_mapping])

                index.IndexEvent(id='_mappings_init_').put()

            ## contribution types
            money = contribution.ContributionType(id='money', slug='money', name='Money', unit='dollar', plural='dollars', subunit='cent', subunit_plural='cents')
            time = contribution.ContributionType(id='time', slug='time', name='Time', unit='hour', plural='hours', subunit='minute', subunit_plural='minutes')
            code = contribution.ContributionType(id='code', slug='code', name='Code', unit='line', plural='lines')
            advocacy = contribution.ContributionType(id='advocacy', slug='advocacy', name='Advocacy', unit='dollar', plural='dollars', subunit='cent', subunit_plural='cents')

            ndb.put_multi([money, time, code, advocacy])

            ## users first
            pug = user.User(key=ndb.Key(user.User, 'david@openfi.re'), username='pug', firstname='David', lastname='Anderson', location='San Francisco, CA', bio='hola yo soy pug').put()
            sam = user.User(key=ndb.Key(user.User, 'sam@openfi.re'), username='sam', firstname='Sam', lastname='Gammon', location='San Francisco, CA', bio='fiesta ayayayay').put()
            david = user.User(key=ndb.Key(user.User, 'davidr@openfi.re'), username='david', firstname='David', lastname='Rekow', location='San Francisco, CA', bio='hi i is david').put()
            ethan = user.User(key=ndb.Key(user.User, 'ethan@openfi.re'), username='ethan', firstname='Ethan', lastname='Leland', location='San Francisco, CA', bio='i am mister ethan').put()

            ## user emails
            user_emails = [
                user.EmailAddress(id='david@openfi.re', parent=pug, user=pug, address='david@openfi.re', label='d', notify=True, jabber=True, gravatar=True),
                user.EmailAddress(id='sam@openfi.re', parent=sam, user=sam, address='sam@openfi.re', label='d', notify=True, jabber=True, gravatar=True),
                user.EmailAddress(id='davidr@openfi.re', parent=david, user=david, address='davidr@openfi.re', label='d', notify=True, jabber=True, gravatar=True),
                user.EmailAddress(id='ethan@openfi.re', parent=ethan, user=ethan, address='ethan@openfi.re', label='d', notify=True, jabber=True, gravatar=True)
            ]
            user_emails = ndb.put_multi(user_emails)

            # user permissions
            user_perms = [
                user.Permissions(id='global', parent=pug, user=pug, moderator=True, admin=True, developer=True),
                user.Permissions(id='global', parent=sam, user=sam, moderator=True, admin=True, developer=True),
                user.Permissions(id='global', parent=david, user=david, moderator=True, admin=True, developer=True),
                user.Permissions(id='global', parent=ethan, user=ethan, moderator=True, admin=True, developer=True)
            ]
            user_perms = ndb.put_multi(user_perms)

            pug = pug.get()
            sam = sam.get()
            david = david.get()
            ethan = ethan.get()

            pug.email = [user_emails[0]]
            sam.email = [user_emails[1]]
            david.email = [user_emails[2]]
            ethan.email = [user_emails[3]]

            pug.permissions = [user_perms[0]]
            sam.permissions = [user_perms[1]]
            david.permissions = [user_perms[2]]
            ethan.permissions = [user_perms[3]]

            pug, sam, david, ethan = tuple(ndb.put_multi([pug, sam, david, ethan]))

            ## categories next
            politics = project.Category(key=ndb.Key(project.Category, 'politics'), slug='politics', name='Politics', description='Having to do with politics.', keywords=['policy', 'government']).put()
            transparency = project.Category(key=ndb.Key(project.Category, 'transparency', parent=politics), slug='transparency', name='Transparency', description='Having to do with open information.', keywords=['politics', 'policy', 'opennes', 'freedom'], parent=politics).put()
            money = project.Category(key=ndb.Key(project.Category, 'money'), slug='money', name='Money', description='Having to do with money or currency.', keywords=['currency', 'tender', 'money', 'debt', 'economies']).put()
            law = project.Category(key=ndb.Key(project.Category, 'law'), slug='law', name='Law', description='Having to do with law or policy.', keywords=['policy', 'law', 'government']).put()
            business = project.Category(key=ndb.Key(project.Category, 'business'), slug='business', name='Business', description='Having to do with commercial enterprise.', keywords=['corporations', 'startups']).put()

            ## proposals third
            fatcatmap = project.Proposal(
                    name='fat cat map',
                    status='a',
                    category=transparency,
                    summary='ever wonder where your local congressman gets his money?',
                    pitch='cool fat pitch herr',
                    tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                    keywords=['transparency', 'politics', 'opendata', 'visualization'],
                    creator=sam,
                    owners=[sam, david],
                    public=True,
                    viewers=[pug, ethan],
                    goals=[
                        project.Goal(amount=1000),
                        project.Goal(amount=10000),
                        project.Goal(amount=100000),
                        project.Goal(amount=500000),
                        project.Goal(amount=1000000)
                    ],
                    tiers=[
                        project.Tier(
                            name='Friend',
                            amount=10,
                            description="We'll give you an invite to the private beta!",
                            delivery=datetime.date(year=2012, month=9, day=1)
                        ),
                        project.Tier(
                            name='Supporter',
                            amount=35,
                            description="Get an FCM <i>Transparency Warrior</i> mug, and an invite to the private beta!",
                            delivery=datetime.date(year=2012, month=9, day=1)
                        ),
                        project.Tier(
                            name='Backer',
                            amount=50,
                            description="Get an FCM <i>Transparency Warrior</i> tote bag, and an invite to the private beta!",
                            delivery=datetime.date(year=2012, month=9, day=1)
                        ),
                        project.Tier(
                            name='Sponsor',
                            amount=100,
                            description="Get both the <i>Transparency Warrior</i> mug and tote bag, and an invite to the private alpha, a <b>full month</b> before our beta release! We'll also list you publicly on our supporters page!",
                            delivery=datetime.date(year=2012, month=8, day=1)
                        ),
                        project.Tier(
                            name='Investor',
                            amount=300,
                            description="Get the mug, tote bag, 5 early alpha invites, and a public listing on our supporters page!",
                            delivery=datetime.date(year=2012, month=8, day=1)
                        ),
                        project.Tier(
                            name='Inner Circle',
                            amount=500,
                            description="Wow, you're passionate about transparency! Get all the swag, 10 early alpha invites, public listing on our supporters page, and the ability to give direct feedback that helps shape fatcatmap!",
                            delivery=datetime.date(year=2012, month=8, day=1)
                        ),
                        project.Tier(
                            name='Transparency Warrior',
                            amount=1000,
                            description="As a critical supporter of the movement, you want to be involved as early and often as possible. Get 50 early alpha invites, public listing, 2x all the swag, and the ability to give direct feedbat that helps shape fatcatmap!",
                            delivery=datetime.date(year=2012, month=7, day=15)
                        ),
                        project.Tier(
                            name='Fat Cat',
                            amount=10000,
                            description="Get any bill you want passed in Congress. Ha ha, just kidding! You're the kind of supporter that <i>makes transparency possible</i>. Because of supporters like you, the fight for sunlight in Washington has hope. You'll get a free lunch with the development team, all of the above, and as many early alpha/beta invites as you can eat!",
                            delivery=datetime.date(year=2012, month=7, day=10)
                        )
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
                    viewers=[pug, sam]
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
                    viewers=[pug, david]
            ).put()

            # then goals + tiers (project sub-artifacts)

            # fourth, projects
            fatcatmap = project.Project(
                    name='fat cat map',
                    status='o',
                    category=transparency,
                    proposal=fatcatmap,
                    summary='ever wonder where your local congressman gets his money?',
                    pitch='cool fat pitch herr',
                    tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                    keywords=['transparency', 'politics', 'opendata', 'visualization'],
                    creator=sam,
                    owners=[sam, david],
                    public=True,
                    viewers=[pug, ethan],
                    progress=73,
                    money=17261
            )
            fatcatmap.put()

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
            )
            seasteading.put()

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
            )
            urbsly.put()

            # project tiers + goals: FATCATMAP
            fatcatmap_goals = [
                project.Goal(parent=fatcatmap.key, amount=1000),
                project.Goal(parent=fatcatmap.key, amount=10000),
                project.Goal(parent=fatcatmap.key, amount=100000),
                project.Goal(parent=fatcatmap.key, amount=500000),
                project.Goal(parent=fatcatmap.key, amount=1000000)
            ]

            fatcatmap_tiers = [
                project.Tier(
                    parent=fatcatmap.key,
                    name='Friend',
                    amount=10,
                    description="We'll give you an invite to the private beta!",
                    delivery=datetime.date(year=2012, month=9, day=1)
                ),
                project.Tier(
                    parent=fatcatmap.key,
                    name='Supporter',
                    amount=35,
                    description="Get an FCM <i>Transparency Warrior</i> mug, and an invite to the private beta!",
                    delivery=datetime.date(year=2012, month=9, day=1)
                ),
                project.Tier(
                    parent=fatcatmap.key,
                    name='Backer',
                    amount=50,
                    description="Get an FCM <i>Transparency Warrior</i> tote bag, and an invite to the private beta!",
                    delivery=datetime.date(year=2012, month=9, day=1)
                ),
                project.Tier(
                    parent=fatcatmap.key,
                    name='Sponsor',
                    amount=100,
                    description="Get both the <i>Transparency Warrior</i> mug and tote bag, and an invite to the private alpha, a <b>full month</b> before our beta release! We'll also list you publicly on our supporters page!",
                    delivery=datetime.date(year=2012, month=8, day=1)
                ),
                project.Tier(
                    parent=fatcatmap.key,
                    name='Investor',
                    amount=300,
                    description="Get the mug, tote bag, 5 early alpha invites, and a public listing on our supporters page!",
                    delivery=datetime.date(year=2012, month=8, day=1)
                ),
                project.Tier(
                    parent=fatcatmap.key,
                    name='Inner Circle',
                    amount=500,
                    description="Wow, you're passionate about transparency! Get all the swag, 10 early alpha invites, public listing on our supporters page, and the ability to give direct feedback that helps shape fatcatmap!",
                    delivery=datetime.date(year=2012, month=8, day=1)
                ),
                project.Tier(
                    parent=fatcatmap.key,
                    name='Transparency Warrior',
                    amount=1000,
                    description="As a critical supporter of the movement, you want to be involved as early and often as possible. Get 50 early alpha invites, public listing, 2x all the swag, and the ability to give direct feedbat that helps shape fatcatmap!",
                    delivery=datetime.date(year=2012, month=7, day=15)
                ),
                project.Tier(
                    parent=fatcatmap.key,
                    name='Fat Cat',
                    amount=10000,
                    description="Get any bill you want passed in Congress. Ha ha, just kidding! You're the kind of supporter that <i>makes transparency possible</i>. Because of supporters like you, the fight for sunlight in Washington has hope. You'll get a free lunch with the development team, all of the above, and as many early alpha/beta invites as you can eat!",
                    delivery=datetime.date(year=2012, month=7, day=10)
                )
            ]

            ndb.put_multi(fatcatmap_goals)
            ndb.put_multi(fatcatmap_tiers)

            fatcatmap.goals = [g.key for g in fatcatmap_goals]
            fatcatmap.tiers = [t.key for t in fatcatmap_tiers]
            fatcatmap.put()

            # fif, assets, avatars + videos
            fcm_avatar = assets.Asset(url='/assets/img/static/projects/cardstock/fatcatmap.png', name='fatcatmap.png', mime='image/png', kind='a', pending=False).put()
            fcm_video = assets.Asset(url='http://www.youtube.com/watch?v=bnyiMnG62OI', name='bnyiMnG62OI', mime='external/youtube', kind='v', pending=False).put()
            ssd_avatar = assets.Asset(url='/assets/img/static/projects/cardstock/seasteading.png', name='seasteading.png', mime='image/png', kind='a', pending=False).put()
            urb_avatar = assets.Asset(url='/assets/img/static/projects/cardstock/urbsly.png', name='urbsly.png', mime='image/png', kind='a', pending=False).put()
            urb_video = assets.Asset(url='http://www.youtube.com/watch?v=bnyiMnG62OI', name='bnyiMnG62OI', mime='external/youtube', kind='v', pending=False).put()

            fcm_media = assets.Avatar(key=ndb.Key(assets.Avatar, fcm_avatar.urlsafe(), parent=fatcatmap.key), version=1, active=True, url='/assets/img/static/projects/cardstock/fatcatmap.png', asset=fcm_avatar, approved=True)
            urb_media = assets.Avatar(key=ndb.Key(assets.Avatar, urb_avatar.urlsafe(), parent=urbsly.key), version=1, active=True, url='/assets/img/static/projects/cardstock/urbsly.png', asset=urb_avatar, approved=True)
            ssd_media = assets.Avatar(key=ndb.Key(assets.Avatar, ssd_avatar.urlsafe(), parent=seasteading.key), version=1, active=True, url='/assets/img/static/projects/cardstock/seasteading.png', asset=ssd_avatar, approved=True)

            fcm_video_media = assets.Video(key=ndb.Key(assets.Video, 'mainvideo', parent=fatcatmap.key), url='https://www.youtube.com/embed/bnyiMnG62OI', asset=fcm_video, provider='youtube', approved=True)
            urb_video_media = assets.Video(key=ndb.Key(assets.Video, 'mainvideo', parent=urbsly.key), url='https://www.youtube.com/embed/rQkTI7XXYvw', asset=urb_video, provider='youtube', approved=True)

            ndb.put_multi([fcm_media, urb_media, ssd_media, fcm_video_media, urb_video_media])

            # finally, custom URLS

            ## projects first
            fcm_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'fatcatmap'), slug='fatcatmap', target=fatcatmap.key)
            ssd_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'seasteading'), slug='seasteading', target=seasteading.key)
            urb_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'urbsly'), slug='urbsly', target=urbsly.key)

            ## then users
            sam_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'sam'), slug='sam', target=sam)
            david_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'david'), slug='david', target=david)
            ethan_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'ethan'), slug='ethan', target=ethan)
            pug_url = assets.CustomURL(key=ndb.Key(assets.CustomURL, 'pug'), slug='pug', target=pug)

            custom_urls = [fcm_url, ssd_url, urb_url, sam_url, david_url, ethan_url, pug_url]

            ndb.put_multi(custom_urls)

            fatcatmap.customurl = fcm_url.key
            seasteading.customurl = ssd_url.key
            urbsly.customurl = urb_url.key

            fatcatmap.avatar = fcm_media.key
            seasteading.avatar = ssd_media.key
            urbsly.avatar = urb_media.key

            fatcatmap.video = fcm_video_media.key
            urbsly.video = urb_video_media.key

            sam_obj = sam.get()
            david_obj = david.get()
            ethan_obj = ethan.get()
            pug_obj = pug.get()

            sam_obj.customurl = sam_url.key
            david_obj.customurl = david_url.key
            ethan_obj.customurl = ethan_url.key
            pug_obj.customurl = pug_url.key

            ndb.put_multi([fatcatmap, seasteading, urbsly, sam_obj, david_obj, ethan_obj, pug_obj])

            system.SystemProperty.set('fixture', 'openfire.dev.BaseDataFixture', has_run=True)

        return self.redirect_to('landing')
