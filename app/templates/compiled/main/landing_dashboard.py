from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\main\\landing_dashboard.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('layout/landing.html', '/source\\main\\landing_dashboard.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_projects(context, environment=environment):
        if 0: yield None
        yield u'\n    <div>\n        <p>PROJECTS</p>\n    </div>\n'

    def block_activity(context, environment=environment):
        if 0: yield None
        yield u'\n    <div>\n        <p>ACTIVITY FOR LOGGED IN USER</p>\n    </div>\n'

    blocks = {'projects': block_projects, 'activity': block_activity}
    debug_info = '1=9&3=15&9=19'
    return locals()