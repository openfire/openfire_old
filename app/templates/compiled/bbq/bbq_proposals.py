from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/bbq/bbq_proposals.html'

    def root(context, environment=environment):
        l_proposals = context.resolve('proposals')
        l_users = context.resolve('users')
        l_categories = context.resolve('categories')
        if 0: yield None
        yield u'<h2>Proposals!</h2>\n<div id="proposal-container">\n    '
        l_proposal = missing
        t_1 = 1
        for l_proposal in l_proposals:
            if 0: yield None
            yield u'\n    <div class="proposal">\n        <div class="proposal-info">\n            <span class="proposal-key" style="display: none;">%s</span>\n            <label>Name: </label>\n            <span class="proposal-name editable">%s</span>\n            <label>Summary: </label>\n            <span class="proposal-summary editable">%s</span>\n            <label>Category: </label>\n            <span class="proposal-category editable">%s</span>\n            <label>Status: </label>\n            <span class="proposal-status editable">%s</span>\n            <label>Pitch: </label>\n            <span class="proposal-pitch editable">%s</span>\n            <label>Tech: </label>\n            <span class="proposal-tech editable">%s</span>\n            <label>Keywords: </label>\n            <span class="proposal-keywords editable">%s</span>\n            <label>Creator: </label>\n            <span class="proposal-creator editable">%s</span>\n        </div>\n        <div>\n            <button class="delete" type="button">delete</button>\n            <button class="start-edit" type="button">edit</button>\n            <button class="cancel-edit" type="button" style="display: none;">cancel</button>\n            <button class="save-edit" type="button" style="display: none;">save</button>\n            <button class="promote-to-project" type="button">Promote to a project</button>\n            <button class="suspend" type="button">Suspend</button>\n            <button class="reject" type="button">Reject</button>\n        </div>\n    </div>\n    ' % (
                context.call(environment.getattr(environment.getattr(l_proposal, 'key'), 'urlsafe')), 
                environment.getattr(l_proposal, 'name'), 
                environment.getattr(l_proposal, 'summary'), 
                environment.getattr(l_proposal, 'category'), 
                environment.getattr(l_proposal, 'status'), 
                environment.getattr(l_proposal, 'pitch'), 
                environment.getattr(l_proposal, 'tech'), 
                environment.getattr(l_proposal, 'keywords'), 
                environment.getattr(l_proposal, 'creator'), 
            )
            t_1 = 0
        if t_1:
            if 0: yield None
            yield u'\n    <div>No proposals yet!</div>\n    '
        l_proposal = missing
        yield u'\n</div>\n<button id="show-new-proposal-btn" class="show-new-inline">+ Add New Proposal (does not work yet)</button>\n<div id="new-proposal-inline" class="inline-form" style="display: none;">\n    <form id="new-proposal-frm">\n        <p>\n            <label for="new-proposal-name-input">Name:</label>\n            <input type="text" id="new-proposal-name-input" name="name">\n        </p>\n        <p>\n            <label for="new-proposal-url-input">URL Slug:</label>\n            <input type="text" id="new-proposal-url-input" name="url">\n        </p>\n        <p>\n            <label for="new-proposal-summary-input">Summary:</label>\n            <input type="text" id="new-proposal-summary-input" name="summary">\n        </p>\n        <p>\n            <label for="new-proposal-category-input">category:</label>\n            <select id="new-proposal-category-input" name="category">\n                '
        l_category = missing
        t_2 = 1
        for l_category in l_categories:
            if 0: yield None
            yield u'\n                <option value="%s">%s</option>\n                ' % (
                context.call(environment.getattr(environment.getattr(l_category, 'key'), 'urlsafe')), 
                environment.getattr(l_category, 'name'), 
            )
            t_2 = 0
        if t_2:
            if 0: yield None
            yield u'\n                <option value="">Add a category first...</option>\n                '
        l_category = missing
        yield u'\n            </select>\n        </p>\n        <p>\n            <label for="new-proposal-status-input">status:</label>\n            <input type="text" id="new-proposal-status-input" name="status">\n        </p>\n        <p>\n            <label for="new-proposal-pitch-input">pitch:</label>\n            <input type="text" id="new-proposal-pitch-input" name="pitch">\n        </p>\n        <p>\n            <label for="new-proposal-tech-input">tech:</label>\n            <input type="text" id="new-proposal-tech-input" name="tech">\n        </p>\n        <p>\n            <label for="new-proposal-keywords-input">keywords:</label>\n            <input type="text" id="new-proposal-keywords-input" name="keywords">\n        </p>\n        <p>\n            <label for="new-proposal-creator-input">creator:</label>\n            <select id="new-proposal-creator-input" name="category">\n                '
        l_user = missing
        t_3 = 1
        for l_user in l_users:
            if 0: yield None
            yield u'\n                <option value="%s">%s</option>\n                ' % (
                context.call(environment.getattr(environment.getattr(l_user, 'key'), 'urlsafe')), 
                environment.getattr(l_user, 'username'), 
            )
            t_3 = 0
        if t_3:
            if 0: yield None
            yield u'\n                <option value="">Add some users first...</option>\n                '
        l_user = missing
        yield u'\n            </select>\n        </p>\n        <p>\n            <button id="save-new-proposal-btn" class="save-new-inline" type="button">Yeah, add that!</button>\n            <button id="cancel-new-proposal-btn" class="cancel-new-inline" type="button">Never mind.</button>\n        </p>\n    </form>\n</div>'

    blocks = {}
    debug_info = '3=14&6=17&8=18&10=19&12=20&14=21&16=22&18=23&20=24&22=25&56=35&57=38&82=49&83=52'
    return locals()