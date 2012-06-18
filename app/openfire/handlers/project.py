# -*- coding: utf-8 -*-
from openfire.handlers import WebHandler


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

        self.render('projects/project_home.html', project_slug=customurl)
        return
