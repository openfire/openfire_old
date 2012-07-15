from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/core/__south.html'

    def root(context, environment=environment):
        l_asset = context.resolve('asset')
        l_security = context.resolve('security')
        l_page = context.resolve('page')
        l_transport = context.resolve('transport')
        if 0: yield None
        yield u'<script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>\n<script>window.jQuery || document.write(\'<script src="%s"><\\/script>\')</script>\n\n<!-- Core Scripts -->\n<script src="%s"></script>\n<script src="%s"></script>\n<script src="%s"></script>\n<script src="/assets/js/static/core/jquery/easing.min.js"></script>\n\n<!-- Base Scripts -->\n' % (
            context.call(environment.getattr(l_asset, 'script'), 'jquery', 'core'), 
            context.call(environment.getattr(l_asset, 'script'), 'modernizr', 'core'), 
            context.call(environment.getattr(l_asset, 'script'), 'underscore', 'core'), 
            context.call(environment.getattr(l_asset, 'script'), 'd3', 'core'), 
        )
        if environment.getattr(environment.getattr(l_security, 'permissions'), 'admin'):
            if 0: yield None
            yield u'\n<script src="%s"></script>\n<script src="%s"></script>\n' % (
                context.call(environment.getattr(l_asset, 'script'), 'admin', 'apptools'), 
                context.call(environment.getattr(l_asset, 'script'), 'admin', 'openfire'), 
            )
        else:
            if 0: yield None
            yield u'\n<script src="%s"></script>\n<script src="%s"></script>' % (
                context.call(environment.getattr(l_asset, 'script'), 'base', 'apptools'), 
                context.call(environment.getattr(l_asset, 'script'), 'app', 'openfire'), 
            )
        yield u'\n'
        if environment.getattr(environment.getattr(l_transport, 'realtime'), 'enabled'):
            if 0: yield None
            if environment.getattr(environment.getattr(l_transport, 'services'), 'secure'):
                if 0: yield None
                yield u'<script async src="https://%s/_ah/channel/jsapi"></script>' % (
                    environment.getattr(environment.getattr(l_transport, 'services'), 'endpoint'), 
                )
            else:
                if 0: yield None
                yield u'<script async src="http://%s/_ah/channel/jsapi"></script>' % (
                    environment.getattr(environment.getattr(l_transport, 'services'), 'endpoint'), 
                )
        yield u'\n\n\n'
        if ((environment.getattr(l_page, 'services') or environment.getattr(l_page, 'analytics')) or environment.getattr(environment.getattr(l_transport, 'realtime'), 'enabled')):
            if 0: yield None
            yield u'<script>'
            for event in context.blocks['page_services'][0](context):
                yield event
            if environment.getattr(environment.getattr(l_transport, 'services'), 'secure'):
                if 0: yield None
                yield u"$.apptools.api.rpc.action_prefix = 'https://%s';" % (
                    environment.getattr(environment.getattr(l_transport, 'services'), 'endpoint'), 
                )
            else:
                if 0: yield None
                yield u"$.apptools.api.rpc.action_prefix = 'http://%s';" % (
                    environment.getattr(environment.getattr(l_transport, 'services'), 'endpoint'), 
                )
            if environment.getattr(environment.getattr(l_transport, 'realtime'), 'enabled'):
                if 0: yield None
                yield u'$.apptools.push.config = {\n\t\ttoken: "%s",\n\t\trenew: %s,\n\t};' % (
                    environment.getattr(environment.getattr(l_transport, 'realtime'), 'token'), 
                    environment.getattr(environment.getattr(l_transport, 'realtime'), 'timeout'), 
                )
            for event in context.blocks['page_analytics'][0](context):
                yield event
            yield u'</script>'

    def block_page_services(context, environment=environment):
        l_build_page_object = context.resolve('build_page_object')
        l_page = context.resolve('page')
        if 0: yield None
        if environment.getattr(l_page, 'services'):
            if 0: yield None
            included_template = environment.get_template('macros/page_object.js', '/source/core/__south.html').module
            l_build_page_object = getattr(included_template, 'build_page_object', missing)
            if l_build_page_object is missing:
                l_build_page_object = environment.undefined("the template %r (imported on line 35 in '/source/core/__south.html') does not export the requested name 'build_page_object'" % included_template.__name__, name='build_page_object')
            yield to_string(context.call(l_build_page_object, environment.getattr(environment.getattr(l_page, 'services'), 'services_manifest'), environment.getattr(environment.getattr(l_page, 'services'), 'config'), l_page))

    def block_page_analytics(context, environment=environment):
        l_google_analytics_async = context.resolve('google_analytics_async')
        l_page = context.resolve('page')
        if 0: yield None
        if environment.getattr(l_page, 'analytics'):
            if 0: yield None
            included_template = environment.get_template('macros/page_analytics.js', '/source/core/__south.html').module
            l_google_analytics_async = getattr(included_template, 'google_analytics_async', missing)
            if l_google_analytics_async is missing:
                l_google_analytics_async = environment.undefined("the template %r (imported on line 55 in '/source/core/__south.html') does not export the requested name 'google_analytics_async'" % included_template.__name__, name='google_analytics_async')
            yield u'\n\t\t'
            yield to_string(context.call(l_google_analytics_async, environment.getattr(l_page, 'analytics')))

    blocks = {'page_services': block_page_services, 'page_analytics': block_page_analytics}
    debug_info = '2=13&5=14&6=15&7=16&11=18&12=21&13=22&15=27&16=28&20=31&21=33&22=36&24=41&31=44&33=47&40=49&41=52&43=57&46=59&48=62&49=63&53=65&33=69&34=73&35=75&36=79&53=81&54=85&55=87&56=92'
    return locals()