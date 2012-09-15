from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\bbq_tabs\\categories.html'

    def root(context, environment=environment):
        l_categories = context.resolve('categories')
        if 0: yield None
        yield u'<h2>openfire categories</h2>\n<a id="a-new-category-dialog" href="#new-category-dialog">+ Add New Category</a>\n<div class="content">\n    <table id="bbq-category-table" class="bbq-datatable">\n        <thead>\n            <tr>\n                <th>Name</th>\n                <th>Slug</th>\n                <th>Description</th>\n            </tr>\n        </thead>\n        <tbody>\n            '
        l_category = missing
        for l_category in l_categories:
            if 0: yield None
            yield u'\n            <tr>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n            </tr>\n            ' % (
                environment.getattr(l_category, 'name'), 
                environment.getattr(l_category, 'slug'), 
                environment.getattr(l_category, 'description'), 
            )
        l_category = missing
        yield u'\n        </tbody>\n    </table>\n</div>\n\n<div id="new-category-dialog" class="pre-modal bbq-dialog" style="opacity: 0;">\n    <form id="new-category-frm">\n        <p>\n            <label for="new-category-name-input">Name:</label>\n            <input type="text" id="new-category-name-input" name="name">\n        </p>\n        <p>\n            <label for="new-category-url-input">URL Slug:</label>\n            <input type="text" id="new-category-url-input" name="url">\n        </p>\n        <p>\n            <label for="new-category-description-input">Description:</label>\n            <input type="text" id="new-category-description-input" name="description">\n        </p>\n        <p>\n            <button id="save-new-category-btn" class="save-new-dialog" type="button">Yeah, add that!</button>\n            <button id="cancel-new-category-btn" class="cancel-new-dialog" type="button">Never mind.</button>\n        </p>\n    </form>\n</div>'

    blocks = {}
    debug_info = '13=11&15=14&16=15&17=16'
    return locals()