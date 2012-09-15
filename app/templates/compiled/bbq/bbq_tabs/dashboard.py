from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\bbq_tabs\\dashboard.html'

    def root(context, environment=environment):
        if 0: yield None
        yield u'<h2>openfire admin dashboard</h2>\n<div class="content">\n    More to come!\n</div>'

    blocks = {}
    debug_info = ''
    return locals()