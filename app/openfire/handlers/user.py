# -*- coding: utf-8 -*-
import webapp2
from google.appengine.ext import ndb
from openfire.handlers import WebHandler
from openfire.models.user import User
from openfire.models.payment import WePayUserPaymentAccount, WePayProjectAccount


class UserLanding(WebHandler):

    ''' openfire user landing page. '''

    def get(self):

        ''' Render user_landing.html. '''

        self.render('user/user_landing.html')
        return


class UserProfile(WebHandler):

    ''' openfire user profile page. '''

    subject = None
    has_edit_privs = False
    is_current_user = False

    should_cache = False
    should_preload = False
    template = 'user/profile.html'

    @webapp2.cached_property
    def _preload(self):

        ''' Preload routine that loads subject user data asynchronously before the handler's HTTP method is run. '''

        return

    def get(self, username=None, key=None):

        ''' Render profile.html. '''

        # coming in from "/me"...
        if username is None and key is None:

            self.logging.info('User coming in on "/me" shortcut...')

            # if there is no user logged in
            if self.user is None:

                self.logging.info('No user logged in. Redirecting to auth/login.')

                # forward to login page, with /me as a continue URL
                self.session['continue_url'] = self.url_for('user/me')
                return self.redirect_to('auth/login')

            else:

                # get the username and redirect to their custom URL
                customurl = self.user.get_custom_url()
                if customurl is not None:
                    self.logging.info('Resolved user, forwarding to existing custom URL.')
                    return self.redirect_to('custom_url', customurl=customurl)

                # if they don't have a custom URL
                else:

                    # if they are unactivated, send them to their opaque URL (their username shouldn't exist yet)
                    if hasattr(self.user, 'activated') and (not self.user.activated):
                        self.logging.warning('User has not activated their account. Forwarding to opaque profile URL.')
                        return self.redirect_to('user/profile/bykey', key=self.encrypt(self.user.key.urlsafe()))

                    # if they are activated but have no custom URL, send them to their username-based URL
                    self.logging.info('User has no custom URL. Forwarding to username-based profile URL.')
                    return self.redirect_to('user/profile', username=self.user.username)

        # coming in from /user/ahblablasamplekey (opaque profile URL)
        elif username is None and key is not None:

            # if there is no user logged in
            if self.user is None:
                return self.error(404)  # only admins and the unactivated user can see their profile

            else:

                # construct the user key
                try:
                    constructed_key = ndb.Key(urlsafe=self.decrypt(key))

                except Exception, e:
                    self.logging.error('Failed to construct invalid URLSafed user key. Bad key: "%s".' % key)
                    return self.error(404)

                # if the person is an admin or the user in question, let them in
                if (self.permissions is not None and self.permissions.admin is True) or (self.user.key == constructed_key):
                    self.has_edit_privs = True

                    if self.user.key == constructed_key:
                        self.is_current_user = True

                    self.subject = constructed_key.get(use_cache=True, use_memcache=True, use_datastore=True)

                else:
                    return self.error(404)  # only admins and the subject unactivated user can see their profile

        # coming in from custom URL or username-based URL
        elif username is not None:

            # resolve subject user
            u = User.query().filter(User.username == username).fetch(options=ndb.QueryOptions(**{
                'limit': 1,
                'produce_cursors': False,
                'deadline': 3
            }))

            # copy to self or 404
            if u is not None:
                if isinstance(u, list) and len(u) > 0:
                    self.subject = u[0]
                else:
                    # user not found :(
                    return self.error(404)
            else:
                return self.error(404)

            # if there is no user logged in
            if self.user is None:

                if hasattr(self.subject, 'public') and self.subject.public is False:
                    return self.error(404)  # there is no logged in user and the profile is private, so 404

            # there is a user logged in
            else:
                # if the currently logged in user is an admin, or the user is looking at their own profile, give them edit privs
                if (self.permissions is not None and self.permissions.admin is True) or (self.user.key == self.subject.key):
                    self.has_edit_privs = True

                    if self.user.key == self.subject.key:
                        self.is_current_user = True
                else:
                    if hasattr(self.subject, 'public'):
                        if not self.subject.public:
                            # user has a private profile
                            return self.error(404)

        context = {
            'user': self.subject,
            'edit_privs': self.has_edit_privs,
            'is_current_user': self.is_current_user
        }

        ## all routing logic complete - build a user's profile objects and render
        return self.render('user/profile.html', **context)


class UserAccount(WebHandler):

    ''' openfire user account page. '''

    def get(self, username):

        ''' Render account.html. '''

        # if there is no user logged in
        if self.user is None:

            self.logging.info('No user logged in on settings page. Redirecting to auth/login.')

            # forward to login page, with /me as a continue URL
            if self.session:
                self.session['continue_url'] = self.url_for('user/me')
            return self.redirect_to('auth/login')

        wepay_account = None
        project_accounts = []
        wepay_accounts = WePayUserPaymentAccount.query(WePayUserPaymentAccount.user == self.user.key).fetch()
        if wepay_accounts and len(wepay_accounts):
            # Currently we only allow one WePay account per user.
            wepay_account = wepay_accounts[0]
            project_accounts = WePayProjectAccount.query(WePayProjectAccount.payment_account.IN([a.key for a in wepay_accounts])).fetch()

        context = {
            'user': self.user,
            'wepay_account': wepay_account,
            'project_accounts': project_accounts,
        }

        self.render('user/account.html', **context)
        return
