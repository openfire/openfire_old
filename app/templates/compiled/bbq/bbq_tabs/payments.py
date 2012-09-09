from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\bbq_tabs\\payments.html'

    def root(context, environment=environment):
        l_payments = context.resolve('payments')
        l_checkouts = context.resolve('checkouts')
        l_withdrawals = context.resolve('withdrawals')
        if 0: yield None
        yield u'<h2>openfire payments</h2>\n<div class="content">\n    <table id="bbq-payment-table" class="bbq-datatable">\n        <thead>\n            <tr>\n                <th>From User</th>\n                <th>To Project</th>\n                <th>Project Goal</th>\n                <th>Project Tier</th>\n                <th>Amount</th>\n                <th>Commission</th>\n                <th>Status</th>\n                <th>Current Transaction</th>\n                <th>All Transactions</th>\n                <th>From Money Source</th>\n                <th>To Account</th>\n                <th>Created</th>\n                <th>Updated</th>\n                <th>Archived</th>\n            </tr>\n        </thead>\n        <tbody>\n            '
        l_payment = missing
        for l_payment in l_payments:
            if 0: yield None
            yield u'\n            <tr>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>\n                    ' % (
                environment.getattr(l_payment, 'from_user'), 
                environment.getattr(context.call(environment.getattr(environment.getattr(l_payment, 'to_project'), 'get')), 'name'), 
                environment.getattr(l_payment, 'to_project_goal'), 
                environment.getattr(l_payment, 'to_project_tier'), 
                environment.getattr(l_payment, 'amount'), 
                environment.getattr(l_payment, 'commission'), 
                environment.getattr(l_payment, 'status'), 
                environment.getattr(l_payment, 'current_transaction'), 
            )
            l_transaction = missing
            t_1 = 1
            for l_transaction in environment.getattr(l_payment, 'all_transactions'):
                if 0: yield None
                yield u'\n                        %s,&nbsp;\n                    ' % (
                    l_transaction, 
                )
                t_1 = 0
            if t_1:
                if 0: yield None
                yield u'\n                        No transactions.\n                    '
            l_transaction = missing
            yield u'\n                </td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n            </tr>\n            ' % (
                environment.getattr(l_payment, 'from_money_source'), 
                environment.getattr(l_payment, 'to_account'), 
                environment.getattr(l_payment, 'created'), 
                environment.getattr(l_payment, 'updated'), 
                environment.getattr(l_payment, 'archived'), 
            )
        l_payment = missing
        yield u'\n        </tbody>\n    </table>\n</div>\n\n<h2>openfire payment checkout transactions</h2>\n<div class="content">\n    <table id="bbq-checkout-transaction-table" class="bbq-datatable">\n        <thead>\n            <tr>\n                <th>Action</th>\n                <th>Status</th>\n                <th>Created</th>\n                <th>Updated</th>\n                <th>Payment</th>\n                <th>WePay Checkout ID</th>\n                <th>WePay Checkout URI</th>\n                <th>WePay Checkout Status</th>\n                <th>Good or Service</th>\n            </tr>\n        </thead>\n        <tbody>\n            '
        l_checkout = missing
        for l_checkout in l_checkouts:
            if 0: yield None
            yield u'\n            <tr>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n            </tr>\n            ' % (
                environment.getattr(l_checkout, 'action'), 
                environment.getattr(l_checkout, 'status'), 
                environment.getattr(l_checkout, 'created'), 
                environment.getattr(l_checkout, 'updated'), 
                environment.getattr(l_checkout, 'payment'), 
                environment.getattr(l_checkout, 'wepay_checkout_id'), 
                environment.getattr(l_checkout, 'wepay_checkout_uri'), 
                environment.getattr(l_checkout, 'wepay_checkout_status'), 
                environment.getattr(l_checkout, 'good_or_service'), 
            )
        l_checkout = missing
        yield u'\n        </tbody>\n    </table>\n</div>\n\n<h2>openfire payment withdrawal transactions</h2>\n<div class="content">\n    <table id="bbq-withdrawal-transaction-table" class="bbq-datatable">\n        <thead>\n            <tr>\n                <th>Action</th>\n                <th>Status</th>\n                <th>Created</th>\n                <th>Updated</th>\n                <th>Account</th>\n                <th>User</th>\n                <th>WePay Withdrawal ID</th>\n                <th>WePay Withdrawal URI</th>\n                <th>WePay Withdrawal Status</th>\n            </tr>\n        </thead>\n        <tbody>\n            '
        l_withdrawal = missing
        for l_withdrawal in l_withdrawals:
            if 0: yield None
            yield u'\n            <tr>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n            </tr>\n            ' % (
                environment.getattr(l_withdrawal, 'action'), 
                environment.getattr(l_withdrawal, 'status'), 
                environment.getattr(l_withdrawal, 'created'), 
                environment.getattr(l_withdrawal, 'updated'), 
                environment.getattr(l_withdrawal, 'account'), 
                environment.getattr(l_withdrawal, 'user'), 
                environment.getattr(l_withdrawal, 'wepay_withdrawal_id'), 
                environment.getattr(l_withdrawal, 'wepay_withdrawal_uri'), 
                environment.getattr(l_withdrawal, 'wepay_withdrawal_status'), 
            )
        l_withdrawal = missing
        yield u'\n        </tbody>\n    </table>\n</div>'

    blocks = {}
    debug_info = '23=13&25=16&26=17&27=18&28=19&29=20&30=21&31=22&32=23&34=27&35=30&40=38&41=39&42=40&43=41&44=42&68=47&70=50&71=51&72=52&73=53&74=54&75=55&76=56&77=57&78=58&102=63&104=66&105=67&106=68&107=69&108=70&109=71&110=72&111=73&112=74'
    return locals()