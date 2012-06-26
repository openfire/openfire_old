from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/user/profile.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('layout/profile.html', '/source/user/profile.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_profile(context, environment=environment):
        if 0: yield None
        yield u'\n    <div>\n        <p>Other profile info</p>\n    </div>\n'

    def block_avatar(context, environment=environment):
        if 0: yield None
        yield u'\n    <div>\n        <p>Picture/avatar</p>\n    </div>\n'

    blocks = {'profile': block_profile, 'avatar': block_avatar}
    debug_info = '1=9&9=15&3=19'
    return locals()