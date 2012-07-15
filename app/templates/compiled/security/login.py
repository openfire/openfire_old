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
        l_security = context.resolve('security')
        l_encrypt = context.resolve('encrypt')
        l_federated = context.resolve('federated')
        if 0: yield None
        yield u'\n\n<div id=\'splash\' class="rounded-big center-all">\n\n\t<div id="login_wrapper" data-federated="'
        if l_federated:
            if 0: yield None
            yield u'true'
        else:
            if 0: yield None
            yield u'false'
        yield u'" data-csrf="%s">\n\n\t\t' % (
            context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_security, 'session'), 'get'), 'sid', '__DEV__')), 
        )
        template = environment.get_template('snippets/login_box.html', '/source/security/login.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event
        yield u'\n\n\t</div><!-- end #login_wrapper -->\n\n</div><!-- end #splash -->\n\n'

    blocks = {'content': block_content}
    debug_info = '1=9&3=15&7=21&9=30'
    return locals()