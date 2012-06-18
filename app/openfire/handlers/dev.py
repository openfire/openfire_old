from openfire.models import user, project, assets
from openfire.handlers import WebHandler

from google.appengine.ext import ndb


class DevModels(WebHandler):

    ''' Quickly insert some dev models for testing. This is NOT meant to be a full, permanent fixture. '''

    def get(self):

        ''' Insert a couple of categories, a couple of proposals + projects, a couple of users, and we're good. '''

        ## users first
        pug = user.User(key=ndb.Key(user.User, 'pug'), username='pug', firstname='David', lastname='Anderson', bio='hola yo soy pug').put()
        sam = user.User(key=ndb.Key(user.User, 'sam'), username='sam', firstname='Sam', lastname='Gammon', bio='fiesta ayayayay').put()
        david = user.User(key=ndb.Key(user.User, 'david'), username='david', firstname='David', lastname='Rekow', bio='hi i is david').put()
        ethan = user.User(key=ndb.Key(user.User, 'ethan'), username='ethan', firstname='Ethan', lastname='Leland', bio='i am mister ethan').put()

        users = [pug, sam, david, ethan]

        ## categories next
        politics = project.Category(key=ndb.Key(project.Category, 'politics'), slug='politics', name='Politics', description='Having to do with politics.', keywords=['policy', 'government']).put()
        transparency = project.Category(key=ndb.Key(project.Category, 'transparency', parent=politics), slug='transparency', name='Transparency', description='Having to do with open information.', keywords=['politics', 'policy', 'opennes', 'freedom']).put()
        money = project.Category(key=ndb.Key(project.Category, 'money'), slug='money', name='Money', description='Having to do with money or currency.', keywords=['currency', 'tender', 'money', 'debt', 'economies']).put()
        law = project.Category(key=ndb.Key(project.Category, 'law'), slug='law', name='Law', description='Having to do with law or policy.', keywords=['policy', 'law', 'government']).put()
        business = project.Category(key=ndb.Key(project.Category, 'business'), slug='business', name='Business', description='Having to do with commercial enterprise.', keywords=['corporations', 'startups']).put()

        categories = [politics, transparency, money, law, business]

        ## proposals third
        fatcatmap = project.Proposal(
                key=ndb.Key(project.Proposal, 'fatcatmap'),
                slug='fatcatmap',
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
                viewers=[pug, ethan]
        ).put()

        seasteading = project.Proposal(
                key=ndb.Key(project.Proposal, 'seasteading'),
                slug='seasteading',
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
                key=ndb.Key(project.Proposal, 'urbsly'),
                slug='urbsly',
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

        proposals = [fatcatmap, seasteading, urbsly]

        # fourth, projects
        fatcatmap = project.Project(
                key=ndb.Key(project.Project, 'fatcatmap'),
                slug='fatcatmap',
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
                key=ndb.Key(project.Project, 'seasteading'),
                slug='seasteading',
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
                key=ndb.Key(project.Project, 'urbsly'),
                slug='urbsly',
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

        # finally - assets, avatars + videos
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

        return
