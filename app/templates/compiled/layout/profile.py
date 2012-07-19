from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/layout/profile.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('layout/layout_base.html', '/source/layout/profile.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_profile(context, environment=environment):
        if 0: yield None
        yield u'\n        <div>\n          <h1>User proifle</h1>\n        </div>\n    '

    def block_main(context, environment=environment):
        if 0: yield None
        yield u'\n\n    '
        for event in context.blocks['avatar'][0](context):
            yield event
        yield u'\n\n    '
        for event in context.blocks['profile'][0](context):
            yield event
        yield u'\n\n'

    def block_avatar(context, environment=environment):
        if 0: yield None
        yield u'\n        <div>\n          <h1>User avatar</h1>\n        </div>\n    '

    blocks = {'profile': block_profile, 'main': block_main, 'avatar': block_avatar}
    debug_info = '1=9&11=15&3=19&5=22&11=25&5=29'
    return locals()