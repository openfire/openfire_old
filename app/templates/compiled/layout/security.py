from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/layout/security.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('core/__base.html', '/source/layout/security.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_stylesheets(context, environment=environment):
        l_asset = context.resolve('asset')
        if 0: yield None
        yield u'\n<link rel="stylesheet" href="%s">\n' % (
            context.call(environment.getattr(l_asset, 'style'), 'security', 'compiled'), 
        )

    def block_body(context, environment=environment):
        if 0: yield None
        yield u'\n\n<div class="snapall page-bg">\n\n    <div id="logobox">\n        <img src="https://d2ipw8y1masjpy.cloudfront.net/static/branding/openfire_transparent_optimized.png" alt=\'openfire!\' width="600" height="173" />\n    </div>\n\n    <div id=\'splash\' class="rounded-big center-all">\n        '
        for event in context.blocks['content'][0](context):
            yield event
        yield u'\n    </div> <!-- end #splash -->\n</div> <!-- end .snapall -->\n\n'

    def block_content(context, environment=environment):
        if 0: yield None
        yield u'<b>SECURITY</b>'

    blocks = {'stylesheets': block_stylesheets, 'body': block_body, 'content': block_content}
    debug_info = '1=9&3=15&4=19&7=22&16=25'
    return locals()