# -*- coding: utf-8 -*-
from openfire.models import assets
from openfire.models import project
from google.appengine.ext import ndb
from openfire.handlers import WebHandler


class Landing(WebHandler):

    ''' openfire landing page. '''

    def get(self):

        ''' Render landing.html or landing_noauth.html. '''

        ## fetch projects
        master_key_list = []
        pq = project.Project.query().order(project.Project.name)
        projects = pq.fetch(pq.count(), keys_only=True)

        for pk in projects:

            # append project key and generate subkeys
            master_key_list.append(pk)
            master_key_list.append(ndb.Key(assets.Avatar, 'current', parent=pk))

        ## prepare media
        projects = {}
        data = ndb.get_multi(master_key_list, use_cache=True, use_memcache=True, use_datastore=True)
        for key, entity in zip(master_key_list, data):
            if key.kind() == 'Project':
                projects[key.id()] = entity
            elif key.kind() == 'Media':
                projects[key.parent().id()].avatar = entity.url

        projects = [v for k, v in projects.items()]

        context = {
            'projects': projects
        }

        if False:
            self.render('main/landing_noauth.html', **context)
        else:
            self.render('main/landing.html', **context)
        return
