# -*- coding: utf-8 -*-

## Base Imports
import config
import webapp2

## Jinja2 Imports
from jinja2 import Template
from jinja2.ext import Extension
from jinja2.bccache import BytecodeCache
from jinja2.exceptions import TemplateNotFound

## Core Imports
from openfire.core import CoreAPI

## Extras Imports
from webapp2_extras import jinja2

## AppTools Imports
from apptools.api import output

## NDB Imports
from google.appengine.ext import ndb
from google.appengine.ext.ndb import context
from google.appengine.ext.ndb import tasklet

## SDK Imports
from google.appengine.api import memcache
from google.appengine.ext import blobstore

## Openfire Imports
from openfire.models import content as models


## CoreContentAPI - manages the retrieval and update of dynamically editable site content
class CoreContentAPI(CoreAPI):

    ''' Core API for managing dynamic content. '''

    # Content Models
    areas = []
    futures = []
    snippets = []
    summaries = []

    # Structure Cache
    keygroups = []
    heuristics = []

    # Class References
    app = None
    handler = None
    service = None
    templates = {}
    environment = None

    ## == Low-level Methods == ##
    @tasklet
    def _batch_fulfill(self, batch):
        pass

    @tasklet
    def _run_query(self, query, options):
        pass

    @tasklet
    def _consider_result(self, result):
        pass

    ## == Mid-level Methods == ##
    def _build_keygroup(self):
        pass

    def _build_area_key(self):
        pass

    def _build_snippet_key(self):
        pass

    def _build_summary_key(self):
        pass

    def _walk_jinja2_ast(self):
        pass

    def _inner_ast_hook(self):
        pass

    def _load_template(self, environment, name):

        ''' Load a template from source/compiled packages and preprocess. '''

        loader = environment.loader
        try:
            source, template, uptodate = loader.get_source(environment, name)
        except TemplateNotFound:
            raise
        else:
            #parsed_ast = environment.parse(environment.preprocess(source))
            bcc = environment.bytecode_cache
            if bcc is not None:
                bucket = bcc.get_bucket(environment, name, template, source)
                code = bucket.code

            if code is None:
                code = environment.compile(source, name, template)

            if bcc is not None and bucket.code is None:
                bucket.code = code
                bcc.set_bucket(bucket)

            return environment.template_class.from_code(environment, code, environment.globals, uptodate)

    ## == High-level Methods == ##
    def preload_content(self, areas):

        ''' Preload a set of content areas asynchronously '''

        pass

    def encounter_content_area(self):

        ''' Encounter a content area during render. '''

        pass

    def prerender(self, environment, path_or_template):

        ''' Prerender the currently selected template. '''

        # If it's a string path...
        if isinstance(path_or_template, basestring):

            # If we have it in the threadcache...
            if path_or_template in self.templates:
                template_object = self.templates[path_or_template]
            else:
                self.templates[path_or_template] = self._load_template(environment, path_or_template)
                template_object = self.templates[path_or_template]

        return template_object

    def render(self, template, context):

        ''' Render a template, given context '''

        if template is None:
            raise ValueError('Must pass in a template object or path to template source or an iterable of those.')
        else:
            return template.render(**context)


## Globals
_output_loader = None
_output_extensions = {}
_output_bytecacher = None
_output_api_instance = CoreContentAPI()


## ContentBridge - brings Core Content API functionality down into an easy mixin
class ContentBridge(object):

    ''' Mixin that bridges dynamic content methods into RemoteServices and WebHandlers. '''

    # References
    __app = None
    __handler = None
    __service = None
    __environment = None

    # Bridge state
    __content_bridge = None
    __content_prerender = None

    def __init__(self, app=None, handler=None, service=None, environment=None):

        ''' Initialize the content bridge. '''

        if app is not None:
            self._initialize_dynamic_content(app, handler, service, environment)

    def _initialize_dynamic_content(self, app, handler=None, service=None, environment=None):

        ''' Initialize the content bridge from an already-instantiated Handler or Service. '''

        self.__app = app
        if handler:
            self.__handler = handler
        elif service:
            self.__service = service
            self.__handler = service.handler
        if self.__app is None:
            self.__app = self.__handler.app
        if environment:
            self.__environment = environment
        self.__acquire_content_bridge()
        return

    @webapp2.cached_property
    def _environment(self):

        ''' Cached access to the current template environment. '''

        if self.__environment is None:
            self.__environment = self.dynamicEnvironmentFactory(self.__app)
        return self.__environment

    def __acquire_content_bridge(self):

        ''' Resolve the current instance of the CoreContentAPI, or create one. '''

        global _output_api_instance
        if self.__content_bridge is not None:
            return self.__content_bridge
        else:
            if _output_api_instance is not None:
                self.__content_bridge = _output_api_instance
            else:
                self.__content_bridge = _output_api_instance = CoreContentAPI()
        return self.__content_bridge

    def preload_template(self, template):

        ''' Preload and pre-render (pre-bytecompile) a template before rendering begins. '''

        if self.__content_bridge is None:
            self.__acquire_content_bridge()
        self.__content_prerender = self.__content_bridge.prerender(self._environment, template)
        return self.__content_prerender

    def dynamicEnvironmentFactory(self, app):

        ''' Prepare a Jinja2 environment suitable for rendering openfire templates. '''

        global _output_loader
        global _output_extensions
        global _output_bytecacher

        if self.__environment is not None:
            return self.__environment

        else:

            # get openfire extension config
            self.logging.info('Preparing Jinja2 OF template execution environment.')

            # use output logging condition for a minute
            self.logging._setcondition(self._ofOutputConfig.get('extensions').get('config').get('logging'))

            # get jinja2 base config
            j2cfg = self._jinjaConfig
            base_environment_args = j2cfg.get('environment_args')
            base_extensions_list = base_environment_args.get('extensions')

            if self._ofOutputConfig.get('extensions', {}).get('config').get('enabled', False) == True:

                if isinstance(_output_extensions, dict) and (len(_output_extensions) == len(base_extensions_list)):
                    compiled_extension_list = _output_extensions.values()

                else:
                    # Seen classes
                    installed_bytecaches = []
                    installed_extensions = []

                    if (len(self._webHandlerConfig.get('extensions').get('load')) + len(base_extensions_list)) > 0:
                        for name in self._webHandlerConfig.get('extensions').get('load') + base_extensions_list:
                            if name in self._ofOutputConfig.get('extensions').get('installed'):
                                if self._ofOutputConfig.get('extensions').get('installed').get(name).get('enabled', False) == True:
                                    extension_path = self._ofOutputConfig.get('extensions').get('installed').get(name).get('path')
                                else:
                                    continue
                            else:
                                extension_path = name

                            try:
                                extension = webapp2.import_string(extension_path)

                            except ImportError:
                                self.logging.error('Encountered ImportError when trying to import extension at name "%s" and path "%s"' % (name, extension_path))

                            else:
                                if issubclass(extension, Extension):
                                    installed_extensions.append((name, extension))
                                    _output_extensions[name] = extension
                                elif issubclass(extension, BytecodeCache):
                                    installed_bytecaches.append((name, extension))

                        # combine extensions and load
                        compiled_extension_list = []
                        map(lambda x: compiled_extension_list.append(x),
                            filter(lambda x: x not in compiled_extension_list,
                                map(lambda x: isinstance(x, basestring) and webapp2.import_string(x) or x,
                                    [e for (n, e) in installed_extensions])))

                    else:
                        self.logging.warning('No extensions installed/found in config (at "openfire.output").')

            else:
                installed_bytecaches = []
                installed_extensions = []
                compiled_extension_list = []

            templates_compiled_target = j2cfg.get('compiled_path')
            use_compiled = not config.debug or j2cfg.get('force_compiled', False)

            # resolve loader/s
            if _output_loader is not None:
                _loader = _output_loader
            else:
                if templates_compiled_target is not None and use_compiled:
                    _loader = output.ModuleLoader(templates_compiled_target)
                else:
                    _loader = output.CoreOutputLoader(j2cfg.get('template_path'))
                _output_loader = _loader

            self.logging.info('Final extensions list: "%s".' % compiled_extension_list)
            self.logging.info('Chosen loader: "%s".' % _loader)

            # resolve bytecacher/s
            if _output_bytecacher is not None:
                _bytecacher = _output_bytecacher
            else:
                if len(installed_bytecaches) > 0:
                    _output_bytecacher = installed_bytecaches[0][1]()
                    _bytecacher = _output_bytecacher

            # bind environment args
            base_environment_args['loader'] = _loader
            base_environment_args['extensions'] = compiled_extension_list
            base_environment_args['bytecode_cache'] = _bytecacher

            # hook up filters
            filters = {
                'currency': lambda x: self._format_as_currency(x, False),
                'percentage': lambda x: self._format_as_currency(x, True)
            }

            # generate environment
            finalConfig = dict(j2cfg.items()[:])
            finalConfig.update({'environment_args': base_environment_args, 'globals': self.baseContext, 'filters': filters})
            environment = jinja2.Jinja2(app, config=finalConfig).environment

            # patch in app, handler, ext and api
            environment.extend(**{
                'wsgi_current_application': app,
                'wsgi_current_handler': self,
                'jinja2_current_loader': _loader,
                'jinja2_current_bytecache': base_environment_args.get('bytecode_cache')
            })

            # replace logging conditional
            self.logging._setcondition(self._webHandlerConfig.get('logging'))
            self.__environment = environment

            return self.__environment

    def render_dynamic(self, path=None, context={}, elements={}, content_type='text/html', headers={}, dependencies=[], flush=True, **kwargs):

            ''' Render shim for advanced dynamic content rendering. '''

            # Provide render options to template
            _render_opts = {
                'path': path,
                'self': self,
                'context': context,
                'elements': elements,
                'content_type': content_type,
                'headers': headers,
                'dependencies': dependencies,
                'kwargs': kwargs
            }

            context['__render_opts'] = _render_opts

            # Layer on user context
            if isinstance(self.context, dict) and len(self.context) > 0:
                self.context.update(context)
            else:
                self.context = context

            # Build response headers
            response_headers = {}
            for key, value in self.baseHeaders.items():
                response_headers[key] = value

            # Consider kwargs
            if len(kwargs) > 0:
                self.context.update(kwargs)

            # Bind runtime-level template context
            self.context = self._bindRuntimeTemplateContext(self.context)

            # Bind elements
            if len(elements) > 0:
                map(self._setcontext, elements)

            # If we have a pre-render, use it, otherwise load and render
            if self.__content_prerender is not None:
                rendered = self.__content_bridge.render(self.__content_prerender, self.context)

            else:
                # Get/select the template using our environment
                rendered = self.__content_bridge.prerender(self._environment, path).render(self.context)

            if flush:
                # Output rendered template
                return self.response.write(rendered)
            else:
                # Return rendered template
                return rendered
