from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\bbq_proposals.html'

    def root(context, environment=environment):
        l_proposals = context.resolve('proposals')
        if 0: yield None
        yield u'<h2>Proposals!</h2>\n<ul>\n    '
        l_proposal = missing
        t_1 = 1
        for l_proposal in l_proposals:
            if 0: yield None
            yield u'\n    <li>%s</li>\n    ' % (
                environment.getattr(l_proposal, 'name'), 
            )
            t_1 = 0
        if t_1:
            if 0: yield None
            yield u'\n    <li>No proposals yet!</li>\n    '
        l_proposal = missing
        yield u'\n</ul>'

    blocks = {}
    debug_info = '3=12&4=15'
    return locals()