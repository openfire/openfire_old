from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\core\\__south.html'

    def root(context, environment=environment):
        l_util = context.resolve('util')
        l_asset = context.resolve('asset')
        l_page = context.resolve('page')
        if 0: yield None
        yield u'<script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>\n<script>window.jQuery || document.write(\'<script src="%s"><\\/script>\')</script>\n\n<!-- Core Scripts -->\n<script src="%s"></script>\n<script src="%s"></script>\n<script src="/assets/js/static/core/jquery/easing.min.js"></script>\n\n<!-- Base Scripts -->\n<script src="/_ah/channel/jsapi"></script>' % (
            context.call(environment.getattr(l_asset, 'script'), 'jquery', 'core'), 
            context.call(environment.getattr(l_asset, 'script'), 'modernizr', 'core'), 
            context.call(environment.getattr(l_asset, 'script'), 'underscore', 'core'), 
        )
        if context.call(environment.getattr(environment.getattr(environment.getattr(l_util, 'api'), 'users'), 'is_current_user_admin')):
            if 0: yield None
            yield u'<script src="/assets/js/static/apptools/base.admin.js"></script> '
        else:
            if 0: yield None
            yield u'<script src="%s"></script>' % (
                context.call(environment.getattr(l_asset, 'script'), 'base', 'apptools'), 
            )
        yield u'<!-- Project Scripts -->'
        if context.call(environment.getattr(environment.getattr(environment.getattr(l_util, 'api'), 'users'), 'is_current_user_admin')):
            if 0: yield None
            yield u'<script src="%s"></script>' % (
                context.call(environment.getattr(l_asset, 'script'), 'admin', 'openfire'), 
            )
        else:
            if 0: yield None
            yield u'<script src="%s"></script>' % (
                context.call(environment.getattr(l_asset, 'script'), 'app', 'openfire'), 
            )
        yield u'\n\n\n\n'
        if (environment.getattr(l_page, 'services') or environment.getattr(l_page, 'analytics')):
            if 0: yield None
            yield u'<script>\n'
            for event in context.blocks['page_services'][0](context):
                yield event
            yield u'\n\n'
            for event in context.blocks['page_analytics'][0](context):
                yield event
            yield u'\n</script>'

    def block_page_services(context, environment=environment):
        l_build_page_object = context.resolve('build_page_object')
        l_page = context.resolve('page')
        if 0: yield None
        if environment.getattr(l_page, 'services'):
            if 0: yield None
            included_template = environment.get_template('macros/page_object.js', '/source\\core\\__south.html').module
            l_build_page_object = getattr(included_template, 'build_page_object', missing)
            if l_build_page_object is missing:
                l_build_page_object = environment.undefined("the template %r (imported on line 34 in '/source\\\\core\\\\__south.html') does not export the requested name 'build_page_object'" % included_template.__name__, name='build_page_object')
            yield u'\n\t'
            yield to_string(context.call(l_build_page_object, environment.getattr(environment.getattr(l_page, 'services'), 'services_manifest'), environment.getattr(environment.getattr(l_page, 'services'), 'config'), l_page))

    def block_page_analytics(context, environment=environment):
        l_google_analytics_async = context.resolve('google_analytics_async')
        l_page = context.resolve('page')
        if 0: yield None
        if environment.getattr(l_page, 'analytics'):
            if 0: yield None
            included_template = environment.get_template('macros/page_analytics.js', '/source\\core\\__south.html').module
            l_google_analytics_async = getattr(included_template, 'google_analytics_async', missing)
            if l_google_analytics_async is missing:
                l_google_analytics_async = environment.undefined("the template %r (imported on line 41 in '/source\\\\core\\\\__south.html') does not export the requested name 'google_analytics_async'" % included_template.__name__, name='google_analytics_async')
            yield u'\n\t\t'
            yield to_string(context.call(l_google_analytics_async, environment.getattr(l_page, 'analytics')))

    blocks = {'page_services': block_page_services, 'page_analytics': block_page_analytics}
    debug_info = '2=12&5=13&6=14&11=16&14=22&18=25&19=28&21=33&30=36&32=39&39=42&32=46&33=50&34=52&35=57&39=59&40=63&41=65&42=70'
    return locals()