from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\core\\base_web.html'

    def root(context, environment=environment):
        parent_template = None
        l_page = context.resolve('page')
        if 0: yield None
        parent_template = environment.get_template('core/__base.html', '/source\\core\\base_web.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        if environment.getattr(l_page, 'ie'):
            if 0: yield None
        for event in parent_template.root_render_func(context):
            yield event

    def block_body(context, environment=environment):
        if 0: yield None
        yield u'\n\n<!-- Header -->\n<div id="header-container">\n\t<header id=\'superbar\' class="clearfix" role="banner">\n\t\t'
        for event in context.blocks['header'][0](context):
            yield event
        yield u'\n\t</header>\n</div>\n\n<!-- Main Content -->\n<div id="main-container">\n\t<div id="main" class="wrapper clearfix" role="main">\n\t\t'
        for event in context.blocks['main'][0](context):
            yield event
        yield u'\n\t</div> <!-- #main -->\n</div> <!-- #main-container -->\n\n<!-- Footer -->\n<div id="footer-container">\n    <footer class="wrapper" role="banner">\n        '
        for event in context.blocks['footer'][0](context):
            yield event
        yield u'\n    </footer>\n</div>\n\n'

    def block_header(context, environment=environment):
        if 0: yield None
        yield u'\n\t\t\t'
        template = environment.get_template('snippets/superbar.html', '/source\\core\\base_web.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event
        yield u'\n\t\t'

    def block_main(context, environment=environment):
        if 0: yield None
        yield u'\n        <h3>main</h3>\n\t\t'

    def block_footer(context, environment=environment):
        if 0: yield None
        yield u'\n        <h3>footer</h3>\n        '

    blocks = {'body': block_body, 'header': block_header, 'main': block_main, 'footer': block_footer}
    debug_info = '1=10&3=13&7=18&12=21&21=24&30=27&12=31&13=34&21=39&30=43'
    return locals()