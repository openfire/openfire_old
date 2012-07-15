from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/bbq/bbq_custom_urls.html'

    def root(context, environment=environment):
        l_custom_urls = context.resolve('custom_urls')
        l_projects = context.resolve('projects')
        l_users = context.resolve('users')
        if 0: yield None
        yield u'<h2>Custom URLs!</h2>\n<a id="a-new-custom-url-dialog" href="#new-custom-url-dialog">+ Add New Custom Url</a>\n<div id="custom-url-container">\n    <div class="custom-url-header">\n        <div class="bbq-col">Slug</div>\n        <div class="bbq-col">Target</div>\n    </div>\n    '
        l_custom_url = missing
        l_encrypt = context.resolve('encrypt')
        for l_custom_url in l_custom_urls:
            if 0: yield None
            yield u'\n    <div class="custom-url">\n        <div class="custom-url-info">\n            <span class="custom-url-slug bbq-editable">%s</span>\n        </div>\n        <div class="custom-url-info">\n            <span class="custom-url-name bbq-editable">%s</span>\n            <span class="custom-url-key" style="display: none;">%s</span>\n        </div>\n        <div class="custom-url-actions">\n            <button class="delete" type="button">delete</button>\n        </div>\n    </div>\n    ' % (
                environment.getattr(l_custom_url, 'slug'), 
                environment.getattr(l_custom_url, 'target'), 
                context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_custom_url, 'key'), 'urlsafe'))), 
            )
        l_custom_url = missing
        yield u'\n</div>\n<div id="new-custom-url-dialog" class="pre-modal" style="opacity: 0;">\n    <div class="bbq-dialog-content">\n        <form id="new-custom-url-frm">\n            <p>\n                <label for="new-custom-url-slug-input">Slug:</label>\n                <input id="new-custom-url-slug-input" type="text" name="slug">\n            </p>\n            <p>\n                <label for="new-custom-url-target-input">Target:</label>\n                <select id="new-custom-url-target-input" name="target">\n                    <option value="" selected="selected">CHOOSE A TARGET:</option>\n                    <option disabled="disabled">PROJECTS:</option>\n                    '
        l_project = missing
        l_encrypt = context.resolve('encrypt')
        t_1 = 1
        for l_project in l_projects:
            if 0: yield None
            yield u'\n                    <option value="%s">&nbsp;&nbsp;&nbsp;&nbsp;%s</option>\n                    ' % (
                context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_project, 'key'), 'urlsafe'))), 
                environment.getattr(l_project, 'name'), 
            )
            t_1 = 0
        if t_1:
            if 0: yield None
            yield u'\n                    <option disabled="disabled">...no projects</option>\n                    '
        l_project = missing
        yield u'\n                    <option disabled="disabled">USERS:</option>\n                    '
        l_user = missing
        l_encrypt = context.resolve('encrypt')
        t_2 = 1
        for l_user in l_users:
            if 0: yield None
            yield u'\n                    <option value="%s">&nbsp;&nbsp;&nbsp;&nbsp;%s</option>\n                    ' % (
                context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_user, 'key'), 'urlsafe'))), 
                environment.getattr(l_user, 'username'), 
            )
            t_2 = 0
        if t_2:
            if 0: yield None
            yield u'\n                    <option disabled="disabled">...no users</option>\n                    '
        l_user = missing
        yield u'\n                </select>\n            </p>\n            <p>\n                <button id="save-new-custom-url-btn" class="save-new-dialog" type="button">Yeah, add that!</button>\n                <button id="cancel-new-custom-url-btn" class="cancel-new-dialog" type="button">Never mind.</button>\n            </p>\n        </form>\n    </div>\n</div>'

    blocks = {}
    debug_info = '8=14&11=17&14=18&15=19&35=26&36=29&41=41&42=44'
    return locals()