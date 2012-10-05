# -*- coding: utf-8 -*-

'''

Project Handlers

This module is where you put your project's RequestHandlers. WebHandler and MobileHandler
are designed to be extended by your app's handlers. This gives you a chance to inject custom
logic / request handling stuff across your entire app, by putting it here.

-sam (<sam@momentum.io>)

'''

## General Imports
import os
import config
import hashlib

## Webapp2 Imports
import webapp2

from decimal import Decimal

## Google Imports
from google.appengine.ext import ndb
from google.appengine.ext.ndb import context

## AppTools Imports
from apptools.core import BaseHandler

## Openfire Imports
from openfire.models.user import User
from openfire.models.user import Permissions

## Core Bridge Imports
from openfire.core.content import ContentBridge
from openfire.core.sessions import SessionsBridge
from openfire.core.data.namespacing import NamespaceBridge


## WebHandler - parent class for all site request handler classes
class WebHandler(BaseHandler, SessionsBridge, ContentBridge, NamespaceBridge):

    ''' Handler for desktop web requests. '''

    # Resource/Template Preloading
    template = None

    # Session Properties
    session = {}
    transport = {}
    sessions = True
    force_session = True
    apply_redirect = True

    # Security Properties
    user = None
    scope = None
    permissions = None
    authenticated = False
    auth_provider = False

    # Channel Properties
    channel_id = None
    channel_token = None
    channel_timeout = 120

    # Runtime Config
    should_cache = False
    should_preload = False

    ## ++ Internal Shortcuts ++ ##
    @webapp2.cached_property
    def config(self):

        ''' Cached access to main config for this handler. '''

        return self._webHandlerConfig

    @webapp2.cached_property
    def jinja2(self):

        ''' Cached access to Jinja2. '''

        ## Patch in dynamic content support, if available
        if hasattr(self, 'dynamicEnvironmentFactory'):
            return self._output_api.get_jinja(self.app, self.dynamicEnvironmentFactory)
        else:
            return self._output_api.get_jinja(self.app, self.jinja2EnvironmentFactory)

    @webapp2.cached_property
    def _webHandlerConfig(self):

        ''' Cached access to this handler's config. '''

        return config.config.get('openfire.classes.WebHandler')

    @webapp2.cached_property
    def _integrationConfig(self):

        ''' Cached access to this handler's integration config. '''

        return self._webHandlerConfig.get('integrations')

    @webapp2.cached_property
    def _jinjaConfig(self):

        ''' Cached access to Jinja2 base config. '''

        return config.config.get('webapp2_extras.jinja2')

    @webapp2.cached_property
    def _outputConfig(self):

        ''' Cached access to base output config. '''

        return config.config.get('apptools.project.output')

    @webapp2.cached_property
    def _ofOutputConfig(self):

        ''' Cached access to openfire's site-specific output config. '''

        return config.config.get('openfire.output')

    @webapp2.cached_property
    def logging(self):

        ''' Cached access to this handler's logging pipe '''

        return super(WebHandler, self).logging.extend('WebHandler', self.__class__.__name__)._setcondition(self.config.get('logging', False))

    @webapp2.cached_property
    def template_environment(self):

        ''' Return a new environment, because if we're already here it's not cached. '''

        return self.jinja2

    @webapp2.cached_property
    def baseTransport(self):

        ''' Return a clean set of transport base settings. '''

        return {
            'secure': False,
            'endpoint': self.request.environ.get('HTTP_HOST') if not self.force_hostname else self.force_hostname,
            'consumer': 'ofapp',
            'scope': 'readonly',
            'make_object': lambda x: self._make_services_object(x)
        }

    ## ++ Internal Methods ++ ##
    def __init__(self, request=None, response=None, preload=False):

        ''' Init this request handler. '''

        self.should_preload = preload

        if request and response:
            # Pass up to webapp2 first
            self.initialize(request, response)
        else:
            self.initialize(webapp2.get_request(), webapp2.Response())

    def initialize(self, request, response):

        ''' Initialize this request handler. '''

        super(WebHandler, self).initialize(request, response)

        # Set up the namespace.
        self.prepare_namespace(request)

        # Initialize dynamic content API
        self._initialize_dynamic_content(self.app)

    def preload(self):

        ''' Preloaded data and template support. '''

        if self.should_preload:
            # Preload/prerender template
            if hasattr(self, 'template') and getattr(self, 'template') not in frozenset(['', None, False]):
                self.preload_template(self.template)
            return

    @ndb.toplevel
    def dispatch(self):

        ''' Retrieve session + dispatch '''

        # Preload second
        if self.should_preload:
            self.preload()

        if self.sessions:
            # Resolve user session
            self.session = self.build_session()

        try:
            if self.sessions and self.apply_redirect:
                # If we detect a triggered redirect, do it and remove the trigger (CRUCIAL.)
                if self.session.get('redirect') is not None:
                    redirect_url = self.session.get('redirect')
                    del self.session['redirect']
                    response = self.redirect(redirect_url)
                    return response

            # Find super
            _super = super(WebHandler, self)

            # Dispatch method
            response = _super.dispatch()
            if isinstance(response, basestring):
                self.response.write(response)
            elif isinstance(response, webapp2.Response):
                self.response = response

        finally:

            if self.sessions:
                # Always save the session.
                self.save_session()

        return self.response

    def _format_as_percentage(self, number):

        ''' Format a number as a percentage. '''

        # create result array
        formatted_number = [i for i in reversed(list(str(number)))]

        # format with commas
        map(lambda x: formatted_number.insert(x, ','), [
                i for i in reversed([
                        b for (b, i) in enumerate(formatted_number[:])
                        if ((b % 3) == 0)])
            if (i != 0)])

        # build, format as percentage, return
        return ''.join([char for char in filter(lambda x: x is not None,
                [''.join([i for i in reversed(formatted_number)]), '%'])])

    def _format_as_currency(self, number, places=0, curr='', sep=',', dp='.', pos='', neg='-', trailneg=''):

        '''
        Format a number as currency. Using standard python 'moneyfmt' recipe for Decimals.

        arguments:
            places:  required number of places after the decimal point
            curr:    optional currency symbol before the sign (may be blank)
            sep:     optional grouping separator (comma, period, space, or blank)
            dp:      decimal point indicator (comma or period)
                     only specify as blank when places is zero
            pos:     optional sign for positive numbers: '+', space or blank
            neg:     optional sign for negative numbers: '-', '(', space or blank
            trailneg:optional trailing minus indicator:  '-', ')', space or blank
        '''

        if not number:
            number = 0.0
        value = Decimal(number)
        q = Decimal(10) ** -places
        sign, digits, exp = value.quantize(q).as_tuple()
        result = []
        digits = map(str, digits)
        build, next = result.append, digits.pop
        if sign:
            build(trailneg)
        for i in range(places):
            build(next() if digits else '0')
        if len(result):
            build(dp)
        if not digits:
            build('0')
        i = 0
        while digits:
            build(next())
            i += 1
            if i == 3 and digits:
                i = 0
                build(sep)
        build(curr)
        build(neg if sign else pos)
        return '$' + ''.join(reversed(result))

    def build_session2(self):

        ''' Build an initial session object and create an SID '''

        if hasattr(self, 'force_session') and self.force_session:
            ## build a session no matter what, yo
            self.session = self.get_session()

            if self.session.get('ukey', None) is None:
                u = self.api.users.get_current_user()
                if u is not None:

                    ## we have an authenticated user
                    self.session['authenticated'] = True
                    self.authenticated = True

                    ## sometimes this returns none (when federated identity auth is enabled), but then the email is a persistent token
                    self.session['uid'] = u.email()

                    user, permissions = tuple(ndb.get_multi([ndb.Key(User, self.session['uid']), ndb.Key(Permissions, 'global', parent=ndb.Key(User, self.session['uid']))]))
                    if user is None:
                        self.session['redirect'] = self.url_for('auth/register')
                        self.session['returnto'] = self.request.url
                        self.session['register'] = True
                    else:
                        self.user = user
                        self.permissions = permissions
                        self.session['ukey'] = user.key.urlsafe()
                        self.session['email'] = u.email()
                        self.session['nickname'] = u.nickname()
                        if self.api.users.is_current_user_admin():
                            self.session['root'] = True
            else:
                self.user = ndb.Key(urlsafe=self.session['ukey'])
                self.permissions = ndb.Key(Permissions, 'global', parent=ndb.Key(User, self.session['uid']))
                self.user, self.permissions = tuple(ndb.get_multi([self.user, self.permissions]))
        return self.session

    def render(self, *args, **kwargs):

        ''' If supported, pass off to render_dynamic, which rolls-in support for editable content blocks. '''

        if hasattr(self, 'render_dynamic'):
            return self.render_dynamic(*args, **kwargs)
        else:
            return super(WebHandler, self).render(*args, **kwargs)

    def _make_services_object(self, services):

		''' Make a dict suitable for JSON representing an API service. '''

		return [[
			service,
			cfg['methods'],
			opts
		] for service, action, cfg, opts in services['services_manifest']]

    def _bindRuntimeTemplateContext(self, context):

        ''' Bind in the session '''

        transport = dict(self.baseTransport.items()[:])
        if hasattr(self, 'transport'):
            transport.update(self.transport)

        context.update({

            # head meta config
            '_meta': config.config.get('openfire.meta'),
            '_opengraph': config.config.get('openfire.meta').get('opengraph'),
            '_location': config.config.get('openfire.meta').get('opengraph').get('location'),

            # encryption/decryption utilities
            'encrypt': lambda x: self.encrypt(x),
            'decrypt': lambda x: self.decrypt(x),

            # formatter shortcuts (also installed as filters)
            'currency': lambda x: self._format_as_currency(x),
            'percentage': lambda x: self._format_as_percentage(x),

            # media utils
            'gravatarify': lambda email, ext, size: ''.join([
                    ':'.join([self.request.environ.get('wsgi.url_scheme', 'http'), '//']),
                    '/'.join([self._integrationConfig.get('gravatar').get('endpoints').get((self.force_https_assets == True and 'https' or self.request.environ.get('wsgi.url_scheme', 'http').lower())),
                        'avatar',
                        hashlib.md5(email).hexdigest()]),
                    '.%s' % ext,
                    '?s=%s&d=%s://lyr9.net/img/default-profile.png?s=%s' % (size, (self.force_https_assets == True and 'https' or self.request.environ.get('wsgi.url_scheme', 'http').lower()), size)
                ]),

            # openfire security extensions
            'security': {
                'session': self.session,
                'permissions': self.permissions,
                'current_user': self.user
            },

            # openfire transport extensions
            'transport': {

                # services config
                'services': transport,

                # realtime/push config
                'realtime': {
                    'enabled': False,
                    'channel': self.channel_token,
                    'timeout': self.channel_timeout
                }
            }
        })
        return super(WebHandler, self)._bindRuntimeTemplateContext(context)

    ## ++ HTTP Methods ++ ##
    def head(self):

        ''' Run GET, if defined, and return the headers only. '''

        if hasattr(self, 'get'):
            self.get()
        return

    def options(self):

        ''' Return available methods '''

        for k, v in self.baseHeaders.items():
            self.response.headers[k] = v
        return self.response.write(','.join([i for i in frozenset(['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS']) if hasattr(self, i.lower())]))


class MobileHandler(WebHandler):

    ''' Handler for mobile web requests. '''
