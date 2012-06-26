from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/bbq/bbq_proposals.html'

    def root(context, environment=environment):
        l_proposals = context.resolve('proposals')
        l_categories = context.resolve('categories')
        if 0: yield None
        yield u'<h2>Proposals (...does not work yet)!</h2>\n<ul>\n    '
        l_proposal = missing
        t_1 = 1
        for l_proposal in l_proposals:
            if 0: yield None
            yield u'\n    <li id="proposal-%s">\n        <p id="proposal-display-%s">\n            <span>%s</span>\n            <span>%s</span>\n            <span>%s</span>\n        </p>\n        <p id="proposal-inputs-%s" style="display: none;">\n            <span><input class="name-input" value="%s"></span>\n            <span><input class="slug-input" value="%s" disabled="disabled"></span>\n            <span><input class="summary-input" value="%s"></span>\n        </p>\n        <span>\n            <button id="delete-proposal-%s" class="delete-object" type="button">delete</button>\n            <button id="start-edit-proposal-%s" class="start-edit-inline" type="button">edit</button>\n            <button id="cancel-edit-proposal-%s" class="cancel-edit-inline" type="button" style="display: none;">cancel</button>\n            <button id="save-edit-proposal-%s" class="save-edit-inline" type="button" style="display: none;">save</button>\n        </span>\n    </li>\n    ' % (
                environment.getattr(l_proposal, 'slug'), 
                environment.getattr(l_proposal, 'slug'), 
                environment.getattr(l_proposal, 'name'), 
                environment.getattr(l_proposal, 'slug'), 
                environment.getattr(l_proposal, 'summary'), 
                environment.getattr(l_proposal, 'slug'), 
                environment.getattr(l_proposal, 'name'), 
                environment.getattr(l_proposal, 'slug'), 
                environment.getattr(l_proposal, 'summary'), 
                environment.getattr(l_proposal, 'slug'), 
                environment.getattr(l_proposal, 'slug'), 
                environment.getattr(l_proposal, 'slug'), 
                environment.getattr(l_proposal, 'slug'), 
            )
            t_1 = 0
        if t_1:
            if 0: yield None
            yield u'\n    <li>No proposals yet!</li>\n    '
        l_proposal = missing
        yield u'\n</ul>\n<button id="show-new-proposal-btn" class="show-new-inline">+ Add New Proposal (does not work yet)</button>\n<div id="new-proposal-inline" class="inline-form" style="display: none;">\n    <form id="new-proposal-frm">\n        <p>\n            <label for="new-proposal-name-input">Name:</label>\n            <input type="text" id="new-proposal-name-input" name="name">\n        </p>\n        <p>\n            <label for="new-proposal-url-input">URL Slug:</label>\n            <input type="text" id="new-proposal-url-input" name="url">\n        </p>\n        <p>\n            <label for="new-proposal-summary-input">Summary:</label>\n            <input type="text" id="new-proposal-summary-input" name="summary">\n        </p>\n        <p>\n            <label for="new-proposal-category-input">category:</label>\n            <select id="new-proposal-category-input" name="category">\n                '
        l_category = missing
        t_2 = 1
        for l_category in l_categories:
            if 0: yield None
            yield u'\n                <option value="%s">%s</option>\n                ' % (
                environment.getattr(l_category, 'key'), 
                environment.getattr(l_category, 'name'), 
            )
            t_2 = 0
        if t_2:
            if 0: yield None
            yield u'\n                <option value="">Add a category first...</option>\n                '
        l_category = missing
        yield u'\n            </select>\n        </p>\n        <p>\n            <label for="new-proposal-status-input">status:</label>\n            <input type="text" id="new-proposal-status-input" name="status">\n        </p>\n        <p>\n            <label for="new-proposal-pitch-input">pitch:</label>\n            <input type="text" id="new-proposal-pitch-input" name="pitch">\n        </p>\n        <p>\n            <label for="new-proposal-tech-input">tech:</label>\n            <input type="text" id="new-proposal-tech-input" name="tech">\n        </p>\n        <p>\n            <label for="new-proposal-keywords-input">keywords:</label>\n            <input type="text" id="new-proposal-keywords-input" name="keywords">\n        </p>\n        <p>\n            <label for="new-proposal-creator-input">creator:</label>\n            <input type="text" id="new-proposal-creator-input" name="creator">\n        </p>\n        <p>\n            <button id="save-new-proposal-btn" class="save-new-inline" type="button">Yeah, add that!</button>\n            <button id="cancel-new-proposal-btn" class="cancel-new-inline" type="button">Never mind.</button>\n        </p>\n    </form>\n</div>'

    blocks = {}
    debug_info = '3=13&4=16&5=17&6=18&7=19&8=20&10=21&11=22&12=23&13=24&16=25&17=26&18=27&19=28&44=38&45=41'
    return locals()