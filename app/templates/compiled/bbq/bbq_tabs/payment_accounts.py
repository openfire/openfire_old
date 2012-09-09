from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\bbq_tabs\\payment_accounts.html'

    def root(context, environment=environment):
        l_credit_cards = context.resolve('credit_cards')
        l_project_accounts = context.resolve('project_accounts')
        l_wepay_accounts = context.resolve('wepay_accounts')
        if 0: yield None
        yield u'\n<h2>User WePay Accounts</h2>\n<div class="content">\n    <table id="bbq-user-payment-account-table" class="bbq-datatable">\n        <thead>\n            <tr>\n                <th>User Key</th>\n                <th>WePay User ID</th>\n            </tr>\n        </thead>\n        <tbody>\n            '
        l_account = missing
        for l_account in l_wepay_accounts:
            if 0: yield None
            yield u'\n            <tr>\n                <td>%s</td>\n                <td>%s</td>\n            </tr>\n            ' % (
                environment.getattr(l_account, 'user'), 
                environment.getattr(l_account, 'wepay_user_id'), 
            )
        l_account = missing
        yield u'\n        </tbody>\n    </table>\n</div>\n\n<br />\n<br />\n\n<h2>Project Payment Accounts</h2>\n<div class="content">\n    <table id="bbq-project-payment-account-table" class="bbq-datatable">\n        <thead>\n            <tr>\n                <th>User Payment Account</th>\n                <th>Project</th>\n                <th>Name</th>\n                <th>Description</th>\n                <th>Balance</th>\n                <th>Current Transactions</th>\n                <th>All Transactions</th>\n                <th>WePay Account ID</th>\n            </tr>\n        </thead>\n        <tbody>\n            '
        l_account = missing
        for l_account in l_project_accounts:
            if 0: yield None
            yield u'\n            <tr>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>\n                    ' % (
                environment.getattr(l_account, 'payment_account'), 
                environment.getattr(l_account, 'project'), 
                environment.getattr(l_account, 'name'), 
                environment.getattr(l_account, 'description'), 
                environment.getattr(l_account, 'balance'), 
            )
            l_transaction = missing
            t_1 = 1
            for l_transaction in environment.getattr(l_account, 'current_transactions'):
                if 0: yield None
                yield u'\n                        %s,&nbsp;\n                    ' % (
                    l_transaction, 
                )
                t_1 = 0
            if t_1:
                if 0: yield None
                yield u'\n                        No current transactions.\n                    '
            l_transaction = missing
            yield u'\n                </td>\n                <td>\n                    '
            l_transaction = missing
            t_2 = 1
            for l_transaction in environment.getattr(l_account, 'all_transactions'):
                if 0: yield None
                yield u'\n                        %s,&nbsp;\n                    ' % (
                    l_transaction, 
                )
                t_2 = 0
            if t_2:
                if 0: yield None
                yield u'\n                        No transactions.\n                    '
            l_transaction = missing
            yield u'\n                </td>\n                <td>%s</td>\n            </tr>\n            ' % (
                environment.getattr(l_account, 'wepay_account_id'), 
            )
        l_account = missing
        yield u'\n        </tbody>\n    </table>\n</div>\n\n\n<h2>openfire saved credit card accounts</h2>\n<div class="content">\n    <table id="bbq-cc-account-table" class="bbq-datatable">\n        <thead>\n            <tr>\n                <th>Owner</th>\n                <th>Description</th>\n                <th>ID</th>\n                <th>Save for Re-Use</th>\n                <th>Created</th>\n                <th>First Use</th>\n                <th>Last Use</th>\n                <th>Authorized</th>\n                <th>State</th>\n            </tr>\n        </thead>\n        <tbody>\n            '
        l_credit_card = missing
        for l_credit_card in l_credit_cards:
            if 0: yield None
            yield u'\n            <tr>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n            </tr>\n            ' % (
                environment.getattr(l_credit_card, 'owner'), 
                environment.getattr(l_credit_card, 'description'), 
                environment.getattr(l_credit_card, 'wepay_cc_id'), 
                environment.getattr(l_credit_card, 'save_for_reuse'), 
                environment.getattr(l_credit_card, 'created'), 
                environment.getattr(l_credit_card, 'first_use'), 
                environment.getattr(l_credit_card, 'last_use'), 
                environment.getattr(l_credit_card, 'wepay_cc_authorized'), 
                environment.getattr(l_credit_card, 'wepay_cc_state'), 
            )
        l_credit_card = missing
        yield u'\n        </tbody>\n    </table>\n</div>'

    blocks = {}
    debug_info = '12=13&14=16&15=17&41=22&43=25&44=26&45=27&46=28&47=29&49=33&50=36&56=46&57=49&62=57&87=62&89=65&90=66&91=67&92=68&93=69&94=70&95=71&96=72&97=73'
    return locals()