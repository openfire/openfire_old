# -*- coding: utf-8 -*-
import config
import logging
from openfire.models import user as u
from openfire.models import assets as a
from openfire.models import project as p
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

    def get(self, key):

        ''' Render project_home.html. '''

        # calculate keys to pull
        pr = ndb.Key(urlsafe=key)
        vi = ndb.Key(a.Video, 'mainvideo', parent=pr)

        # pull project and attachments
        project, video = tuple(ndb.get_multi([pr, vi], use_cache=True, use_memcache=True, use_datastore=True))
        _keys_only = ndb.QueryOptions(keys_only=True, limit=20, read_policy=ndb.EVENTUAL_CONSISTENCY, produce_cursors=False)

        # pull avatar, tiers and goals
        tiers = p.Tier.query(ancestor=project.key).order(p.Tier.amount)
        goals = p.Goal.query(ancestor=project.key).order(p.Goal.amount)
        avatar = a.Avatar.query(ancestor=project.key).filter(a.Avatar.active == True).filter(a.Avatar.active == True).order(-a.Avatar.modified)
        avatar = avatar.get(options=ndb.QueryOptions(limit=1, projection=('url', 'asset'), read_policy=ndb.EVENTUAL_CONSISTENCY, produce_cursors=False))
        if avatar is not None:
            asset = avatar.asset.get()
            avatar = avatar.to_dict()
            avatar['asset'] = asset

        # 404 if project not found
        if project is None:
            return self.error(404)

        allowed_viewers = ndb.get_multi(project.owners + project.viewers)

        # make sure the user is allowed to view
        if project.is_private() and (self.user.key not in project.owners) and (self.user.key not in project.viewers):
            logging.critical('User does not have permissions to view the specified project.')
            if config.debug:
                return self.error(403)
            else:
                return self.error(404)

        # calculate owners and viewers
        owners, viewers = [], []
        for v in allowed_viewers:
            if v.key in project.owners:
                owners.append(v)
            elif v.key in project.viewers:
                viewers.append(v)

        if project is None:
            return self.error(404)
        else:
            self.render(
                'projects/project_home.html',
                project=project,
                video=video,
                owners=owners,
                viewers=viewers,
                avatar=avatar,
                goals=ndb.get_multi(goals.fetch(options=_keys_only)),
                tiers=ndb.get_multi(tiers.fetch(options=_keys_only))
            )
            return






