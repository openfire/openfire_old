# -*- coding: utf-8 -*-
import webapp2
from jinja2 import nodes
from config import config
from apptools.util import debug
from openfire.core.content import ContentBridge
from openfire.core.output.extensions import OutputExtension

_extensionConfig = config.get('openfire.output.extension.DynamicContent')


## DynamicContentExtension
class DynamicContent(OutputExtension):

    ''' Extends Jinja2 to support custom openfire dynamic content tags. '''

    tags = set(['content', 'snippet', 'summary'])

    @webapp2.cached_property
    def __config(self):

        ''' Cached config. '''

        return _extensionConfig

    @webapp2.cached_property
    def __logging(self):

        ''' Cached log pipe. '''

        return debug.AppToolsLogger(path='openfire.output.extensions', name='DynamicContent')._setcondition(self.__config.get('logging', False))

    def __init__(self, environment):

        ''' Extend the attached environment. '''

        super(DynamicContent, self).__init__(environment)

        if self.__config.get('config').get('enabled', False) == True:

            self.logging.info('DynamicContent output extension enabled and loaded properly. Attaching to template enviornment.')

            # make our content bridge
            bridge = ContentBridge(app=environment.wsgi_current_application, handler=environment.wsgi_current_handler, environment=self)

            self.logging.info('==Default Namespace: "%s"' % self.__config.get('config').get('default_namespace', '__EMPTY__'))
            self.logging.info('==Content Bridge: "%s"' % bridge)

            # add the defaults to the environment
            environment.extend(
                default_dynamic_namespace=self.__config.get('config').get('default_namespace', None),
                dynamic_content_bridge=bridge
            )

    def parse(self, parser):

        ''' Jinja2 Parse Hook '''

        # the first token is the token that started the tag. in our case
        # we listen on `content`, `snippet`, `summary`. so this will be a
        # name token with one of those values. we get the line number so
        # that we can give that line number to the nodes we create by hand.
        lineno = parser.stream.next().lineno

        # now we parse a single expression that is used as the content area
        # key name, before we get to optional args/kwargs
        args = [parser.parse_expression()]

        # if there is a comma, use that as an override of the default content
        # area namespace for the current environment
        if parser.stream.skip_if('comma'):
            args.append(parser.parse_expression())
        else:
            args.append(nodes.Const(None))

        # now we parse the body of the cache block up to the apprpriate `end`
        # tag, and drop the needle to place the parser after our dynamic block
        body = parser.parse_statements(['name:endcontent', 'name:endsnippet', 'name:endsummary', 'name:end'], drop_needle=True)

        # now return the `CallBlock` node that calls the appropriate extension
        # method from the attached enfironment

        return nodes.CallBlock(self.call_method('_callback', args), [], [], body).set_lineno(lineno)

    def _callback(self, keyname, namespace, caller):

        ''' Helper callback. '''

        # resolve namespace
        if namespace is None:
            if hasattr(self.environment, 'default_dynamic_namespace'):
                namespace = self.environment.default_dynamic_namespace
            else:
                namespace = '__system__'

        return caller()
