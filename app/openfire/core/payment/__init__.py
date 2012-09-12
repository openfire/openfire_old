from google.appengine.ext import ndb
from openfire.core.payment.wepay import WePayAPI
from openfire.core.payment.common import CorePaymentResponse, OFPaymentError, OFPaymentFees
from openfire.models.payment import Payment, WePayProjectAccount, WePayUserPaymentAccount

class CorePaymentAPI(object):

    ''' A core API for payments. '''

    def _calculate_commission(self, amount):

        ''' Calculate how much commission openfire should take from a particular pledge. '''

        # The total cut from the payment never goes below the TOTAL_CUT.
        commission = (amount * OFPaymentFees['WEPAY_PERCENT']) + .3
        total_cut = amount * OFPaymentFees['TOTAL_CUT']
        if commission > total_cut:
            # The commission is already above 4.75%, so don't take any more for right now.
            return 0.0
        return total_cut - commission

    def _calculate_goal_progress(self, goal):

        ''' Calculate the progress percentage for a goal. '''

        return int(goal.amount_pledged / goal.amount * 100)

    def _calculate_project_progress(self, project):

        ''' Calculate the progress percentage for a project. '''

        if not project.active_goal:
            return 0
        return self._calculate_goal_progress(project.active_goal.get())

    def _add_payment_to_project(self, project, payment):

        ''' Adds a payment to a project and updates progress. This will tip the project if appropriate. '''

        response = CorePaymentResponse()

        # Link the payment and update the backer count.
        project.payments.append(payment.key)
        project.backers = project.backers + 1

        # Calculate the new money total and progress for goal first, then the project.
        goal = project.active_goal.get()
        goal.amount_pledged = goal.amount_pledged + payment.amount
        goal.progress = self._calculate_goal_progress(goal)
        if goal.met:
            goal.extra_payments.append(payment.key)
        else:
            goal.igniting_payments.append(payment.key)
        goal.put()

        project.money = project.money + payment.amount
        project.progress = self._calculate_project_progress(project)
        project.put()

        if goal.met:
            # If the goal has already been met, charge the payment right now.
            charge_response = self.charge_payments([payment])
            if charge_response[0].success:
                response.response = charge_response[0].response
                response.success = True
            else:
                response.error_code = OFPaymentError.OF_FAILED_IMMEDIATE_CHARGE
                response.error_message = 'Payment recorded but failed to charge the payment.'

        else:
            # If the active goal was just met, tip the goal.
            response.success = True
            if project.money >= goal.amount:
                self._tip_project_goal(project, goal)

        return response

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

        if project.active_goal:
            # If there is an active goal, remove from that as well.
            goal = project.active_goal.get()
            goal.amount_pledged = goal.amount_pledged - payment.amount
            goal.progress = self._calculate_goal_progress(goal)
            goal.put()

    def _tip_project_goal(self, project, goal):

        ''' Tips a project goal, setting it to 'met' and charging all the payments. '''

        goal.met = True
        goal.progress = 100
        goal.put()

        payments = ndb.get_multi(goal.igniting_payments)
        responses = self.charge_payments(payments)
        # TODO: Use charged here? It is an array of responses with transactions for each payment.
        #       Should probably use it to log errors.
        return True

    def generate_auth_url(self, user):

        ''' Generate and return an auth url for openfire. '''

        return WePayAPI.generate_oauth_url(user)

    def create_user_payment_account(self, user, *args):

        ''' Links an already created 3rd party account to an openfire user. '''

        return WePayAPI.create_account_for_user(user, *args)

    def create_project_payment_account(self, project_key, name, description, wepay_account):

        ''' Create a sub account for a user to use to collect payments for a project. '''

        response = WePayAPI.create_payment_account(name, description, wepay_account.wepay_user_id)
        if response.success:
            wepay_account_id = response.response
            account_key = ndb.Key(WePayProjectAccount, project_key.urlsafe())
            new_account = WePayProjectAccount(key=account_key, project=project_key, payment_account=wepay_account.key,
                    name=name, description=description, wepay_account_id=wepay_account_id)
            new_account.put()
            response.response = new_account
        return response

    def set_up_project_payment_account(self, project):

        '''
        Set up the sub account for a user to use to collect payments for a project.
        If the creator or any of the owners has a payment account linked, create a
        WePay collection account for this project.
        '''

        response = CorePaymentResponse()
        keys = [project.creator]
        keys.extend(project.owners)
        for owner_key in keys:
            accounts = WePayUserPaymentAccount.query(WePayUserPaymentAccount.user == owner_key).fetch()
            if accounts and len(accounts):
                # Create a collection account for this project owner only.
                account_response = PaymentAPI.create_project_payment_account(
                        project.key, project.name,
                        'Collection account for ' + project.name, accounts[0])
                if not account_response.success:
                    pass # TODO: Log an error here or do something!
                response = account_response
                break
        if not response.success:
            if not response.error_code:
                response.error_code = OFPaymentError.OF_NO_PROJECT_OWNERS_WITH_ACCOUNT
            if not response.error_message:
                response.error_message = 'Failed to create a payment account because no owner has linked a WePay account.'
        return response

    def account_for_project(self, project_key):

        ''' Return the payment account for the given project key, or none. '''

        account_key = ndb.Key(WePayProjectAccount, project_key.urlsafe())
        return account_key.get()

    def update_account_balance(self, account):

        ''' Update the balance for a project account. '''

        return WePayAPI.update_account_balance(account)

    def save_user_cc(self, user, cc_info):

        ''' Adds a credit card money source to a user. '''

        return WePayAPI.save_cc_for_user(user, cc_info)

    def back_project(self, project, goal, tier_key, amount, money_source):

        ''' Create a payment that records the contribution amount that will be charged if the project ignites. '''

        response = CorePaymentResponse()

        # Make sure that the goal is open.
        if not goal.funding_open:
            response.error_code = OFPaymentError.OF_NO_ACTIVE_PROJECT_GOAL
            response.error_message = 'This project does not have an active goal to contribute to.'
            return response

        account = self.account_for_project(project.key)
        if not account:
            response.error_code = OFPaymentError.OF_NO_PROJECT_COLLECTION_ACCOUNT
            response.error_message = 'This project does not have a collection account set up to collect money.'
            return response

        description = 'Contribution to %s' % project.name
        payment = Payment(
            amount=amount,
            commission=self._calculate_commission(amount),
            description=description,
            status='p',
            from_user=money_source.owner,
            from_money_source=money_source.key,
            to_project=project.key,
            to_account=self.account_for_project(project.key).key,
            to_project_goal=goal.key,
            to_project_tier=tier_key,
        )
        payment.put()
        response.response = payment

        # Link the payment to the project and update progress.
        add_response = self._add_payment_to_project(project, payment)
        if add_response.success:
            response.success = True
        else:
            response.error_code = add_response.error_code
            response.error_message = add_response.error_message

        return response

    def charge_payments(self, payments):

        '''
        Charge many payments at once when a project goal is completed.
        Returns a list of transactions.
        '''

        return [WePayAPI.execute_payment(p) for p in payments]

    def cancel_payment(self, payment, reason):

        ''' Cancel a single payment. '''

        response = CorePaymentResponse()
        if payment.current_transaction:
            transaction = payment.current_transaction.get()
            if transaction:
                cancel_response = WePayAPI.cancel_payment(transaction, reason)
                if cancel_response.success:
                    response.success = True
                else:
                    response.error_code = cancel_response.error_code
                    response.error_message = cancel_response.error_message
            else:
                response.error_code = OFPaymentError.OF_BAD_CURRENT_TRANSACTION_KEY
                response.error_message = 'Current transaction key exists on payment but points to nothing.'
        else:
            response.success = True

        if response.success:
            payment.status = 'c'
            payment.put()

            # Un-link the payment from the project and update progress.
            self._remove_payment_from_project(payment.to_project.get(), payment)

        return response

    def refund_payment(self, payment, reason, amount=None):

        ''' Refund a single payment. '''

        response = CorePaymentResponse()
        if payment.current_transaction:
            transaction = payment.current_transaction.get()
            if transaction:
                refund_response = WePayAPI.refund_payment(transaction, reason, amount)
                if refund_response.success:
                    response.success = True
                    response.response = refund_response.response
            else:
                response.error_code = OFPaymentError.NO_BAD_TRANSACTION_KEY
                response.error_message = 'Bad current transaction key exists for this payment.'
        else:
            response.error_code = OFPaymentError.NO_TRANSACTION_FOR_REFUND
            response.error_message = 'No transaction exists for this payment.'

            return False

        if response.success:
            # Un-link the payment from the project and update progress.
            self._remove_payment_from_project(payment.to_project.get(), payment)

        return response

    def payment_updated(self, payment_id):

        ''' A payment was updated through an IPN. '''

        return WePayAPI.checkout_updated(payment_id)

    def withdrawal_updated(self, withdrawal_id):

        ''' A withdrawal was updated through an IPN. '''

        return WePayAPI.withdrawal_updated(withdrawal_id)

    def generate_withdrawal_url(self, user, account, amount, note):

        ''' Generate a url where a user can withdraw money from a project payment account. '''

        return WePayAPI.generate_withdrawal(user, account, amount, note)


# Payment API singleton.
PaymentAPI = CorePaymentAPI()
