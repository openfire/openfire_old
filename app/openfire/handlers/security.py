# -*- coding: utf-8 -*-
import time
import webapp2
import logging
import hashlib
import config as cfg
from config import config
from openfire.models import user as user_models
from openfire.models import assets
from openfire.handlers import WebHandler
from google.appengine.ext import ndb

import json
from webapp2_extras import security as wsec


class SecurityConfigProvider(object):

    ''' A security handler. '''

    @webapp2.cached_property
    def _securityConfig(self):

        ''' Cached shortcut to security config. '''

        return config.get('openfire.security')

    @webapp2.cached_property
    def _metaConfig(self):

        ''' Cached shortcut to meta config. '''

        return config.get('openfire.meta')

    def _resolveProvider(self, name):

        ''' Resolve a security provider's settings. '''

        for p in self._securityConfig.get('authentication', {}).get('federation', {}).get('providers'):
            if p.get('name') == name:
                return p
        return None


class Login(WebHandler, SecurityConfigProvider):

    ''' Default login handler - redirect using App Engine's users API, if available. '''

    def do_auth_redirect(self, url):

        ''' Redirect to a third party provider. '''

        logging.info('AUTH: Redirecting to provider URL "%s".' % url)
        return self.redirect(url)

    def via_facebook(self):

        ''' Redirect the user to Facebook-based login. '''

        return self.do_auth_redirect(
            "https://www.facebook.com/dialog/oauth?client_id=%(appid)s&redirect_uri=%(callback)s&scope=%(scope)s&state=%(state)s" % {

                # appID and sessionID
                'appid': self._metaConfig.get('opengraph', {}).get('facebook', {}).get('app_id', False),
                'state': self.encrypt(self.session.get('sid')),

                # scopes and callback
                'scope': ','.join([scope.get('name') for scope in self._resolveProvider('facebook').get('scopes', []) if scope.get('enabled', False)]),
                'callback': ''.join([
                                self.request.environ.get('HTTP_SCHEME', 'HTTP').lower(), '://',
                                self.request.environ.get('HTTP_HOST', 'localhost:8080'),
                                self.url_for('auth/action-provider', action='callback', provider='facebook', csrf=hashlib.sha1(self.session.get('sid')).hexdigest(), ofsid=self.encrypt(self.session.get('sid')))
                            ])

        })

    def via_google(self):

        ''' Redirect the user to Google-based login. '''

        if 'staging' in self.request.environ.get('HTTP_HOST'):
            return self.do_auth_redirect(*[                
                self.url_for('auth/action-provider', action='callback', provider='googleplus', csrf=hashlib.sha256(self.session.get('sid')).hexdigest(), ofsid=self.encrypt(self.session.get('sid')))
            ])

        return self.do_auth_redirect(*[

            self.api.users.create_login_url(

                # google auth callback
                self.url_for('auth/action-provider', action='callback', provider='googleplus', csrf=hashlib.sha256(self.session.get('sid')).hexdigest(), ofsid=self.encrypt(self.session.get('sid'))),

                # federated identity endpoint
                federated_identity=self._resolveProvider('googleplus').get('endpoint')

            )
        ])

    def via_twitter(self):

        ''' Redirect the user to Twitter-based login. '''

        return self.do_auth_redirect(*[

            ""

        ])

    def get(self, provider=None):

        ''' Render the login page, or forward the user to AppEngine login. '''

        ## prepare page context
        context = {
            'meta_config': self._metaConfig,
            'security_config': self._securityConfig
        }

        ## federated logon display ERROR CODES
        if self.request.get('fder'):
            context['federated_error'] = {

                'authorization_denied': "Authorization was denied!",
                'access_token_fail': "Something went wrong! Try again."

            }.get(self.request.get('fder'))
            return self.render('security/login.html', **context)

        ## copy over continue URL
        if 'continue' in self.request.params:
            self.session['continue_url'] = self.request.params.get('continue')

        ## do routing
        if provider is not None:
            logging.info('AUTH: User requested federated logon from provider "%s".' % provider)
            return {

                # run code for whatever provider we're doing
                'facebook': self.via_facebook,
                'googleplus': self.via_google,
                'twitter': self.via_twitter

            }.get(provider, lambda: self.error(404))()

        else:

            ## Simple logon: appengine basic
            if self._securityConfig.get('authentication', {}).get('federation', {}).get('simple', False):
                ## fallback to appengine-based logon
                try:
                    logging.info('AUTH: Decided on simple logon.')
                    login_url = self.api.users.create_login_url(self.request.environ.get('HTTP_REFERRER', '/'))
                    if login_url is not None:
                        return self.redirect(login_url)

                except:
                    ## wat do
                    self.error(404)
                    return

        ## Render login page
        return self.render('security/login.html', **context)

    def post(self):

        ''' Organic logon '''

        ## prepare page context
        context = {
            'meta_config': self._metaConfig,
            'security_config': self._securityConfig
        }

        logging.info('AUTH: Processing organic logon request.')

        ## return error for too many failed logins
        if 'bad_logon_count' in self.session and (self.session.get('bad_logon_count', 0) > 0):
            if self._securityConfig.get('config', {}).get('bad_logon_limit', 0) < self.session.get('bad_logon_count'):

                logging.error('AUTH: User exceeded bad login count. Ratelimiting.')

                context['error'] = 'You have been ratebanned.'
                return self.render('security/login.html', **context)

        ## pick up the form
        if 'username' in self.request.params and 'password' in self.request.params:

            try:
                hashed_password = wsec.hash_password(self.request.params.get('password'), 'sha256', wsec.generate_random_string(length=32, pool=wsec.ASCII_PRINTABLE), 'openfire-internal')
                user_key = ndb.Key(user_models.User, self.request.params.get('username'))
            except NotImplementedError:
                context['error'] = 'Woops! Something went wrong. Please try again.'
                return self.render('security/login.html', **context)
            else:
                logging.info('AUTH: Calculated user key "%s".' % user_key)

                # resolve user by username
                user = user_key.get()

                # user found?
                if user is not None:

                    logging.info('AUTH: User found at username "%s".' % user.username)

                    # password match?
                    if user.password == hashed_password:

                        logging.info('AUTH: Passwords match. Logon successful.')

                        # log them in
                        self.build_authenticated_session(
                            email=user.key.id(),
                            nickname=' '.join([user.firstname, user.lastname]),
                            ukey=user.key.urlsafe(),
                            uid=user.key.id()
                        )

                        if 'bad_logon_count' in self.session:
                            self.session['bad_logon_count'] = 0

                        # redirect them on
                        if self.session.get('continue_url'):
                            logging.info('AUTH: Continue URL found. Redirecting to "%s".' % self.session.get('continue_url'))
                            return self.redirect(self.session.get('continue_url'))
                        else:
                            logging.info('AUTH: No continue URL found. Redirecting to landing.')
                            return self.redirect_to('landing')

                    # password was wrong
                    else:
                        logging.error('AUTH: Password MISMATCH. Logon unsuccessful.')
                        self.session['bad_logon_count'] = self.session.get('bad_logon_count', 0) + 1
                        context['error'] = 'Woops, there was a problem logging you in.'
                        return self.render('security/login.html', **context)

                # username was wrong
                else:
                    logging.error('AUTH: User not found. Logon unsuccessful.')
                    self.session['bad_logon_count'] = self.session.get('bad_logon_count', 0) + 1
                    context['error'] = 'Woops, there was a problem logging you in.<br />Are you sure your <a href="#">username is correct?</a>'
                    return self.render('security/login.html', **context)
        else:
            return self.render('security/login.html', **context)


class Logout(WebHandler, SecurityConfigProvider):

    ''' Default logout handler - redirect using App Engine's users API, if available. '''

    def get(self):

        ''' Logout page '''

        try:
            self.session = {}
            logout_url = self.api.users.create_logout_url(self.request.environ.get('HTTP_REFERRER', '/'))
            if logout_url is not None:
                return self.redirect(logout_url)

        except:
            self.error(404)
            return


class Register(WebHandler, SecurityConfigProvider):

    ''' Default signup handler - return 404 by default. '''

    def get(self):

        ''' Dev signup handler. Will need to be rewritten with an actual registration form. '''

        # if they aren't logged in, redirect
        u = self.api.users.get_current_user()
        if u is None:
            return self.redirect_to('auth/login')

        # make sure user doesn't already exist
        pu = user_models.User.get_by_id(u.email())
        if pu is None:
            if cfg.debug:
                # only autoregister on the devserver
                self.response.write('Autoregistering...<br />')

                username, domain = tuple(u.email().split('@'))

                # make user
                user = user_models.User(id=u.email(), user=u, username=u.nickname(), firstname='John', lastname='Doe', bio='You are cool')
                ukey = user.put()

                # make customurl
                curl = assets.CustomURL(id=username, slug=username, target=ukey)
                curl.put()

                user.customurl = curl.key

                # make email
                em = user_models.EmailAddress(id=u.email(), parent=ukey, user=ukey, address=u.email(), label='d', notify=True, jabber=True, gravatar=True)
                em.put()
                user.email = [em.key]

                # make permissions
                pm = user_models.Permissions(id='global', parent=ukey, user=ukey, moderator=True, admin=True, developer=True)
                pm.put()
                user.permissions = [pm.key]

                user.put()

                self.response.write('<b>Done. Redirecting.</b>')

                # TODO: Redirect back to the url they came from, if provided.

                return self.redirect_to('landing')
        else:
            return self.redirect_to('landing')


class Provider(WebHandler, SecurityConfigProvider):

    ''' Description/policy page for a login provider. '''

    def get(self, provider):

        ''' Return a test message. '''

        return self.response.write('<b>provider:</b> ' + provider)


class FederatedAction(WebHandler, SecurityConfigProvider):

    ''' Description/policy page for a login provider. '''

    ### === Redirect Methods === ###
    def redirect_failure(self, error_message=None, error_code=None):

        ''' Redirect to login with an error message or code '''

        if error_message:
            logging.error('AUTH: Redirecting back to logon with error_message "%s".' % error_message)
            redirect_url = self.url_for('auth/login', fdmg=error_message)
        elif error_code:
            logging.error('AUTH: Redirecting back to logon with error_code "%s".' % error_code)
            redirect_url = self.url_for('auth/login', fder=error_code)
        else:
            logging.error('AUTH: Redirecting back to logon because of a generic failure.')
            redirect_url = self.url_for('auth/login', fder='generic')
        return self.redirect(redirect_url)

    def redirect_success(self):

        ''' Redirect to continue_url or homepage after successful logon '''

        if self.session.get('continue_url') or 'continue' in self.request.params:
            continue_url = self.request.get('continue', self.session.get('continue_url'))
        else:
            continue_url = self.url_for('landing')

        return self.redirect(continue_url)

    ### === Session Functions === ###
    def build_authenticated_session(self, email, nickname, ukey, uid):

        ''' Build an authenticated session struct, to be picked up by handler dispatch on the next pageload '''

        self.authenticated = True
        self.session['authenticated'] = True
        self.session['email'] = email
        self.session['uid'] = email
        if isinstance(ukey, ndb.Key):
            self.session['ukey'] = ukey.urlsafe()
        else:
            self.session['ukey'] = ukey
        self.session['nickname'] = nickname

        return self.session

    ### === Callback Functions === ###
    def callback_facebook(self):

        ''' Finish processing Facebook auth. '''

        # pull POST fields from fb
        csrf = self.request.get('csrf')
        code = self.request.get('code')
        state = self.request.get('state')
        error = self.request.get('error', False)

        # check state for CSRF protection
        if (self.decrypt(state) == self.session.get('sid')) and (csrf == hashlib.sha1(self.session.get('sid')).hexdigest()):
            logging.info('FB: State and CSRF match. Decoding.')

            # check for errors
            if error:
                logging.warning('FB: Error flag present in callback. Uh oh.')

                error_reason = self.request.get('error_reason')
                error_description = self.request.get('error_description')

                logging.warning('FB: Error reason: "%s".' % error_reason)
                logging.warning('FB: Error description: "%s".' % error_description)

                if error_reason == 'user_denied':
                    logging.critical('Looks like the user shafted us. Redirecting.')

                    return self.redirect('/login?fder=authorization_denied')

            # no errors
            else:

                token_endpoint = "https://graph.facebook.com/oauth/access_token?client_id=%(client)s&redirect_uri=%(redirect)s&client_secret=%(secret)s&code=%(code)s" % {

                    'client': self._resolveProvider('facebook').get('key'),
                    'redirect': ''.join([
                            self.request.environ.get('HTTP_SCHEME', 'HTTP').lower(), '://',
                            self.request.environ.get('HTTP_HOST', 'localhost:8080'),
                            self.url_for('auth/action-provider', action='callback', provider='facebook', csrf=csrf)
                    ]),
                    'secret': self._resolveProvider('facebook').get('secret'),
                    'code': code

                }

                # get the stupid token
                access_token = self.api.urlfetch.fetch(token_endpoint)

                # successful reup
                if access_token.status_code == 200:
                    logging.info('FB: Access code endpoint fetch success.')
                    params = {}
                    for b_item in access_token.content.split('&'):
                        k, v = b_item.split('=')
                        params[k] = v

                    logging.info('FB: Access code: "%s". Expiration: "%s".' % (params.get('access_token'), params.get('expires')))

                    access_token = params['access_token']
                    expires = params['expires']

                    self.session['fb_access_token'] = access_token
                    self.session['fb_token_expire'] = expires
                    self.session['fb_token_establish'] = time.time()

                    ## get the 'me'
                    me_endpoint = "https://graph.facebook.com/me?access_token=%s" % access_token
                    user_info = self.api.urlfetch.fetch(me_endpoint)

                    ## check for user existence via facebook email address
                    if user_info.status_code == 200:
                        logging.info('FB: Graph `me` request success.')
                        user_struct = json.loads(user_info.content)

                        # Copy over user struct stuff
                        email = user_struct['email']
                        nickname = user_struct['name']
                        ukey = ndb.Key(user_models.User, email)

                        # Log it
                        logging.info('FB: Loggin in user with email "%s" and nickname "%s" and derived ukey "%s".' % (email, nickname, ukey))

                        # log them in
                        self.build_authenticated_session(
                            email=email,
                            nickname=nickname,
                            ukey=ukey.urlsafe(),
                            uid=ukey.id()
                        )

                        return self.redirect_success()

                else:
                    logging.critical('FB: ERROR! Failed to get persistent auth token.')
                    logging.critical('FB: Response from facebook: "%s".' % access_token.content)
                    return self.redirect('/login?fder=access_token_fail')

        # isgood
        else:
            logging.critical('WARNING! POSSIBLE SECURITY BREACH.')
            logging.critical('State variable did not match in callback.')
            return self.redirect("/login")

        return self.response.write('<pre>' + str(self.request) + '</pre>')

    def callback_google(self):

        ''' Finish processing Google auth. '''

        u = self.api.users.get_current_user()

        # federated/openid
        if u is not None:

            self.build_authenticated_session(
                email=u.email(),
                nickname=u.nickname(),
                ukey=ndb.Key(user_models.User, u.email()),
                uid=u.email()
            )

            return self.redirect_success()

        else:

            try:
                # federated/oauth
                u = self.api.oauth.get_current_user()
                assert u is not None

                self.build_authenticated_session(
                    email=u.email(),
                    nickname=u.nickname(),
                    ukey=ndb.Key(user_models.User, u.email()),
                    uid=u.email()
                )

            ## everything failed
            except AssertionError:

                ## redirect to login page w/ error
                return self.redirect_failure(error_code='hybrid_login_failed')

        return self.response.write('<pre>' + str(self.request) + '</pre>')

    def callback_twitter(self):

        ''' Finish processing Twitter auth. '''

        return self.response.write('<pre>' + str(self.request) + '</pre>')

    ### === HTTP Methods === ###
    def get(self, action=None, provider=None):

        ''' Return a test message. '''

        if action == 'callback':
            if provider is not None:
                return {
                    'googleplus': self.callback_google,
                    'facebook': self.callback_facebook,
                    'twitter': self.callback_twitter
                }.get(provider, lambda: self.error(404))()

        return self.response.write('<b>action:</b> ' + action)
