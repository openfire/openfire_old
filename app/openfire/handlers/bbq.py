# -*- coding: utf-8 -*-
from openfire.handlers import WebHandler
from openfire.models.project import Category, Proposal, Project, Goal
from openfire.models.user import User, Topic
from openfire.models.assets import CustomURL
from openfire.models.payment import (WePayUserPaymentAccount, WePayProjectAccount, Payment,
        WePayCheckoutTransaction, WePayWithdrawalTransaction, WePayCreditCard)


class Moderate(WebHandler):

    ''' openfire bbq (moderation) page. '''

    def get(self):

        ''' Render moderate.html. '''

        # Queries used to set up the bbq context.
        proposal_query = Proposal.query()
        project_query = Project.query()
        goal_query = Goal.query()

        context = {
            'categories': Category.query().fetch(),
            'proposals': proposal_query.fetch(),
            'projects': project_query.fetch(),
            'goals': goal_query.fetch(),
            'featured_projects': project_query.filter(Project.status == 'f').fetch(),
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

            # Objects that need admin attention.
            'awaiting_action': {
                'proposals': proposal_query.filter(Proposal.status == 's').fetch(),
                'goals': goal_query.filter(Proposal.status == 's').fetch(),
            },
        }

        context['awaiting_action_count'] = 0
        for obj_type in context['awaiting_action'].keys():
            context['awaiting_action_count'] += len(context['awaiting_action'][obj_type])

        return self.render('bbq/moderate.html', **context)
