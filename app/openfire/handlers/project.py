# -*- coding: utf-8 -*-
from openfire.models import user
from openfire.models import assets
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

        p = ndb.Key(project.Project, customurl)
        a = ndb.Key(assets.Avatar, 'current', parent=p)
        v = ndb.Key(assets.Video, 'mainvideo', parent=p)

        models = ndb.get_multi([p, a, v], use_cache=True, use_memcache=True, use_datastore=True)

        if models[0] is None:
            return self.error(404)
        else:
            self.render('projects/project_home.html', project_slug=customurl, project=models[0], video=models[2], avatar=models[1])
            return
