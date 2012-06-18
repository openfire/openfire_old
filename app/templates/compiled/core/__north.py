from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\core\\__north.html'

    def root(context, environment=environment):
        l_page = context.resolve('page')
        l_asset = context.resolve('asset')
        if 0: yield None
        yield u'<!-- Stylesheets -->\n'
        for event in context.blocks['stylesheets'][0](context):
            yield event
        yield u'\n\n'
        if environment.getattr(l_page, 'ie'):
            if 0: yield None
            yield u'\n\t<link rel="stylesheet" href="%s">\n' % (
                context.call(environment.getattr(l_asset, 'style'), 'ie', 'compiled'), 
            )

    def block_stylesheets(context, environment=environment):
        if 0: yield None
        yield u'\n\t<link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Satisfy">\n\t<link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Karla:400,700,400italic,700italic">\n'

    blocks = {'stylesheets': block_stylesheets}
    debug_info = '2=11&7=14&8=17&2=20'
    return locals()