from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/bbq/bbq_projects.html'

    def root(context, environment=environment):
        l_projects = context.resolve('projects')
        if 0: yield None
        yield u'<h2>Projects!</h2>\n<div id="project-container">\n    <div class="project-header">\n        <div class="bbq-col">Name</div>\n        <div class="bbq-col">Summary</div>\n        <div class="bbq-col">Category</div>\n        <div class="bbq-col">Status</div>\n        <div class="bbq-col">Pitch</div>\n        <div class="bbq-col">Tech</div>\n        <div class="bbq-col">Keywords</div>\n        <div class="bbq-col">Creator</div>\n        <div class="bbq-col">Owners</div>\n        <div class="bbq-col">Goals</div>\n        <div class="bbq-col">Tiers</div>\n        <div class="bbq-col">Avatar</div>\n        <div class="bbq-col">Video</div>\n        <div class="bbq-col">Images</div>\n    </div>\n    '
        l_project = missing
        l_encrypt = context.resolve('encrypt')
        t_1 = 1
        for l_project in l_projects:
            if 0: yield None
            yield u'\n    <div class="project">\n        <div class="project-info">\n            <span class="project-key" style="display: none;">%s</span>\n            <span class="project-name bbq-editable">%s</span>\n        </div>\n        <div class="project-info">\n            <span class="project-summary bbq-editable">%s</span>\n        </div>\n        <div class="project-info">\n            <span class="project-category bbq-not-editable">%s</span>\n        </div>\n        <div class="project-info">\n            <span class="project-status bbq-editable">%s</span>\n        </div>\n        <div class="project-info">\n            <span class="project-pitch bbq-editable">%s</span>\n        </div>\n        <div class="project-info">\n            <span class="project-tech bbq-editable">%s</span>\n        </div>\n        <div class="project-info">\n            <span class="project-keywords bbq-editable">%s</span>\n        </div>\n        <div class="project-info">\n            <span class="project-creator bbq-not-editable">%s</span>\n        </div>\n        <div class="project-info">\n            <span class="project-owners bbq-not-editable">%s</span>\n        </div>\n        <div class="project-info">\n            <span class="project-goals bbq-not-editable">%s</span>\n        </div>\n        <div class="project-info">\n            <span class="project-tiers bbq-not-editable">%s</span>\n        </div>\n        <div class="project-info">\n            <span class="project-avatars">\n                <img data-key="%s" src="/_assets/blob/serve/%s">\n            </span>\n        </div>\n        <div class="project-info">\n            <div id="project-%s-video">\n                <span class="project-videos">\n                    <span class="project-video bbq-not-editable">%s</span>\n                </span>\n                <div class="add-project-video">\n                    <input type="text" name="video-url">\n                    <span class="vimeo-label">Vimeo</span>\n                    <input type="radio" name="provider" value="VIMEO">\n                    <span class="vimeo-label">YouTube</span>\n                    <input type="radio" name="provider" value="YOUTUBE">\n                    <button id="add-project-%s-video" type="button" class="add-project-video-btn">+ Add Video</button>\n                </div>\n            </div>\n        </div>\n        <div class="project-info">\n            <span class="project-images">\n                ' % (
                context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_project, 'key'), 'urlsafe'))), 
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
                context.call(environment.getattr(environment.getattr(l_project, 'avatar'), 'urlsafe')), 
                context.call(environment.getattr(environment.getattr(l_project, 'avatar'), 'id')), 
                context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_project, 'key'), 'urlsafe'))), 
                ((environment.getattr(l_project, 'video') and environment.getattr(context.call(environment.getattr(environment.getattr(l_project, 'video'), 'get')), 'url')) or ''), 
                context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_project, 'key'), 'urlsafe'))), 
            )
            l_image = missing
            t_2 = 1
            for l_image in environment.getattr(l_project, 'images'):
                if 0: yield None
                yield u'\n                    \n                    <img data-key="%s" src="/_assets/blob/serve/%s">\n                ' % (
                    context.call(environment.getattr(l_image, 'urlsafe')), 
                    context.call(environment.getattr(environment.getattr(context.call(environment.getattr(l_image, 'get')), 'asset'), 'urlsafe')), 
                )
                t_2 = 0
            if t_2:
                if 0: yield None
                yield u'\n                    NO IMAGES.\n                '
            l_image = missing
            yield u'\n            </span>\n        </div>\n        <div class="project-actions">\n            <button class="delete" type="button">delete</button>\n            <button class="start-edit" type="button">edit</button>\n            <button class="cancel-edit" type="button" style="display: none;">cancel</button>\n            <button class="save-edit" type="button" style="display: none;">save</button>\n            <button class="go-live" type="button">Go-Live!</button>\n            <button class="suspend" type="button">Suspend</button>\n            <button class="shutdown" type="button">Shut Down</button>\n            <div id="project-%s-avatar" class="drop-box">\n                DROP AVATAR HERE\n            </div>\n            <div id="project-%s-image" class="drop-box">\n                DROP IMAGE HERE\n            </div>\n        </div>\n    </div>\n    ' % (
                context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_project, 'key'), 'urlsafe'))), 
                context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_project, 'key'), 'urlsafe'))), 
            )
            t_1 = 0
        if t_1:
            if 0: yield None
            yield u'\n    <div>No projects yet!</div>\n    '
        l_project = missing
        yield u'\n</div>\n'

    blocks = {}
    debug_info = '19=13&22=16&23=17&26=18&29=19&32=20&35=21&38=22&41=23&44=24&47=25&50=26&53=27&57=28&61=30&63=31&71=32&77=36&79=39&93=48&96=49'
    return locals()