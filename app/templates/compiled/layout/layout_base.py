from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/layout/layout_base.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('core/base_web.html', '/source/layout/layout_base.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_rightnav(context, environment=environment):
        l_util = context.resolve('util')
        l_api = context.resolve('api')
        l_link = context.resolve('link')
        if 0: yield None
        yield u"\n\t<ul class='right'>\n\n\t\t"
        if context.call(environment.getattr(environment.getattr(l_api, 'users'), 'get_current_user')) != None:
            if 0: yield None
            yield u'  \n\t\t\t<li class=\'profiletab\'>\n\t\t\t\t<a href="/me" title=\'Profile\'>%s</a>\n\t\t\t\t<img src="http://www.gravatar.com/avatar/%s.jpg?s=32&d=http://placehold.it/32/ffffff.png" />\n\t\t\t</li>\n\t\t' % (
                context.call(environment.getattr(context.call(environment.getattr(environment.getattr(l_api, 'users'), 'get_current_user')), 'nickname')), 
                context.call(environment.getattr(context.call(environment.getattr(environment.getattr(environment.getattr(l_util, 'converters'), 'hashlib'), 'md5'), context.call(environment.getattr(context.call(environment.getattr(environment.getattr(l_api, 'users'), 'get_current_user')), 'email'))), 'hexdigest')), 
            )
        else:
            if 0: yield None
            yield u'\n\t\t\t<li><a href="%s" title="Sign Up">Sign Up</a></li>\n\t\t\t<li><a href="%s" title="Log In">Log In</a></li>\n\t\t' % (
                context.call(l_link, 'auth/logout'), 
                context.call(l_link, 'auth/login'), 
            )
        yield u'\n\n\t</ul>\n\t'

    def block_tinylogo(context, environment=environment):
        l_link = context.resolve('link')
        l_asset = context.resolve('asset')
        if 0: yield None
        yield u'\n<div id=\'tinylogo\'>\n\t<a title="openfire home" href=\'%s\'><img src=\'%s\' /></a>\n</div>\n' % (
            context.call(l_link, 'landing'), 
            context.call(environment.getattr(l_asset, 'image'), 'branding/oflogo', 'of_small_transparent.png'), 
        )

    def block_footerleft(context, environment=environment):
        if 0: yield None
        yield u"\n\t\t<div class='left'>\n\t        BETA - work in progress\n\t    </div>\n    "

    def block_leftnav(context, environment=environment):
        l_link = context.resolve('link')
        if 0: yield None
        yield u'\n\t<ul class=\'left\'>\n\t\t<li><a href="%s" title="openfire home">Home</a></li>\n\t\t<li><a href="%s" title="browse projects">Projects</a></li>\n\t</ul>\n\t' % (
            context.call(l_link, 'landing'), 
            context.call(l_link, 'project/landing'), 
        )

    def block_footerright(context, environment=environment):
        if 0: yield None
        yield u"\n\t\t<div class='right'>\n\t        copyright (c) 2012, openfire\n\t    </div>\n    "

    def block_footer(context, environment=environment):
        if 0: yield None
        yield u"\n    <div id='footer-content'>\n    "
        for event in context.blocks['footerleft'][0](context):
            yield event
        yield u'\n\n    '
        for event in context.blocks['footerright'][0](context):
            yield event
        yield u'\n    </div>\n'

    def block_stylesheets(context, environment=environment):
        l_asset = context.resolve('asset')
        if 0: yield None
        yield u'\n\t<link rel="stylesheet" href="%s">\n' % (
            context.call(environment.getattr(l_asset, 'style'), 'main', 'compiled'), 
        )

    def block_header(context, environment=environment):
        if 0: yield None
        yield u'\n'
        for event in context.blocks['tinylogo'][0](context):
            yield event
        yield u'\n\n<nav role="navigation">\n\n\t'
        for event in context.blocks['leftnav'][0](context):
            yield event
        yield u'\n\n\t'
        for event in context.blocks['rightnav'][0](context):
            yield event
        yield u'\n</nav>\n'

    def block_main(context, environment=environment):
        if 0: yield None
        yield u'\n'

    blocks = {'rightnav': block_rightnav, 'tinylogo': block_tinylogo, 'footerleft': block_footerleft, 'leftnav': block_leftnav, 'footerright': block_footerright, 'footer': block_footer, 'stylesheets': block_stylesheets, 'header': block_header, 'main': block_main}
    debug_info = '1=9&23=15&26=21&28=24&29=25&32=30&33=31&8=35&10=40&46=44&16=48&18=52&19=53&52=56&44=60&46=63&52=66&3=70&4=74&7=77&8=80&16=83&23=86&41=90'
    return locals()