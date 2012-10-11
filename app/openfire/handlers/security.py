# -*- coding: utf-8 -*-
import time
import base64
import webapp2
import hashlib
import config as cfg
from config import config

from google.appengine.ext import ndb

from openfire.models import assets
from openfire.models import user as user_models

from openfire.handlers import WebHandler

from apptools.util import json
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

    def build_authenticated_session(self, email, nickname, ukey, uid, provider='organic', mode=None, register=False):

        ''' Build an authenticated session struct, to be picked up by handler dispatch on the next pageload '''

        self.authenticated = True
        self.session['authenticated'] = True
        if isinstance(email, ndb.Key):
            self.session['email'] = email.id()
        elif isinstance(email, list):
            self.session['email'] = email[0].id()
        else:
            self.session['email'] = email
        self.session['uid'] = self.session['email']
        if isinstance(ukey, ndb.Key):
            self.session['ukey'] = ukey.urlsafe()
        else:
            self.session['ukey'] = ukey
        self.session['nickname'] = nickname

        if provider != 'organic':
            self.session['mode'] = 'federated'
            self.session['provider'] = provider
        else:
            self.session['mode'] = 'organic'

        if register:
            self.session['register'] = True

        return self.session


class Login(WebHandler, SecurityConfigProvider):

    ''' Default login handler - redirect using App Engine's users API, if available. '''

    def do_auth_redirect(self, url):

        ''' Redirect to a third party provider. '''

        self.logging.info('AUTH: Redirecting to provider URL "%s".' % url)
        return self.redirect(url)

    def via_facebook(self):

        ''' Redirect the user to Facebook-based login. '''

        if cfg.debug or 'staging' in self.request.environ.get('HTTP_HOST'):
            appid = '257586781019220'
        else:
            appid = self._metaConfig.get('opengraph', {}).get('facebook', {}).get('app_id', '__EMPTY_APP_ID__')

        return self.do_auth_redirect(

            "https://www.facebook.com/dialog/oauth?client_id=%(appid)s&redirect_uri=%(callback)s&scope=%(scope)s&state=%(state)s" % {

                # appID and sessionID
                'appid': appid,
                'state': self.encrypt(self.session.get('sid')),

                # scopes and callback
                'scope': ','.join([scope.get('name') for scope in self._resolveProvider('facebook').get('scopes', []) if scope.get('enabled', False)]),
                'callback': self.url_for('auth/action-provider',
                                action='callback',
                                provider='facebook',
                                csrf=hashlib.sha1(self.session.get('sid')).hexdigest(),
                                ofsid=self.encrypt(self.session.get('sid')),
                                _full=True,
                                _scheme='https' if not cfg.debug else 'http',
                                _netloc=self.force_hostname or self.request.host
                            )

        })

    def via_google(self):

        ''' Redirect the user to Google-based login. '''

        if 'staging' in self.request.environ.get('HTTP_HOST'):
            return self.do_auth_redirect(*[
                self.api.users.create_login_url(

                    # google auth callback (no federated identity endpoint)
                    self.url_for('auth/action-provider', **{
                        'action': 'callback',
                        'provider': 'googleplus',
                        'csrf': hashlib.sha256(self.session.get('sid')).hexdigest(),
                        'ofsid': self.encrypt(self.session.get('sid')),
                        'ofentry': base64.b64encode(self.force_hostname or self.request.host),
                        '_scheme': 'https' if not cfg.debug else 'http',
                        '_full': True,
                        '_netloc': 'auth.openfi.re' if not cfg.debug else 'localhost:8080'
                    })

                )
            ])

        return self.do_auth_redirect(*[

            self.api.users.create_login_url(

                # google auth callback
                self.url_for('auth/action-provider', **{
                    'action': 'callback',
                    'provider': 'googleplus',
                    'csrf': hashlib.sha256(self.session.get('sid')).hexdigest(),
                    'ofsid': self.encrypt(self.session.get('sid')),
                    'ofentry': base64.b64encode(self.force_hostname or self.request.host),
                    '_scheme': 'https' if not cfg.debug else 'http',
                    '_full': True,
                    '_netloc': 'auth.openfi.re' if not cfg.debug else 'localhost:8080'
                }),

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
            self.logging.info('AUTH: User requested federated logon from provider "%s".' % provider)
            return {

                # run code for whatever provider we're doing
                'google': self.via_google,
                'facebook': self.via_facebook,
                'googleplus': self.via_google,
                'twitter': self.via_twitter

            }.get(provider, lambda: self.error(404))()

        else:

            ## Simple logon: appengine basic
            if self._securityConfig.get('authentication', {}).get('federation', {}).get('simple', False):
                ## fallback to appengine-based logon
                try:
                    self.logging.info('AUTH: Decided on simple logon.')
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

        self.logging.info('AUTH: Processing organic logon request.')

        ## return error for too many failed logins
        if 'bad_logon_count' in self.session and (self.session.get('bad_logon_count', 0) > 0):
            if self._securityConfig.get('config', {}).get('bad_logon_limit', 0) < self.session.get('bad_logon_count'):

                self.logging.error('AUTH: User exceeded bad login count. Ratelimiting.')

                context['error'] = 'You have been ratebanned.'
                return self.render('security/login.html', **context)

        ## pick up the form
        if 'username' in self.request.params and 'password' in self.request.params:

            try:
                hashed_password = wsec.hash_password( self.request.params.get('password'),  # plaintext pswd
                                                      self._securityConfig.get('config', {}).get('wsec', {}).get('hash', 'sha256'),  # hash algorithm
                                                      self._securityConfig.get('config', {}).get('random', {}).get('blocks', {}).get('salt', '__salt__'),  # salt
                                                      self._securityConfig.get('config', {}).get('random', {}).get('blocks', {}).get('pepper', '__pepper__'))  # n' peppa

                user_key = ndb.Key(user_models.User, self.request.params.get('username'))
                email_key = user_models.EmailAddress.query().filter(user_models.EmailAddress.address == self.request.params.get('username')).get(keys_only=True, produce_cursors=False)
            except NotImplementedError:
                context['error'] = 'Woops! Something went wrong. Please try again.'
                return self.render('security/login.html', **context)
            else:
                self.logging.info('AUTH: Calculated user key "%s".' % user_key)

                # resolve user by username
                user = user_key.get()

                if user is None:
                    # try resolving as email
                    if email_key is not None:
                        email = email_key.get()
                        if email is not None:
                            user = email.key.parent().get()

                # user found?
                if user is not None:

                    self.logging.info('AUTH: User found at username "%s".' % user.username)

                    # password match?
                    if user.password == hashed_password:

                        self.logging.info('AUTH: Passwords match. Logon successful.')

                        # log them in
                        self.build_authenticated_session(
                            email=user.key.id(),
                            nickname=' '.join([user.firstname, user.lastname]),
                            ukey=user.key.urlsafe(),
                            uid=user.key.id(),
                            provider='organic'
                        )

                        if 'bad_logon_count' in self.session:
                            self.session['bad_logon_count'] = 0

                        # redirect them on
                        if self.session.get('continue_url'):
                            self.logging.info('AUTH: Continue URL found. Redirecting to "%s".' % self.session.get('continue_url'))
                            return self.redirect(self.session.get('continue_url'))
                        else:
                            self.logging.info('AUTH: No continue URL found. Redirecting to landing.')
                            return self.redirect_to('landing', **{
                                '_full': True,
                                '_scheme': 'https' if not cfg.debug else 'http',
                                '_netloc': self.force_hostname or self.request.host
                            })

                    # password was wrong
                    else:
                        self.logging.error('AUTH: Password MISMATCH. Logon unsuccessful.')
                        self.session['bad_logon_count'] = self.session.get('bad_logon_count', 0) + 1
                        context['error'] = 'Woops, there was a problem logging you in.'
                        return self.render('security/login.html', **context)

                # username was wrong
                else:
                    self.logging.error('AUTH: User not found. Logon unsuccessful.')
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
            tombstoned_session = {'destroy': True}

            # If this user logged in via google+, log them out
            if 'mode' in self.session and self.session.get('mode') == 'googleplus':
                logout_url = self.api.users.create_logout_url(self.url_for('auth/login', **{
                    '_full': True,
                    '_scheme': 'https' if not cfg.debug else 'http',
                    '_netloc': self.force_hostname or self.request.host
                }))
                self.session = tombstoned_session
                return self.redirect(logout_url)

            else:
                self.session = tombstoned_session
                return self.redirect_to('auth/login', **{
                    '_full': True,
                    '_scheme': 'https' if not cfg.debug else 'http',
                    '_netloc': self.force_hostname or self.request.host
                })

        except ValueError, e:
            self.session = tombstoned_session
            return self.redirect_to('auth/login', **{
                '_full': True,
                '_scheme': 'https' if not cfg.debug else 'http',
                '_netloc': self.force_hostname or self.request.host
            })


class Register(WebHandler, SecurityConfigProvider):

    ''' Default signup handler - return 404 by default. '''

    # shut off registration redirect
    apply_redirect = False

    def get(self):

        ''' Dev signup handler. Will need to be rewritten with an actual registration form. '''

        return self.render('security/register.html')


class Provider(WebHandler, SecurityConfigProvider):

    ''' Description/policy page for a login provider. '''

    def get(self, provider):

        ''' Return a test message. '''

        return self.response.write('<b>provider:</b> ' + provider)


class FederatedAction(WebHandler, SecurityConfigProvider):

    ''' Description/policy page for a login provider. '''

    apply_redirect = False

    ### === Redirect Methods === ###
    def redirect_failure(self, entrypoint=None, error_message=None, error_code=None):

        ''' Redirect to login with an error message or code '''

        if entrypoint is None: entrypoint = self.force_hostname or self.request.host
        if error_message:
            self.logging.error('AUTH: Redirecting back to logon with error_message "%s".' % error_message)
            redirect_url = self.url_for('auth/login', **{
                'fdmg': error_message,
                '_full': True,
                '_scheme': 'https' if not cfg.debug else 'http',
                '_netloc': entrypoint
            })
        elif error_code:
            self.logging.error('AUTH: Redirecting back to logon with error_code "%s".' % error_code)
            redirect_url = self.url_for('auth/login', **{
                'fder': error_code,
                '_full': True,
                '_scheme': 'https' if not cfg.debug else 'http',
                '_netloc': entrypoint
            })
        else:
            self.logging.error('AUTH: Redirecting back to logon because of a generic failure.')
            redirect_url = self.url_for('auth/login', **{
                'fder': 'generic',
                '_full': True,
                '_scheme': 'https' if not cfg.debug else 'http',
                '_netloc': entrypoint
            })
        return self.redirect(redirect_url)

    def redirect_success(self, entrypoint=None):

        ''' Redirect to continue_url or homepage after successful logon '''

        if entrypoint is None: entrypoint = self.force_hostname or self.request.host

        if self.session.get('continue_url') or 'continue' in self.request.params:
            continue_url = self.request.get('continue', self.session.get('continue_url'))
        else:
            continue_url = self.url_for('landing', **{
                '_full': True,
                '_scheme': 'https' if not cfg.debug else 'http',
                '_netloc': entrypoint
            })

        return self.redirect(continue_url)

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
            self.logging.info('FB: State and CSRF match. Decoding.')

            # check for errors
            if error:
                self.logging.warning('FB: Error flag present in callback. Uh oh.')

                error_reason = self.request.get('error_reason')
                error_description = self.request.get('error_description')

                self.logging.warning('FB: Error reason: "%s".' % error_reason)
                self.logging.warning('FB: Error description: "%s".' % error_description)

                if error_reason == 'user_denied':
                    self.logging.critical('Looks like the user shafted us. Redirecting.')

                    return self.redirect(self.url_for('auth/login', **{
                        'fder': 'authorization_denied',
                        '_full': True,
                        '_scheme': 'https' if not cfg.debug else 'http',
                        '_netloc': self.force_hostname or self.request.host
                    }))

            # no errors
            else:

                if cfg.debug or 'staging' in self.request.environ.get('HTTP_HOST'):
                    client = '257586781019220'
                    secret = '679a4b95e7213409d61397bb989b826a'
                else:
                    client = self._resolveProvider('facebook').get('key')
                    secret = self._resolveProvider('facebook').get('secret')

                token_endpoint = "https://graph.facebook.com/oauth/access_token?client_id=%(client)s&redirect_uri=%(redirect)s&client_secret=%(secret)s&code=%(code)s" % {

                    'client': client,
                    'redirect': ''.join([
                            self.url_for('auth/action-provider',
                                action='callback',
                                provider='facebook',
                                csrf=csrf,
                                _full=True,
                                _netloc=self.force_hostname or self.request.host,
                                _scheme='https' if not cfg.debug else 'http'
                            )
                    ]),
                    'secret': secret,
                    'code': code

                }

                # get the stupid token
                access_token = self.api.urlfetch.fetch(token_endpoint)

                # successful reup
                if access_token.status_code == 200:
                    self.logging.info('FB: Access code endpoint fetch success.')
                    params = {}
                    for b_item in access_token.content.split('&'):
                        k, v = b_item.split('=')
                        params[k] = v

                    self.logging.info('FB: Access code: "%s". Expiration: "%s".' % (params.get('access_token'), params.get('expires')))

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
                        self.logging.info('FB: Graph `me` request success.')
                        user_struct = json.loads(user_info.content)

                        # Copy over user struct stuff
                        id = self.session['fb_id'] = user_struct['id']
                        email = self.session['fb_email'] = user_struct['email']
                        nickname = self.session['fullname'] = user_struct['name']

                        self.logging.info('FB: Found user with ID "%s" and email "%s".' % (id, email))

                        ukey = ndb.Key(user_models.User, email)

                        em_q = user_models.EmailAddress.query().filter(user_models.EmailAddress.address == email)
                        result = em_q.fetch(1, keys_only=True)

                        if result:
                            ukey = result[0].parent()

                        fb_id = user_models.FacebookAccount.query().filter(user_models.FacebookAccount.ext_id == id).fetch(1, keys_only=True, produce_cursors=False)

                        if fb_id is not None:
                            ukey, fb_acct = tuple(ndb.get_multi([ukey, fb_id]))
                        else:
                            user, fb_acct = ukey.get(), None
                            if user is None:
                                ukey = None
                            else:
                                ukey = user.key

                        if ukey is None and fb_acct is not None:
                            fb_user = fb_acct.key.parent().get()
                            ukey = fb_user.key

                        # Log it
                        self.logging.info('FB: Loggin in user with email "%s" and nickname "%s" and derived ukey "%s".' % (email, nickname, ukey))

                        if ukey is not None:
                            # log them in
                            self.build_authenticated_session(
                                email=email,
                                nickname=user_struct['name'],
                                ukey=ukey.urlsafe(),
                                uid=ukey.id(),
                                provider='facebook',
                                mode='oauth'
                            )
                            return self.redirect_success()
                        else:
                            self.build_authenticated_session(
                                email=email,
                                nickname=user_struct['name'],
                                ukey=None,
                                uid=user_struct['id'],
                                provider='facebook',
                                mode='oauth',
                                register=True
                            )
                            return self.redirect_to('auth/register',
                                exi=base64.b64encode(user_struct['id']),
                                state=hashlib.sha512(user_struct['id']).hexdigest(),
                                provider='facebook',
                                _full=True,
                                _scheme='https' if not cfg.debug else 'http',
                                _netloc=self.force_hostname or self.request.host
                            )

                else:
                    self.logging.critical('FB: ERROR! Failed to get persistent auth token.')
                    self.logging.critical('FB: Response from facebook: "%s".' % access_token.content)
                    return self.redirect(self.url_for('auth/login', **{
                        'fder': 'access_token_fail',
                        '_full': True,
                        '_scheme': 'https' if not cfg.debug else 'http',
                        '_netloc': self.force_hostname or self.request.host
                    }))

        else:
            self.logging.critical('WARNING! POSSIBLE SECURITY BREACH.')
            self.logging.critical('State variable did not match in callback.')
        return self.redirect(self.url_for('auth/login', **{
            '_full': True,
            '_scheme': 'https' if not cfg.debug else 'http',
            '_netloc': self.force_hostname or self.request.host
        }))

    def callback_google(self):

        ''' Finish processing Google auth. '''

        u = self.api.users.get_current_user()
        entrypoint = self.request.get('ofentry', None)
        if entrypoint:
            entrypoint = base64.b64decode(entrypoint)
        else:
            entrypoint = self.force_hostname or self.request.host

        # federated/openid
        if u is not None:

            ## resolve user
            user_key = ndb.Key(user_models.User, u.email())
            email_key = user_models.EmailAddress.query().filter(user_models.EmailAddress.address == u.email()).get(keys_only=True, produce_cursors=False)

            if email_key is not None:
                user, email = tuple(ndb.get_multi([user_key, email_key]))
                if user is None and email is not None:
                    self.user = user = email.key.parent().get()

            else:
                self.user = user = user_key.get()

            if user is not None:
                self.build_authenticated_session(
                    email=user.email[0].id(),
                    nickname=user.firstname + ' ' + user.lastname,
                    ukey=user.key,
                    uid=u.user_id(),
                    mode='openid',
                    provider='googleplus'
                )
                return self.redirect_success(entrypoint)
            else:
                self.build_authenticated_session(
                    email=u.email(),
                    nickname=u.nickname(),
                    ukey=ndb.Key(user_models.User, u.email()),
                    uid=u.user_id(),
                    provider='googleplus',
                    mode='openid',
                    register=True
                )
                return self.redirect_to('auth/register', **{
                    'exi': base64.b64encode(u.user_id()),
                    'p': 'gp',
                    'state': hashlib.sha512(u.user_id()).hexdigest(),
                    'provider': 'googleplus',
                    '_full': True,
                    '_scheme': 'https' if not cfg.debug else 'http',
                    '_netloc': entrypoint
                })
        else:

            try:
                # federated/oauth
                u = self.api.oauth.get_current_user()
                assert u is not None

                user_key = ndb.Key(user_models.User, u.email())
                email_key = user_models.EmailAddress.query().filter(user_models.EmailAddress.address == u.email()).get(keys_only=True, produce_cursors=False)

                if email_key is not None:
                    user, email = tuple(ndb.get_multi([user_key, email_key]))
                    if user is None and email is not None:
                        self.user = user = email.key.parent().get()

                else:
                    self.user = user = user_key.get()

                if user is not None:
                    self.build_authenticated_session(
                        email=user.email,
                        nickname=user.firstname + ' ' + user.lastname,
                        ukey=user.key,
                        uid=u.user_id(),
                        provider='googleplus',
                        mode='oauth'
                    )
                    return self.redirect_success(entrypoint)
                else:
                    self.build_authenticated_session(
                        email=u.email(),
                        nickname=u.email(),
                        ukey=None,
                        uid=u.user_id(),
                        provider='googleplus',
                        mode='oauth',
                        register=True
                    )
                    return self.redirect_to('auth/register', **{
                        'exi': base64.b64encode(u.user_id()),
                        'p': 'foa',
                        'state': hashlib.sha512(u.user_id()).hexdigest(),
                        'provider': 'googleplus',
                        '_full': True,
                        '_scheme': 'https' if not cfg.debug else 'http',
                        '_netloc': entrypoint
                    })

            ## everything failed
            except AssertionError:

                ## redirect to login page w/ error
                return self.redirect_failure(entrypoint, error_code='hybrid_login_failed')

            except Exception, e:

                if not cfg.debug:
                    self.logging.error('Generic failure occured in hybrid logon routine. Exception: "%s".' % str(e))
                    return self.redirect_failure(entrypoint, error_code='generic_failure')
                else:
                    raise
        
        return self.redirect_failure(entrypoint, error_code='generic_failure')

    def callback_twitter(self):

        ''' Finish processing Twitter auth. '''

        return self.response.write('<pre>' + str(self.request) + '</pre>')

    ### === HTTP Methods === ###
    def get(self, action=None, provider=None):

        ''' Return a test message. '''

        if 'register' in self.session:
            del self.session['register']

        if 'returnto' in self.session:
            del self.session['returnto']

        if action == 'callback':
            if provider is not None:
                return {
                    'google': self.callback_google,
                    'googleplus': self.callback_google,
                    'facebook': self.callback_facebook,
                    #'twitter': self.callback_twitter
                }.get(provider, lambda: self.error(404))()

        return self.response.write('<b>action:</b> ' + action)
