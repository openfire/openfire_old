# -*- coding: utf-8 -*-
from config import config
from openfire.models import user
from openfire.models import assets

from apptools import BaseHandler
from openfire.handlers import WebHandler


class Login(WebHandler):

    ''' Default login handler - redirect using App Engine's users API, if available. '''

    def get(self):

        try:
            login_url = self.api.users.create_login_url(self.request.environ.get('HTTP_REFERRER', '/'))
            if login_url is not None:
                return self.redirect(login_url)

        except:
            self.error(404)
            return


class Logout(WebHandler):

    ''' Default logout handler - redirect using App Engine's users API, if available. '''

    def get(self):

        try:
            logout_url = self.api.users.create_logout_url(self.request.environ.get('HTTP_REFERRER', '/'))
            if logout_url is not None:
                return self.redirect(logout_url)

        except:
            self.error(404)
            return


class Signup(BaseHandler):

    ''' Default signup handler - return 404 by default. '''

    def get(self):

        ''' Dev signup handler. Will need to be rewritten with an actual registration form. '''

        # if they aren't logged in, redirect
        u = self.api.users.get_current_user()
        if u is None:
            return self.redirect_to('auth/login')

        # make sure user doesn't already exist
        pu = user.User.get_by_id(u.email())
        if pu is None:
            if config.debug:
                # only autoregister on the devserver
                self.response.write('Autoregistering...<br />')

                username, domain = tuple(u.email().split('@'))

                # make user
                u = user.User(id=u.email(), user=u, username=u.nickname(), firstname='John', lastname='Doe', bio='You are cool')
                ukey = u.put()

                # make customurl
                curl = assets.CustomURL(id=username, slug=username, target=ukey)
                curl.put()
                u.customurl = curl
                u.put()

                # make email
                em = user.EmailAddress(id=u.email(), parent=ukey, user=ukey, address=u.email(), label='d', notify=True, jabber=True, gravatar=True)
                em.put()

                # make permissions
                pm = user.Permissions(id='global', parent=ukey, user=ukey, moderator=True, admin=True, developer=True)
                pm.put()

                self.response.write('<b>Done. Redirecting.</b>')
                return self.redirect_to('landing')
        else:
            return self.redirect_to('landing')
