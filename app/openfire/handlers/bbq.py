# -*- coding: utf-8 -*-
from openfire.handlers import WebHandler
from openfire.models.project import Category, Proposal, Project
from openfire.models.user import User, Topic
from openfire.models.assets import CustomURL
from openfire.models.payment import (WePayUserPaymentAccount, WePayProjectAccount, Payment,
        WePayCheckoutTransaction, WePayWithdrawalTransaction, WePayCreditCard)


class Moderate(WebHandler):

    ''' openfire bbq (moderation) page. '''

    def get(self):

        ''' Render moderate.html. '''

        context = {
            'categories': Category.query().fetch(),
            'proposals': Proposal.query().fetch(),
            'projects': Project.query().fetch(),
            'users': User.query().fetch(),
            'custom_urls': CustomURL.query().fetch(),
            'topics': Topic.query().fetch(),

            # Payments.
            'wepay_accounts': WePayUserPaymentAccount.query().fetch(),
            'project_accounts': WePayProjectAccount.query().fetch(),
            'payments': Payment.query().fetch(),
            'checkouts': WePayCheckoutTransaction.query().fetch(),
            'withdrawals': WePayWithdrawalTransaction.query().fetch(),
            'credit_cards': WePayCreditCard.query().fetch(),
        }
        return self.render('bbq/moderate.html', **context)
