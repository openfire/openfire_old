from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/bbq/bbq_custom_urls.html'

    def root(context, environment=environment):
        l_custom_urls = context.resolve('custom_urls')
        l_projects = context.resolve('projects')
        l_users = context.resolve('users')
        if 0: yield None
        yield u'<h2>Custom URLs!</h2>\n<div id="custom-url-container">\n    '
        l_custom_url = missing
        for l_custom_url in l_custom_urls:
            if 0: yield None
            yield u'\n    <div class="custom-url">\n        <div class="custom-url-info">\n            <span class="custom-url-key" style="display: none;">%s</span>\n            <label>Slug: </label>\n            <span class="custom-url-slug">%s</span>\n            <label>Target: </label>\n            <span class="custom-url-name">%s</span>\n        </div>\n        <div class="custom-url-actions">\n            <button class="delete" type="button">delete</button>\n        </div>\n    </div>\n    ' % (
                context.call(environment.getattr(environment.getattr(l_custom_url, 'key'), 'urlsafe')), 
                environment.getattr(l_custom_url, 'slug'), 
                environment.getattr(l_custom_url, 'target'), 
            )
        l_custom_url = missing
        yield u'\n</div>\n<button id="show-new-custom-url-btn" class="show-new-inline">+ Add New Custom URL</button>\n<div id="new-custom-url-inline" class="inline-form" style="display: none;">\n    <form id="new-custom-url-frm">\n        <p>\n            <label for="new-custom-url-slug-input">Slug:</label>\n            <input id="new-custom-url-slug-input" type="text" name="slug">\n        </p>\n        <p>\n            <label for="new-custom-url-target-input">Target:</label>\n            <select id="new-custom-url-target-input" name="target">\n                <option value="" selected="selected">CHOOSE A TARGET:</option>\n                <option disabled="disabled">PROJECTS:</option>\n                '
        l_project = missing
        t_1 = 1
        for l_project in l_projects:
            if 0: yield None
            yield u'\n                <option value="%s">&nbsp;&nbsp;&nbsp;&nbsp;%s</option>\n                ' % (
                context.call(environment.getattr(environment.getattr(l_project, 'key'), 'urlsafe')), 
                environment.getattr(l_project, 'name'), 
            )
            t_1 = 0
        if t_1:
            if 0: yield None
            yield u'\n                <option disabled="disabled">...no projects</option>\n                '
        l_project = missing
        yield u'\n                <option disabled="disabled">USERS:</option>\n                '
        l_user = missing
        t_2 = 1
        for l_user in l_users:
            if 0: yield None
            yield u'\n                <option value="%s">&nbsp;&nbsp;&nbsp;&nbsp;%s</option>\n                ' % (
                context.call(environment.getattr(environment.getattr(l_user, 'key'), 'urlsafe')), 
                environment.getattr(l_user, 'username'), 
            )
            t_2 = 0
        if t_2:
            if 0: yield None
            yield u'\n                <option disabled="disabled">...no users</option>\n                '
        l_user = missing
        yield u'\n            </select>\n        </p>\n        <p>\n            <button id="save-new-custom-url-btn" class="save-new-inline" type="button">Yeah, add that!</button>\n            <button id="cancel-new-custom-url-btn" class="cancel-new-inline" type="button">Never mind.</button>\n        </p>\n    </form>\n</div>'

    blocks = {}
    debug_info = '3=13&6=16&8=17&10=18&30=24&31=27&36=38&37=41'
    return locals()