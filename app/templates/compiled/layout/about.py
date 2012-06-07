from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/layout/about.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('layout/layout_base.html', '/source/layout/about.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_info(context, environment=environment):
        if 0: yield None
        yield u'\n        INFO\n    '

    def block_main(context, environment=environment):
        if 0: yield None
        yield u'\n\n    '
        for event in context.blocks['info'][0](context):
            yield event
        yield u'\n\n'

    blocks = {'info': block_info, 'main': block_main}
    debug_info = '1=9&5=15&3=19&5=22'
    return locals()