# -*- coding: utf-8 -*-
from openfire.models import user
from openfire.models import assets
from openfire.models import project
from google.appengine.ext import ndb
from openfire.handlers import WebHandler
from openfire.handlers.project import ProjectHome
from openfire.handlers.user import UserProfile


class Landing(WebHandler):

    ''' openfire landing page. '''

    def get(self):

        ''' Render landing.html or landing_noauth.html. '''

        ## fetch projects
        master_key_list = []
        pq = project.Project.query().order(project.Project.name)
        pc = pq.count()

        context = {
        }

        if pc > 0:
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


            context['projects'] = projects

        if False:
            self.render('main/landing_noauth.html', **context)
        else:
            self.render('main/landing.html', **context)
        return


class CustomUrlHandler(WebHandler):

    ''' openfire custom url handling. '''

    # For now we only support projects and user profiles.
    _project_handler_class = ProjectHome
    _user_handler_class = UserProfile

    def get(self, customurl):

        ''' Render the class defined by the target object, or a 404 page. '''

        url_key = ndb.Key('CustomURL', customurl)
        url_object = url_key.get()
        if not url_object:
            return self.error(404) # Failed to find custom url

        kind = url_object.target.kind()
        context = {}
        handler = None
        if kind not in ('Project', 'User'):
            return self.error(404) # Invalid kind

        elif kind == 'Project':
            handler = self._project_handler_class()
            context['key'] = url_object.target.urlsafe()

        elif kind == 'User':
            handler = self._user_handler_class()
            context['username'] = url_object.target.id()

        if not handler:
            return self.error(500) # Failed to instantiate handler?

        # Initialize the new handler with the current request and response.
        handler.initialize(self.request, self.response)
        return handler.get(**context)
