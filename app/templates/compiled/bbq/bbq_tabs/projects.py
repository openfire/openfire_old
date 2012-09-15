from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\bbq_tabs\\projects.html'

    def root(context, environment=environment):
        l_projects = context.resolve('projects')
        if 0: yield None
        yield u'<h2>openfire projects</h2>\n<div class="content">\n    <table id="bbq-project-table" class="bbq-datatable">\n        <thead>\n            <tr>\n                <th>Name</th>\n                <th>URL</th>\n                <th>Status</th>\n                <th>Summary</th>\n                <th>Owners</th>\n                <th>Category</th>\n                <th>Progress</th>\n                <th>Total Raised</th>\n            </tr>\n        </thead>\n        <tbody>\n            '
        l_project = missing
        for l_project in l_projects:
            if 0: yield None
            yield u'\n            <tr>\n                <td><a href="/%s">%s</a></td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>\n                    ' % (
                context.call(environment.getattr(l_project, 'get_custom_url')), 
                environment.getattr(l_project, 'name'), 
                context.call(environment.getattr(l_project, 'get_custom_url')), 
                environment.getattr(l_project, 'status'), 
                environment.getattr(l_project, 'summary'), 
            )
            l_owner = missing
            for l_owner in environment.getattr(l_project, 'owners'):
                if 0: yield None
                yield u'\n                        %s, &nbsp;\n                    ' % (
                    context.call(environment.getattr(l_owner, 'id')), 
                )
            l_owner = missing
            yield u'\n                </td>\n                <td>%s</td>\n                <td>%s%%</td>\n                <td>$%s</td>\n            </tr>\n            ' % (
                context.call(environment.getattr(environment.getattr(l_project, 'category'), 'id')), 
                environment.getattr(l_project, 'progress'), 
                environment.getattr(l_project, 'money'), 
            )
        l_project = missing
        yield u'\n        </tbody>\n    </table>\n</div>\n'

    blocks = {}
    debug_info = '17=11&19=14&20=16&21=17&22=18&24=21&25=24&28=28&29=29&30=30'
    return locals()