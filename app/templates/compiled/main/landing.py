from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\main\\landing.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('layout/landing.html', '/source\\main\\landing.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_postsouth(context, environment=environment):
        if 0: yield None
        yield u'\n<script type="text/javascript">\n$(document).ready(function () {\n\t$.apptools.widgets.modal._init();\n});\n</script>\n'

    blocks = {'postsouth': block_postsouth}
    debug_info = '1=9&3=15'
    return locals()