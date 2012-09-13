# -*- coding: utf-8 -*-
import config
import webapp2
import logging
from google.appengine.ext import ndb

from openfire.handlers import WebHandler
from openfire.models.project import Category


class ProposeLanding(WebHandler):

    ''' openfire proposal landing page. '''

    def get(self):

        ''' Render propose_landing.html. '''

        context = {
            'categories': Category.query().fetch(),
        }
        self.render('propose/proposal_landing.html', **context)
        return


class ProposalHome(WebHandler):

    ''' openfire proposal home page. '''

    should_log = True       # activate handler-specific logging
    should_cache = False    # activate fullpage caching
    cache_timeout = 1200    # memcache fullpage caching timeout
    template = 'propose/proposal_home.html'

    @webapp2.cached_property
    def logging(self):

        ''' Named logging pipe. '''

        return super(ProposalHome, self).logging.extend(name='ProposalHome')._setcondition(self.should_log)

    def get(self, key):

        ''' Render proposal_home.html. '''

        # calculate keys to pull
        pr = ndb.Key(urlsafe=key)
        self.preload_namespace(pr)

        if self.should_cache:
            if self.user:
                mck = '::'.join(['of', 'pagecontent', 'proposal_home', self.user.key.urlsafe(), pr.urlsafe()])
            else:
                mck = '::'.join(['of', 'pagecontent', 'proposal_home', '_public_', pr.urlsafe()])
            self.logging.info('Looking in Memcache for proposal page context at key "%s"...' % mck)
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

            # pull proposal
            proposal = pr.get(use_cache=True, use_memcache=True, use_datastore=True)

            # couldn't find proposal
            if proposal is None:
                return self.error(404)

            allowed_viewers = ndb.get_multi(proposal.owners + proposal.viewers)

            # make sure the user is allowed to view
            if self.user is not None:
                userkey = self.user.key
            else:
                userkey = None

            if not proposal.public and (userkey not in proposal.owners) and (userkey not in proposal.viewers):
                logging.critical('User does not have permissions to view the specified proposal.')
                if config.debug:
                    return self.error(403)  # 403 in development
                else:
                    return self.error(404)  # 404 for extra ninja stealth in production

            # calculate owners and viewers
            owners, viewers = [], []
            for v in allowed_viewers:
                if v.key in proposal.owners:
                    owners.append(v)
                elif v.key in proposal.viewers:
                    viewers.append(v)

            page_content = self.render(
                    self.template,
                    proposal=proposal,
                    owners=owners,
                    viewers=viewers,
                    flush=False
            )

            # set pagecontent cache
            if self.should_cache:
                self.api.memcache.set(mck, page_content, self.cache_timeout)

            return self.response.write(page_content)
