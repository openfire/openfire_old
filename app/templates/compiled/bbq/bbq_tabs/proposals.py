from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\bbq_tabs\\proposals.html'

    def root(context, environment=environment):
        l_proposals = context.resolve('proposals')
        l_users = context.resolve('users')
        l_categories = context.resolve('categories')
        if 0: yield None
        yield u'<h2>Proposals!</h2>\n<a id="a-new-proposal-dialog" href="#new-proposal-dialog">+ Add New Proposal</a>\n<div class="content">\n    <table id="bbq-proposal-table" class="bbq-datatable">\n        <thead>\n            <tr>\n                <th>Name</th>\n                <th>Status</th>\n                <th>Summary</th>\n                <th>Owners</th>\n                <th>Category</th>\n            </tr>\n        </thead>\n        <tbody>\n            '
        l_proposal = missing
        for l_proposal in l_proposals:
            if 0: yield None
            yield u'\n            <tr>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>\n                    ' % (
                environment.getattr(l_proposal, 'name'), 
                environment.getattr(l_proposal, 'status'), 
                environment.getattr(l_proposal, 'summary'), 
            )
            l_owner = missing
            for l_owner in environment.getattr(l_proposal, 'owners'):
                if 0: yield None
                yield u'\n                        %s, &nbsp;\n                    ' % (
                    context.call(environment.getattr(l_owner, 'id')), 
                )
            l_owner = missing
            yield u'\n                </td>\n                <td>%s</td>\n            </tr>\n            ' % (
                context.call(environment.getattr(environment.getattr(l_proposal, 'category'), 'id')), 
            )
        l_proposal = missing
        yield u'\n        </tbody>\n    </table>\n</div>\n<div id="new-proposal-dialog" class="pre-modal" style="opacity: 0;">\n    <div class="bbq-dialog-content">\n        <form id="new-proposal-frm">\n            <p>\n                <label for="new-proposal-name-input">Name:</label>\n                <input type="text" id="new-proposal-name-input" name="name">\n            </p>\n            <p>\n                <label for="new-proposal-url-input">URL Slug:</label>\n                <input type="text" id="new-proposal-url-input" name="url">\n            </p>\n            <p>\n                <label for="new-proposal-summary-input">Summary:</label>\n                <input type="text" id="new-proposal-summary-input" name="summary">\n            </p>\n            <p>\n                <label for="new-proposal-category-input">category:</label>\n                <select id="new-proposal-category-input" name="category">\n                    '
        l_category = missing
        t_1 = 1
        for l_category in l_categories:
            if 0: yield None
            yield u'\n                    <option value="%s">%s</option>\n                    ' % (
                context.call(environment.getattr(environment.getattr(l_category, 'key'), 'urlsafe')), 
                environment.getattr(l_category, 'name'), 
            )
            t_1 = 0
        if t_1:
            if 0: yield None
            yield u'\n                    <option value="">Add a category first...</option>\n                    '
        l_category = missing
        yield u'\n                </select>\n            </p>\n            <p>\n                <label for="new-proposal-status-input">status:</label>\n                <input type="text" id="new-proposal-status-input" name="status">\n            </p>\n            <p>\n                <label for="new-proposal-pitch-input">pitch:</label>\n                <input type="text" id="new-proposal-pitch-input" name="pitch">\n            </p>\n            <p>\n                <label for="new-proposal-tech-input">tech:</label>\n                <input type="text" id="new-proposal-tech-input" name="tech">\n            </p>\n            <p>\n                <label for="new-proposal-keywords-input">keywords:</label>\n                <input type="text" id="new-proposal-keywords-input" name="keywords">\n            </p>\n            <p>\n                <label for="new-proposal-creator-input">creator:</label>\n                <select id="new-proposal-creator-input" name="category">\n                    '
        l_user = missing
        t_2 = 1
        for l_user in l_users:
            if 0: yield None
            yield u'\n                    <option value="%s">%s</option>\n                    ' % (
                context.call(environment.getattr(environment.getattr(l_user, 'key'), 'urlsafe')), 
                environment.getattr(l_user, 'username'), 
            )
            t_2 = 0
        if t_2:
            if 0: yield None
            yield u'\n                    <option value="">Add some users first...</option>\n                    '
        l_user = missing
        yield u'\n                </select>\n            </p>\n            <p>\n                <button id="save-new-proposal-btn" class="save-new-dialog" type="button">Yeah, add that!</button>\n                <button id="cancel-new-proposal-btn" class="cancel-new-dialog" type="button">Never mind.</button>\n            </p>\n        </form>\n    </div>\n</div>'

    blocks = {}
    debug_info = '15=13&17=16&18=17&19=18&21=21&22=24&25=28&49=34&50=37&75=48&76=51'
    return locals()