# -*- coding: utf-8 -*-
from openfire.models import user
from openfire.models import project
from openfire.handlers import WebHandler

from google.appengine.ext import ndb


class ProjectLanding(WebHandler):

    ''' openfire project landing page. '''

    def get(self):

        ''' Render project_landing.html. '''

        self.render('projects/project_landing.html')
        return


class ProjectHome(WebHandler):

    ''' openfire page. '''

    def get(self, customurl):

        ''' Render project_home.html. '''

        p = project.Project.get_by_id(customurl)
        if p is None:
            ## make up a project real quick
            p = project.Project(**{

                    'key': ndb.Key(project.Project, 'fatcatmap'),
                    'slug': 'fatcatmap',
                    'name': 'fat cat map',
                    'status': 'o',
                    'proposal': ndb.Key(project.Proposal, 'cool'),
                    'category': ndb.Key(project.Category, 'politics'),
                    'summary': 'ever wonder who your local congressman gets his money from? fatcatmap answers that question, with data.',
                    'pitch': 'Cool beans pitch.',
                    'tech': 'Google App Engine, Amazon Web Services, Layer9, AppTools',
                    'keywords': ['politics', 'influence', 'money', 'corruption', 'congress'],
                    'creator': ndb.Key(user.User, 'sam'),
                    'owners': [ndb.Key(user.User, 'sam'), ndb.Key(user.User, 'david')],
                    'public': True,
                    'viewers': []

                })

        self.render('projects/project_home.html', project_slug=customurl, project=p)
        return
