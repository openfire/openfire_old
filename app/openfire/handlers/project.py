# -*- coding: utf-8 -*-
import config
import webapp2
import logging
from openfire.models import user as u
from openfire.models import social as s
from openfire.models import assets as a
from openfire.models import project as p
from openfire.handlers import WebHandler

from google.appengine.ext import ndb


## QueryOptions objects
_keys_only = ndb.QueryOptions(keys_only=True, limit=20, read_policy=ndb.EVENTUAL_CONSISTENCY, produce_cursors=False, hint=ndb.QueryOptions.ANCESTOR_FIRST)
_images_q = ndb.QueryOptions(limit=1, produce_cursors=False, keys_only=True, hint=ndb.QueryOptions.ANCESTOR_FIRST)


## ProjectLanding - page for a listing of projects (`browse`)
class ProjectLanding(WebHandler):

    ''' openfire project landing page. '''

    template = 'projects/project_landing.html'

    def get(self):

        ''' Render project_landing.html. '''

        self.render(self.template)
        return


## ProjectHome - homepage for a project on openfire
class ProjectHome(WebHandler):

    ''' openfire page. '''

    should_log = True       # activate handler-specific logging
    should_cache = False    # activate fullpage caching
    should_preload = False  # whether to activate preloading
    cache_timeout = 1200    # memcache fullpage caching timeout
    template = 'projects/project_home.html'

    @webapp2.cached_property
    def logging(self):

        ''' Named logging pipe. '''

        return super(ProjectHome, self).logging.extend(name='ProjectHome')._setcondition(self.should_log)

    @webapp2.cached_property
    def videoConfig(self):

        ''' Named access to video configuration. '''

        return config.config.get('openfire.video')

    def get(self, key):

        ''' Render project_home.html. '''

        # calculate keys to pull
        pr = ndb.Key(urlsafe=key)
        self.preload_namespace(pr)

        if self.should_cache:
            if self.user:
                mck = '::'.join(['of', 'pagecontent', 'project_home', self.user.key.urlsafe(), pr.urlsafe()])
            else:
                mck = '::'.join(['of', 'pagecontent', 'project_home', '_public_', pr.urlsafe()])
            self.logging.info('Looking in Memcache for project page context at key "%s"...' % mck)
            page_content = self.api.memcache.get(mck)

            if page_content is not None:
                self.logging.info('Found cached page content in memcache!')
                return page_content

            else:
                self.logging.info('Did not find cached page content in memcache. Continuing.')
                page_content = None
        else:
            page_content = None

        if page_content is None:
            vi = ndb.Key(a.Video, 'mainvideo', parent=pr)

            # pull project and attachments
            if not isinstance(self.user, ndb.Model):
                project, video = tuple(ndb.get_multi([pr, vi], use_cache=True, use_memcache=True, use_datastore=True))
                follow = None
            else:
                project, follow, video = tuple(ndb.get_multi([pr, ndb.Key(s.Follow, getattr(self, 'user').key.urlsafe(), parent=pr), vi], use_cache=True, use_memcache=True, use_datastore=True))

            # couldn't find project
            if project is None:
                return self.error(404)

            # pull avatar/asset + video asset
            avatar = a.Avatar.query(ancestor=project.key, default_options=_images_q).filter(a.Avatar.active == True).order(-a.Avatar.modified)
            avatar = avatar.fetch(options=_images_q)
            if len(avatar) > 0 and video is not None:
                avatar = avatar[0]
                avatar, av_asset, vi_asset = tuple(ndb.get_multi([avatar, ndb.Key(urlsafe=avatar.id()), video.asset], use_cache=True, use_memcache=True, use_datastore=True))
                avatar = avatar.to_dict()
                avatar['asset'] = av_asset

                video._asset = vi_asset

            elif video is None and len(avatar) > 0:
                avatar = avatar[0]
                if isinstance(avatar, ndb.Model):
                    asset = avatar.asset
                else:
                    asset = ndb.Key(urlsafe=avatar.id())
                avatar, av_asset = tuple(ndb.get_multi([avatar, ndb.Key(urlsafe=avatar.id())], use_cache=True, use_memcache=True, use_datastore=True))
                avatar = avatar.to_dict()
                avatar['asset'] = asset

            # pull project images
            project_images = []
            placed_images = {}
            images = a.Image.query(ancestor=project.key, default_options=_images_q)
            i_count = images.count()
            if i_count > 0:
                images = ndb.get_multi(images, use_cache=True, use_memcache=True, use_datastore=True)
                for image in images:
                    if len(image.placement) > 0:
                        for placement in image.placement:
                            placed_images[placement] = image
                    project_images.append(image)

            p_images = {'placement': placed_images, 'library': project_images}
            if avatar:
                p_images['avatar'] = avatar['asset']
            else:
                p_images['avatar'] = None

            # pull goals and tiers
            active_goal = project.active_goal and project.active_goal.get() or None
            tiers = []
            next_steps = []
            if active_goal:
                tiers = ndb.get_multi(active_goal.tiers)
                next_steps = ndb.get_multi(active_goal.next_steps)
            completed_goals = ndb.get_multi(project.completed_goals)
            future_goal = project.future_goal.get()

            allowed_viewers = ndb.get_multi(project.owners + project.viewers)

            # make sure the user is allowed to view
            if self.user is not None:
                userkey = self.user.key
            else:
                userkey = None
            if project.is_private() and (userkey not in project.owners) and (userkey not in project.viewers):
                logging.critical('User does not have permissions to view the specified project.')
                if config.debug:
                    return self.error(403)  # 403 in development
                else:
                    return self.error(404)  # 404 for extra ninja stealth in production

            # calculate owners and viewers
            owners, viewers = [], []
            for v in allowed_viewers:
                if v.key in project.owners and not v in owners:
                    owners.append(v)
                elif v.key in project.viewers and not v in viewers:
                    viewers.append(v)

            page_content = self.render(
                    self.template,
                    project=project,
                    follow=follow,
                    video=video,
                    owners=owners,
                    viewers=viewers,
                    avatar=avatar,
                    images=p_images,
                    active_goal=active_goal,
                    completed_goals=completed_goals,
                    future_goal=future_goal,
                    tiers=tiers,
                    next_steps=next_steps,
                    video_config=self.videoConfig,
                    flush=False
            )

            # set pagecontent cache
            if self.should_cache:
                self.api.memcache.set(mck, page_content, self.cache_timeout)

            return self.response.write(page_content)
