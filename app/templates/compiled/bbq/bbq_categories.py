from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\bbq_categories.html'

    def root(context, environment=environment):
        l_categories = context.resolve('categories')
        if 0: yield None
        yield u'<h2>Categories!</h2>\n<ul>\n    '
        l_category = missing
        t_1 = 1
        for l_category in l_categories:
            if 0: yield None
            yield u'\n    <li id="category-%s">\n        <p id="category-display-%s">\n            <span>%s</span>\n            <span>%s</span>\n            <span>%s</span>\n        </p>\n        <p id="category-inputs-%s" style="display: none;">\n            <span><input class="name-input" value="%s"></span>\n            <span><input class="slug-input" value="%s" disabled="disabled"></span>\n            <span><input class="description-input" value="%s"></span>\n        </p>\n        <span>\n            <button id="delete-category-%s" class="delete-category-btn" type="button">delete</button>\n            <button id="start-edit-category-%s" class="start-edit-category-btn" type="button">edit</button>\n            <button id="cancel-edit-category-%s" class="cancel-edit-category-btn" type="button" style="display: none;">cancel</button>\n            <button id="save-edit-category-%s" class="save-edit-category-btn" type="button" style="display: none;">save</button>\n        </span>\n    </li>\n    ' % (
                environment.getattr(l_category, 'slug'), 
                environment.getattr(l_category, 'slug'), 
                environment.getattr(l_category, 'name'), 
                environment.getattr(l_category, 'slug'), 
                environment.getattr(l_category, 'description'), 
                environment.getattr(l_category, 'slug'), 
                environment.getattr(l_category, 'name'), 
                environment.getattr(l_category, 'slug'), 
                environment.getattr(l_category, 'description'), 
                environment.getattr(l_category, 'slug'), 
                environment.getattr(l_category, 'slug'), 
                environment.getattr(l_category, 'slug'), 
                environment.getattr(l_category, 'slug'), 
            )
            t_1 = 0
        if t_1:
            if 0: yield None
            yield u'\n    <li>No categories yet!</li>\n    '
        l_category = missing
        yield u'\n</ul>\n<button id="show-new-category-btn">+ Add New Category</button>\n<div id="new-category-inline" style="display: none;">\n    <form id="new-category-frm">\n        <p>\n            <label for="new-category-name-input">Name:</label>\n            <input type="text" id="new-category-name-input" name="name">\n        </p>\n        <p>\n            <label for="new-category-url-input">URL Slug:</label>\n            <input type="text" id="new-category-url-input" name="url">\n        </p>\n        <p>\n            <label for="new-category-description-input">Description:</label>\n            <input type="text" id="new-category-description-input" name="description">\n        </p>\n        <p>\n            <button id="save-new-category-btn" type="button">Yeah, add that!</button>\n            <button id="cancel-new-category-btn" type="button">Never mind.</button>\n        </p>\n    </form>\n</div>'

    blocks = {}
    debug_info = '3=12&4=15&5=16&6=17&7=18&8=19&10=20&11=21&12=22&13=23&16=24&17=25&18=26&19=27'
    return locals()