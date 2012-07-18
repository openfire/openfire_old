import hashlib
import datetime
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from apptools import BaseHandler
from webapp2_extras import security as wsec

from openfire.models import system, contribution
from openfire.models import user, project, assets
from openfire.models.indexer import index, entry, map as mapping

from openfire.fixtures import fixture_util as util


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

        uploads = self.get_uploads()

        return self.response.write('<pre>' + str(self.request) + '</pre>')


class DevModels(BaseHandler):

    ''' Quickly insert some dev models for testing. This is NOT meant to be a full, permanent fixture. '''

    force_load_session = False

    def get(self):

        ''' Load the fixtures if they have not already been loaded. '''

        run = True
        flag = system.SystemProperty.get('fixture', 'openfire.dev.BaseDataFixture')
        if flag:
            run = (not flag.has_run)
            if not run:
                return self.redirect_to('landing')

        ## indexer models
        util.build_indexes(['user', 'update', 'project', 'category', 'activity'])

        ## contribution types
        util.create_contribution_type(slug='money', name='Money', unit='dollar', plural='dollars',
                subunit='cent', subunit_plural='cents')
        util.create_contribution_type(slug='time', name='Time', unit='hour', plural='hours',
                subunit='minute', subunit_plural='minutes')
        util.create_contribution_type(slug='code', name='Code', unit='line', plural='lines',
                subunit='line', subunit_plural='line')
        util.create_contribution_type(slug='advocacy', name='Advocacy', unit='dollar', plural='dollars',
                subunit='cent', subunit_plural='cents')

        ## users
        users = {}
        users['pug'] = util.create_user(username='pug', password='pugiscool',
                firstname='David', lastname='Anderson',
                location='San Francisco, CA', bio='hola yo soy pug',
                email='david@openfi.re', create_permissions=True)
        users['sam'] = util.create_user(username='sam', password='samiscool',
                firstname='Sam', lastname='Gammon',
                location='San Francisco, CA', bio='fiesta ayayayay',
                email='samuel.gammon@gmail.com', create_permissions=True)
        users['david'] = util.create_user(username='david', password='davidiscool',
                firstname='David', lastname='Rekow',
                location='San Francisco, CA', bio='hi i is david',
                email='davidr@openfi.re', create_permissions=True)
        users['ethan'] = util.create_user(username='ethan', password='ethaniscool',
                firstname='Ethan', lastname='Leland',
                location='San Francisco, CA', bio='ethan i am',
                email='ethan.leland@gmail.com', create_permissions=True)


        ## categories next
        categories = {}
        categories['politics'] = util.create_category(slug='politics', name='Politics',
                description='Having to do with politics.',
                keywords=['policy', 'government'])
        categories['transparency'] = util.create_category(slug='transparency', name='Transparency',
                description='Having to do with open information.',
                keywords=['politics', 'policy', 'opennes', 'freedom'],
                parent_key=categories['politics'])
        categories['money'] = util.create_category(slug='money', name='Money',
                description='Having to do with money or currency.',
                keywords=['currency', 'tender', 'money', 'debt', 'economies'])
        categories['law'] = util.create_category(slug='law', name='Law',
                description='Having to do with law or policy.',
                keywords=['policy', 'law', 'government'])
        categories['business'] = util.create_category(slug='business', name='Business',
                description='Having to do with commercial enterprise.',
                keywords=['corporations', 'startups'])


        ## proposals third
        proposals = {}
        proposals['fatcatmap'] = util.create_proposal(
                name='fat cat map',
                status='a',
                public=True,
                summary='ever wonder where your local congressman gets his money?',
                pitch='cool fat pitch herr',
                tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                keywords=['transparency', 'politics', 'opendata', 'visualization'],
                category=categories['transparency'],
                creator=users['sam'],
                owners=[users['sam'], users['david']],
                viewers=[users['pug'], users['ethan']],
                goals=[
                    {'amount': 1000},
                    {'amount': 10000},
                    {'amount': 50000},
                    {'amount': 100000},
                ],
                tiers=[
                    {
                        'name': 'Friend',
                        'amount': 10,
                        'description': "We'll give you an invite to the private beta!",
                        'delivery': str(datetime.date(year=2012, month=9, day=1))
                    },
                    {
                        'name': 'Supporter',
                        'amount': 35,
                        'description': "Get an FCM <i>Transparency Warrior</i> mug, and an invite to the private beta!",
                        'delivery': str(datetime.date(year=2012, month=9, day=1))
                    },
                    {
                        'name': 'Backer',
                        'amount': 50,
                        'description': "Get an FCM <i>Transparency Warrior</i> tote bag, and an invite to the private beta!",
                        'delivery': str(datetime.date(year=2012, month=9, day=1))
                    },
                    {
                        'name': 'Sponsor',
                        'amount': 100,
                        'description': "Get both the <i>Transparency Warrior</i> mug and tote bag, and an invite to the private alpha, a <b>full month</b> before our beta release! We'll also list you publicly on our supporters page!",
                        'delivery': str(datetime.date(year=2012, month=8, day=1))
                    },
                    {
                        'name': 'Investor',
                        'amount': 300,
                        'description': "Get the mug, tote bag, 5 early alpha invites, and a public listing on our supporters page!",
                        'delivery': str(datetime.date(year=2012, month=8, day=1))
                    },
                    {
                        'name': 'Inner Circle',
                        'amount': 500,
                        'description': "Wow, you're passionate about transparency! Get all the swag, 10 early alpha invites, public listing on our supporters page, and the ability to give direct feedback that helps shape fatcatmap!",
                        'delivery': str(datetime.date(year=2012, month=8, day=1))
                    },
                    {
                        'name': 'Transparency Warrior',
                        'amount': 1000,
                        'description': "As a critical supporter of the movement, you want to be involved as early and often as possible. Get 50 early alpha invites, public listing, 2x all the swag, and the ability to give direct feedbat that helps shape fatcatmap!",
                        'delivery': str(datetime.date(year=2012, month=7, day=15))
                    },
                    {
                        'name': 'Fat Cat',
                        'amount': 10000,
                        'description': "Get any bill you want passed in Congress. Ha ha, just kidding! You're the kind of supporter that <i>makes transparency possible</i>. Because of supporters like you, the fight for sunlight in Washington has hope. You'll get a free lunch with the development team, all of the above, and as many early alpha/beta invites as you can eat!",
                        'delivery': str(datetime.date(year=2012, month=7, day=10))
                    },
                ]
        )

        proposals['seasteading'] = util.create_proposal(
                name='SeaSteading',
                status='a',
                category=categories['law'],
                summary='ever take issue with H1B visa policy in the united states! well then help us buy a cruise ship.',
                pitch='cool sea pitch herr',
                tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                keywords=['business', 'law', 'policy'],
                creator=users['david'],
                owners=[users['david'], users['ethan']],
                public=True,
                viewers=[users['pug'], users['sam']]
        )

        urbsly = util.create_proposal(
                name='urbsly',
                status='a',
                category=categories['business'],
                summary='ever hate on monsanto a bunch? duke on them some more with this thing',
                pitch='cool urbs pitch herr',
                tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                keywords=['ecology', 'seeds-and-shit', 'yup'],
                creator=users['ethan'],
                owners=[users['ethan'], users['sam']],
                public=True,
                viewers=[users['pug'], users['david']]
        )

        # then goals + tiers (project sub-artifacts)

        # fourth, projects
        projects = {}
        projects['fatcatmap'] = util.create_project(
                name='fat cat map',
                status='o',
                category=categories['transparency'],
                proposal=proposals['fatcatmap'],
                summary='ever wonder where your local congressman gets his money?',
                pitch='cool fat pitch herr',
                tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                keywords=['transparency', 'politics', 'opendata', 'visualization'],
                creator=users['sam'],
                owners=[users['sam'], users['david']],
                public=True,
                viewers=[users['pug'], users['ethan']],
                progress=73,
                money=17261,
        )

        projects['seasteading'] = util.create_project(
                name='SeaSteading',
                status='o',
                category=categories['law'],
                proposal=proposals['seasteading'],
                summary='ever take issue with H1B visa policy in the united states! well then help us buy a cruise ship.',
                pitch='cool sea pitch herr',
                tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                keywords=['business', 'law', 'policy'],
                creator=users['david'],
                owners=[users['david'], users['ethan']],
                public=True,
                viewers=[users['pug'], users['sam']],
        )

        projects['urbsly'] = util.create_project(
                name='urbsly',
                status='o',
                category=categories['business'],
                proposal=urbsly,
                summary='ever hate on monsanto a bunch? duke on them some more with this thing',
                pitch='cool urbs pitch herr',
                tech='Google App Engine, Amazon AWS, Layer9, AppTools',
                keywords=['ecology', 'seeds-and-shit', 'yup'],
                creator=users['ethan'],
                owners=[users['ethan'], users['sam']],
                public=True,
                viewers=[users['pug'], users['david']],
        )

        # project tiers + goals for fatcatmap
        util.create_goal(parent_key=projects['fatcatmap'], amount=1000)
        util.create_goal(parent_key=projects['fatcatmap'], amount=10000)
        util.create_goal(parent_key=projects['fatcatmap'], amount=100000)
        util.create_goal(parent_key=projects['fatcatmap'], amount=500000)
        util.create_goal(parent_key=projects['fatcatmap'], amount=1000000)

        util.create_tier(
            parent_key=projects['fatcatmap'],
            name='Friend',
            amount=10,
            description="We'll give you an invite to the private beta!",
            delivery=str(datetime.date(year=2012, month=9, day=1))
        )
        util.create_tier(
            parent_key=projects['fatcatmap'],
            name='Supporter',
            amount=35,
            description="Get an FCM <i>Transparency Warrior</i> mug, and an invite to the private beta!",
            delivery=str(datetime.date(year=2012, month=9, day=1)),
        )
        util.create_tier(
            parent_key=projects['fatcatmap'],
            name='Backer',
            amount=50,
            description="Get an FCM <i>Transparency Warrior</i> tote bag, and an invite to the private beta!",
            delivery=str(datetime.date(year=2012, month=9, day=1)),
        )
        util.create_tier(
            parent_key=projects['fatcatmap'],
            name='Sponsor',
            amount=100,
            description="Get both the <i>Transparency Warrior</i> mug and tote bag, and an invite to the private alpha, a <b>full month</b> before our beta release! We'll also list you publicly on our supporters page!",
            delivery=str(datetime.date(year=2012, month=9, day=1)),
        )
        util.create_tier(
            parent_key=projects['fatcatmap'],
            name='Investor',
            amount=300,
            description="Get the mug, tote bag, 5 early alpha invites, and a public listing on our supporters page!",
            delivery=str(datetime.date(year=2012, month=9, day=1)),
        )
        util.create_tier(
            parent_key=projects['fatcatmap'],
            name='Inner Circle',
            amount=500,
            description="Wow, you're passionate about transparency! Get all the swag, 10 early alpha invites, public listing on our supporters page, and the ability to give direct feedback that helps shape fatcatmap!",
            delivery=str(datetime.date(year=2012, month=9, day=1)),
        )
        util.create_tier(
            parent_key=projects['fatcatmap'],
            name='Transparency Warrior',
            amount=1000,
            description="As a critical supporter of the movement, you want to be involved as early and often as possible. Get 50 early alpha invites, public listing, 2x all the swag, and the ability to give direct feedbat that helps shape fatcatmap!",
            delivery=str(datetime.date(year=2012, month=7, day=15)),
        )
        util.create_tier(
            parent_key=projects['fatcatmap'],
            name='Fat Cat',
            amount=10000,
            description="Get any bill you want passed in Congress. Ha ha, just kidding! You're the kind of supporter that <i>makes transparency possible</i>. Because of supporters like you, the fight for sunlight in Washington has hope. You'll get a free lunch with the development team, all of the above, and as many early alpha/beta invites as you can eat!",
            delivery=str(datetime.date(year=2012, month=7, day=10)),
        )

        # fif, assets, avatars + videos
        util.create_avatar(parent_key=projects['fatcatmap'], url='/assets/img/static/projects/cardstock/fatcatmap.png',
                name='fatcatmap.png', mime='image/png')
        util.create_video(parent_key=projects['fatcatmap'], url='http://www.youtube.com/embed/bnyiMnG62OI',
                name='bnyiMnG62OI', mime='external/youtube', provider='youtube')

        util.create_avatar(parent_key=projects['seasteading'], url='/assets/img/static/projects/cardstock/seasteading.png',
                name='seasteading.png', mime='image/png')

        util.create_avatar(parent_key=projects['urbsly'], url='/assets/img/static/projects/cardstock/urbsly.png',
                name='urbsly.png', mime='image/png')
        util.create_video(parent_key=projects['urbsly'], url='https://www.youtube.com/embed/rQkTI7XXYvw',
                name='bnyiMnG62OI', mime='external/youtube', provider='youtube')


        # finally, custom URLS
        util.create_custom_url(slug='sam', target_key=users['sam'])
        util.create_custom_url(slug='david', target_key=users['david'])
        util.create_custom_url(slug='ethan', target_key=users['ethan'])
        util.create_custom_url(slug='pug', target_key=users['pug'])
        util.create_custom_url(slug='fatcatmap', target_key=projects['fatcatmap'])
        util.create_custom_url(slug='seasteading', target_key=projects['seasteading'])
        util.create_custom_url(slug='urbsly', target_key=projects['urbsly'])

        system.SystemProperty.set('fixture', 'openfire.dev.BaseDataFixture', has_run=True)

        return self.redirect_to('landing')
