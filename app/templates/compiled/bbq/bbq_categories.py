from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\bbq_categories.html'

    def root(context, environment=environment):
        l_categories = context.resolve('categories')
        if 0: yield None
        yield u'<h2>Categories!</h2>\n<a id="a-new-category-dialog" href="#new-category-dialog">+ Add New Category</a>\n<div id="category-container">\n    <div class="category-header">\n        <div class="bbq-col">Name</div>\n        <div class="bbq-col">Slug</div>\n        <div class="bbq-col">Description</div>\n    </div>\n    '
        l_category = missing
        l_encrypt = context.resolve('encrypt')
        for l_category in l_categories:
            if 0: yield None
            yield u'\n    <div id="category-%s" class="category">\n        <div class="category-info">\n            <span class="category-name bbq-editable">%s</span>\n        </div>\n        <div class="category-info">\n            <span class="category-slug bbq-not-editable">%s</span>\n        </div>\n        <div class="category-info">\n            <span class="category-description bbq-editable">%s</span>\n            <span class="category-key" style="display: none;">%s</span>\n        </div>\n        <div class="category-actions">\n            <button class="delete" type="button">delete</button>\n            <button class="start-edit" type="button">edit</button>\n            <button class="cancel-edit" type="button" style="display: none;">cancel</button>\n            <button class="save-edit" type="button" style="display: none;">save</button>\n        </div>\n    </div>\n    ' % (
                context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_category, 'key'), 'urlsafe'))), 
                environment.getattr(l_category, 'name'), 
                environment.getattr(l_category, 'slug'), 
                environment.getattr(l_category, 'description'), 
                context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_category, 'key'), 'urlsafe'))), 
            )
        l_category = missing
        yield u'\n</div>\n<div id="new-category-dialog" class="pre-modal bbq-dialog" style="opacity: 0;">\n    <form id="new-category-frm">\n        <p>\n            <label for="new-category-name-input">Name:</label>\n            <input type="text" id="new-category-name-input" name="name">\n        </p>\n        <p>\n            <label for="new-category-url-input">URL Slug:</label>\n            <input type="text" id="new-category-url-input" name="url">\n        </p>\n        <p>\n            <label for="new-category-description-input">Description:</label>\n            <input type="text" id="new-category-description-input" name="description">\n        </p>\n        <p>\n            <button id="save-new-category-btn" class="save-new-dialog" type="button">Yeah, add that!</button>\n            <button id="cancel-new-category-btn" class="cancel-new-dialog" type="button">Never mind.</button>\n        </p>\n    </form>\n</div>'

    blocks = {}
    debug_info = '9=12&10=15&12=16&15=17&18=18&19=19'
    return locals()