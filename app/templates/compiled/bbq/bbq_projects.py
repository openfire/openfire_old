from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/bbq/bbq_projects.html'

    def root(context, environment=environment):
        l_projects = context.resolve('projects')
        if 0: yield None
        yield u'<h2>Projects (...are coming soon)!</h2>\n<ul>\n    '
        l_project = missing
        t_1 = 1
        for l_project in l_projects:
            if 0: yield None
            yield u'\n    <li>%s</li>\n    ' % (
                environment.getattr(l_project, 'name'), 
            )
            t_1 = 0
        if t_1:
            if 0: yield None
            yield u'\n    <li>No projects yet!</li>\n    '
        l_project = missing
        yield u'\n</ul>'

    blocks = {}
    debug_info = '3=12&4=15'
    return locals()