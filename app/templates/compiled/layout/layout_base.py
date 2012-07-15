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
        included_template = environment.get_template('macros/eggs.html', '/source/layout/layout_base.html').module
        l_random_greeting = getattr(included_template, 'random_greeting', missing)
        if l_random_greeting is missing:
            l_random_greeting = environment.undefined("the template %r (imported on line 2 in '/source/layout/layout_base.html') does not export the requested name 'random_greeting'" % included_template.__name__, name='random_greeting')
        context.vars['random_greeting'] = l_random_greeting
        context.exported_vars.discard('random_greeting')
        for event in parent_template.root_render_func(context):
            yield event

    def block_rightnav(context, environment=environment):
        l_gravatarify = context.resolve('gravatarify')
        l_random_greeting = context.resolve('random_greeting')
        l_link = context.resolve('link')
        l_security = context.resolve('security')
        if 0: yield None
        yield u"\n\t<ul class='right'>\n\n\t\t"
        if environment.getattr(l_security, 'current_user'):
            if 0: yield None
            yield u'  \n\t\t\t<li class=\'profiletab\'>\n\t\t\t\t<a href="/me" title=\'Profile\'>%s</a>\n\t\t\t\t<img src="%s" width=\'32\' height=\'32\' alt=\'you!\' />\n\t\t\t</li>\n\t\t' % (
                context.call(l_random_greeting, environment.getattr(l_security, 'current_user'), environment.getattr(l_security, 'session')), 
                context.call(l_gravatarify, context.call(environment.getattr(environment.getattr(l_security, 'session'), 'get'), 'email'), 'jpg', '32'), 
            )
        else:
            if 0: yield None
            yield u'\n\t\t\t<li><a id=\'signup_trigger\' href="%s" title="Sign Up">Sign Up</a></li>\n\t\t\t<li><a id=\'login_trigger\' href="%s" title="Log In">Log In</a></li>\n\t\t' % (
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
    debug_info = '1=9&2=12&24=21&27=28&29=31&30=32&33=37&34=38&9=42&11=47&47=51&17=55&19=59&20=60&53=63&45=67&47=70&53=73&4=77&5=81&8=84&9=87&17=90&24=93&42=97'
    return locals()