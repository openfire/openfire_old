from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/security/login.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('layout/security.html', '/source/security/login.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_content(context, environment=environment):
        l_federated = context.resolve('federated')
        if 0: yield None
        yield u'\n\n\t<div id="login_wrapper" data-federated="'
        if l_federated:
            if 0: yield None
            yield u'true'
        else:
            if 0: yield None
            yield u'false'
        yield u'">\n\t\t'
        template = environment.get_template('snippets/login_box.html', '/source/security/login.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event
        yield u'\n\t</div>\n\n'

    blocks = {'content': block_content}
    debug_info = '1=9&3=15&5=19&6=26'
    return locals()