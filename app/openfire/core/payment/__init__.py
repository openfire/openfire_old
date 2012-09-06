from google.appengine.ext import ndb
from openfire.core.payment.wepay import WePayAPI
from openfire.models.payment import Payment, ProjectAccount, WePayProjectAccount

class CorePaymentAPI(object):

    ''' A core API for payments. '''

    def _calculate_commission(self, amount):

        ''' Calculate how much commission openfire should take from a particular pledge. '''

        # TODO: Calculate our commission. For now just take $1.
        return 1

    def _calculate_project_progress(self, project):

        ''' Calculate the progress percentage for a project. '''

        # TODO: How to do this? We currently use the highest goal.
        return int(project.money / project.goals[-1].get().amount * 100)

    def _add_payment_to_project(self, project, payment):

        ''' Adds a payment to a project and updates progress. This will tip the project if appropriate. '''

        # Link the payment and update the backer count.
        project.payments.append(payment.key)
        project.backers = project.backers + 1

        # Calculate the new money total and progress.
        project.money = project.money + payment.amount
        project.progress = self._calculate_project_progress(project)
        project.put()

        # If the current goal was just met, tip it.
        # TODO: How to do this? We currently use the highest goal.
        goal = project.goals[-1].get()
        if not goal.met and project.money >= goal.amount:
            self._tip_project_goal(project, goal)

    def _remove_payment_from_project(self, project, payment):

        ''' Removes a payment from a project and subtract the amount. '''

        # Remove the payment from the project's list.
        project = payment.to_project.get()
        if payment.key in project.payments:
            project.payments.remove(payment.key)
        project.backers = project.backers - 1

        # Calculate the new money total and progress.
        project.money = project.money - payment.amount
        project.progress = self._calculate_project_progress(project)
        project.put()

    def _tip_project_goal(self, project, goal):

        ''' Tips a project goal, setting it to 'met' and charging all the payments. '''

        # TODO: For now, since we just use the top goal, set all the goals as met and charge all payments!
        goals = ndb.get_multi(project.goals)
        for goal in goals:
            goal.met = True
            goal.progress = 100
            goal.put()

        payments = ndb.get_multi(project.payments)
        charged = self.charge_payments(payments)
        # TODO: Use charged here? It is an array of transactions for each payment.
        return True

    def generate_auth_url(self, user):

        ''' Generate and return an auth url for openfire. '''

        return WePayAPI.generate_oauth_url(user)

    def create_user_payment_account(self, user, *args):

        ''' Links an already created 3rd party account to an openfire user. '''

        return WePayAPI.create_account_for_user(user, *args)

    def create_project_payment_account(self, project_key, name, description, wepay_account):

        ''' Create a sub account for a user to use to collect payments for a project. '''

        wepay_account_id = WePayAPI.create_payment_account(name, description, wepay_account.wepay_user_id)
        account_key = ndb.Key(WePayProjectAccount, project_key.urlsafe())
        new_account = WePayProjectAccount(key=account_key, project=project_key, payment_account=wepay_account.key,
                name=name, description=description, wepay_account_id=wepay_account_id)
        new_account.put()
        return new_account

    def account_for_project(self, project):

        ''' Return the payment account for the given project key, or none. '''

        account_key = ndb.Key(WePayProjectAccount, project.key.urlsafe())
        return account_key.get()

    def update_account_balance(self, account):

        ''' Update the balance for a project account. '''

        return WePayAPI.update_account_balance(account)

    def save_user_cc(self, user, cc_info):

        ''' Adds a credit card money source to a user. '''

        return WePayAPI.save_cc_for_user(user, cc_info)

    def back_project(self, project, tier_key, amount, money_source):

        ''' Create a payment that records the contribution amount that will be charged if the project ignites. '''

        description = 'Contribution to %s' % project.name
        payment = Payment(
            amount=amount,
            commission=self._calculate_commission(amount),
            description=description,
            status='p',
            from_user=money_source.owner,
            from_money_source=money_source.key,
            to_project=project.key,
            to_account=self.account_for_project(project).key,
        )
        payment.put()

        # Link the payment to the project and update progress.
        self._add_payment_to_project(project, payment)

        # If the goal has already been met, charge the payment right now.
        if project.goals[-1].get().met:
            success = self.charge_payments([payment])
            # TODO: Use success here.

        return payment

    def charge_payments(self, payments):

        '''
        Charge many payments at once when a project goal is completed.
        Returns a list of transactions.
        '''

        return [WePayAPI.execute_payment(p) for p in payments]

    def cancel_payment(self, payment, reason):

        ''' Cancel a single payment. '''

        if payment.current_transaction:
            transaction = payment.current_transaction.get()
            if not transaction:
                return False
            canceled = WePayAPI.cancel_payment(transaction, reason)
            if not canceled:
                return False

        payment.status = 'c'
        payment.put()

        # Un-link the payment from the project and update progress.
        self._remove_payment_from_project(payment.to_project.get(), payment)

        return True

    def refund_payment(self, payment, reason, amount=None):

        ''' Refund a single payment. '''

        if not payment.current_transaction:
            return False
        transaction = payment.current_transaction.get()
        if not transaction:
            return False
        return WePayAPI.refund_payment(transaction, reason, amount)

    def payment_updated(self, payment_id):

        ''' A payment was updated through an IPN. '''

        return WePayAPI.checkout_updated(payment_id)

    def withdrawal_updated(self, withdrawal_id):

        ''' A withdrawal was updated through an IPN. '''

        return WePayAPI.withdrawal_updated(withdrawal_id)

    def generate_withdrawal_url(self, user, account, amount, note):

        ''' Generate a url where a user can withdraw money from a project payment account. '''

        withdrawal = WePayAPI.generate_withdrawal(user, account, amount, note)
        if not withdrawal:
            return None
        return withdrawal.wepay_withdrawal_uri


# Payment API singleton.
PaymentAPI = CorePaymentAPI()
