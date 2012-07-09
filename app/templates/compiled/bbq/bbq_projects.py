from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/bbq/bbq_projects.html'

    def root(context, environment=environment):
        l_projects = context.resolve('projects')
        if 0: yield None
        yield u'<h2>Projects!</h2>\n<div id="project-container">\n    '
        l_project = missing
        t_1 = 1
        for l_project in l_projects:
            if 0: yield None
            yield u'\n    <div class="project">\n        <div class="project-info">\n            <span class="project-key" style="display: none;">%s</span>\n            <label>Name: </label>\n            <span class="project-name editable">%s</span>\n            <label>Summary: </label>\n            <span class="project-summary editable">%s</span>\n            <label>Category: </label>\n            <span class="project-category editable">%s</span>\n            <label>Status: </label>\n            <span class="project-status editable">%s</span>\n            <label>Pitch: </label>\n            <span class="project-pitch editable">%s</span>\n            <label>Tech: </label>\n            <span class="project-tech editable">%s</span>\n            <label>Keywords: </label>\n            <span class="project-keywords editable">%s</span>\n            <label>Creator: </label>\n            <span class="project-creator editable">%s</span>\n            <label>Owners: </label>\n            <span class="project-owners editable">%s</span>\n            <label>Goals: </label>\n            <span class="project-goals editable">%s</span>\n            <label>Tiers: </label>\n            <span class="project-tiers editable">%s</span>\n        </div>\n        <div>\n            <button class="delete" type="button">delete</button>\n            <button class="start-edit" type="button">edit</button>\n            <button class="cancel-edit" type="button" style="display: none;">cancel</button>\n            <button class="save-edit" type="button" style="display: none;">save</button>\n            <button class="go-live" type="button">Go-Live!</button>\n            <button class="suspend" type="button">Suspend</button>\n            <button class="shutdown" type="button">Shut Down</button>\n        </div>\n    </div>\n    ' % (
                context.call(environment.getattr(environment.getattr(l_project, 'key'), 'urlsafe')), 
                environment.getattr(l_project, 'name'), 
                environment.getattr(l_project, 'summary'), 
                environment.getattr(l_project, 'category'), 
                environment.getattr(l_project, 'status'), 
                environment.getattr(l_project, 'pitch'), 
                environment.getattr(l_project, 'tech'), 
                environment.getattr(l_project, 'keywords'), 
                environment.getattr(l_project, 'creator'), 
                environment.getattr(l_project, 'owners'), 
                environment.getattr(l_project, 'goals'), 
                environment.getattr(l_project, 'tiers'), 
            )
            t_1 = 0
        if t_1:
            if 0: yield None
            yield u'\n    <div>No projects yet!</div>\n    '
        l_project = missing
        yield u'\n</div>\n'

    blocks = {}
    debug_info = '3=12&6=15&8=16&10=17&12=18&14=19&16=20&18=21&20=22&22=23&24=24&26=25&28=26'
    return locals()