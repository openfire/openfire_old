from protorpc import remote
from google.appengine.ext import ndb
from apptools.services.builtin import Echo

from openfire.core.payment import PaymentAPI
from openfire.services import RemoteService
from openfire.messages import payment as payment_messages
from openfire.models.user import User
from openfire.models.project import Project
from openfire.models.payment import MoneySource, Payment, WePayWithdrawalTransaction, WePayUserPaymentAccount



class PaymentService(RemoteService):

    ''' Payment service api. '''

    @remote.method(payment_messages.AuthURL, payment_messages.AuthURL)
    def get_auth_url(self, request):

        ''' Generate an oauth url that the user can visit to authorize the openfire app. '''

        response = PaymentAPI.generate_auth_url(self.user)
        if not response.success:
            raise self.exceptions.ApplicationError(response.error_message)
        return payment_messages.AuthURL(url=response.response)

    @remote.method(payment_messages.UserPaymentAccount, payment_messages.UserPaymentAccount)
    def get_user_payment_account(self, request):

        ''' Get payment account info for a user. '''

        if not request.key:
            raise self.exceptions.ApplicationError('No payment account provided.')
        account = ndb.Key(urlsafe=request.key).get()
        if not account:
            raise self.exceptions.ApplicationError('No payment account found.')
        return account.to_message()

    @remote.method(payment_messages.ProjectAccount, payment_messages.ProjectAccount)
    def create_project_payment_account(self, request):

        ''' Create a wepay sub-account on a user's payment account to collect money for a project. '''

        if not request.project:
            raise self.exceptions.ApplicationError('No project provided.')

        project_key = ndb.Key(urlsafe=request.project)
        project = project_key.get()

        # If an account already exists, just return that.
        existing_account = PaymentAPI.account_for_project(project_key)
        if existing_account:
            return existing_account.to_message()

        # If any of the owners have a payment account linked, create a collection account for this project.
        account = None
        for owner_key in project.owners:
            accounts = WePayUserPaymentAccount.query(WePayUserPaymentAccount.user == owner_key).fetch()
            if accounts and len(accounts):
                # Create a collection account for this project owner's account only.
                account = accounts[0]
                break

        # Get or create the name and description.
        name = request.name
        if not name:
            name = project.name
        description = request.description
        if not description:
            description = "Collection account for " + project.name

        response = PaymentAPI.create_project_payment_account(project_key, name, description, account)
        if not response.success:
            raise self.exceptions.ApplicationError(response.error_message)
        return response.response.to_message()

    @remote.method(payment_messages.ProjectAccount, payment_messages.ProjectAccount)
    def get_project_payment_account(self, request):

        ''' Get payment account info for a project. '''

        account = None
        if request.key:
            account = ndb.Key(urlsafe=request.key).get()
            if not account:
                raise self.exceptions.ApplicationError('No project account found.')
        elif request.project:
            project_key = ndb.Key(urlsafe=request.project)
            account = PaymentAPI.account_for_project(project_key)
            if not account:
                raise self.exceptions.ApplicationError('No account found for project.')
        else:
            raise self.exceptions.ApplicationError('No project or account provided.')

        return account.to_message()

    @remote.method(payment_messages.ProjectAccount, payment_messages.ProjectAccount)
    def update_account_balance(self, request):

        ''' Update the balance of a project account. '''

        if not request.key:
            raise self.exceptions.ApplicationError('No account provided.')
        account = ndb.Key(urlsafe=request.key).get()
        response = PaymentAPI.update_account_balance(account)
        if not response.success:
            raise self.exceptions.ApplicationError(response.error_message)
        return response.response.to_message()

    @remote.method(payment_messages.BackProject, Echo)
    def back_project(self, request):

        ''' Back a project with a credit card. Save and authorize the CC info, create a payment for tipping point. '''

        if not self.user:
            raise self.exceptions.ApplicationError('You are not logged in.')
        if not request.project:
            raise self.exceptions.ApplicationError('No project provided.')

        project_key = ndb.Key(urlsafe=request.project)
        project = project_key.get()
        if not project:
            raise self.exceptions.ApplicationError('No project found.')

        if not project.active_goal:
            raise self.exceptions.ApplicationError('No active goal set for this project.')
        goal = project.active_goal.get()
        if not goal:
            raise self.exceptions.ApplicationError('No active goal found for this project.')

        # If no money source is given, save the cc info as a money source first.
        if not request.money_source and request.new_cc:
            save_cc_response = PaymentAPI.save_user_cc(self.user, request.new_cc)
            if not save_cc_response.success:
                raise self.exceptions.ApplicationError(save_cc_response.error_message)
            money_source = save_cc_response.response
        elif request.money_source:
            money_source = ndb.Key(urlsafe=request.money_source).get()
        else:
            raise self.exceptions.ApplicationError('No money source provided.')

        # Call the core API to back the project.
        try:
            payment_response = PaymentAPI.back_project(project, goal,
                    ndb.Key(urlsafe=request.tier), float(request.amount), money_source)
            if not payment_response.success:
                raise self.exceptions.ApplicationError('There was an error: ' + payment_response.error_message)
        except Exception as e:
            # TODO: Let's have a catch all for now that we can email to ourselves
            #       in case anything goes wrong while backing a project. So, remove this
            #       from what the user sees and log/email the error.
            raise self.exceptions.ApplicationError('Failed to donate to project. Please again. ADMIN: ' + e.message)

        # Save the next step votes if there are any.
        all_votes_recorded= True
        if request.next_step_votes:
            for vote in request.next_step_votes:
                step = ndb.Key(urlsafe=vote.key).get()
                if not step:
                    all_votes_recorded = False
                elif vote.num_votes > 0:
                    step.votes = step.votes + vote.num_votes
                    step.put()

        return Echo(message='Thanks for contributing! (all votes recorded? %s)' % all_votes_recorded)

    @remote.method(payment_messages.MoneySources, payment_messages.MoneySources)
    def money_sources(self, request):

        ''' List money sources (saved credit cards) for a user account. '''

        if not self.user:
            raise self.exceptions.ApplicationError('You are not logged in.')
        sources = MoneySource.query(MoneySource.owner == self.user.key, MoneySource.save_for_reuse == True).fetch()
        msgs = []
        for source in sources:
            msgs.append(source.to_message())
        return payment_messages.MoneySources(user=self.user.key.urlsafe(), sources=msgs)

    @remote.method(payment_messages.RemoveMoneySource, Echo)
    def remove_money_source(self, request):

        ''' Remove a money source from a user payment account by setting save for reuse to false. '''

        if not request.source:
            raise self.exceptions.ApplicationError('No money source provided.')

        source = ndb.Key(urlsafe=request.source).get()
        if not source:
            raise self.exceptions.ApplicationError('No money source found.')

        source.save_for_reuse = False
        source.put()

        return Echo(message='Successfully removed money source.')

    @remote.method(payment_messages.MoneySources, payment_messages.MoneySources)
    def admin_money_sources(self, request):

        ''' List all money sources. Admin only. '''

        sources = MoneySource.query().fetch()
        return payment_messages.MoneySources(sources=sources)

    @remote.method(payment_messages.PaymentHistory, payment_messages.PaymentHistory)
    def payment_history(self, request):

        ''' Display a history of payments for a user or project. '''

        # TODO: Permissions.

        if not request.target:
            raise self.exceptions.ApplicationError('No target provided.')

        target_key = ndb.Key(urlsafe=request.target)
        kind = target_key.kind()
        query = None
        if kind == User:
            query = Payment.query(Payment.from_user == target_key)
        elif kind == Project:
            query = Payment.query(Payment.to_project == target_key)
        else:
            # Not user nor project.
            raise self.exceptions.ApplicationError('Target is wrong kind.')

        # Filter by date if given.
        if request.start:
            query = query.filter(Payment.created >= request.start)
        if request.end:
            query = query.filter(Payment.created <= request.end)

        payments = [p.to_message for p in query.fetch()]
        return payment_messages.PaymentHistory(payments=payments, start=request.start, end=request.end, target=request.target)

    @remote.method(payment_messages.PaymentHistory, payment_messages.PaymentHistory)
    def admin_payment_history(self, request):

        ''' View all payment history. Admin only. '''

        # Filter by date if given.
        query = Payment.query()
        if request.start:
            query = query.filter(Payment.created >= request.start)
        if request.end:
            query = query.filter(Payment.created <= request.end)
        payments = [p.to_message for p in query.fetch()]
        return payment_messages.PaymentHistory(payments=payments, start=request.start, end=request.end, target=request.target)

    @remote.method(payment_messages.CancelPayment, Echo)
    def cancel_payment(self, request):

        ''' Cancel a payment that has not yet been charged. '''

        if not request.payment:
            raise self.exceptions.ApplicationError('No payment provided.')

        payment = ndb.Key(urlsafe=request.payment).get()
        if not payment:
            raise self.exceptions.ApplicationError('No payment found.')

        # TODO: Require reason.
        reason = request.reason
        if not reason:
            reason = "UNKNOWN"

        response = PaymentAPI.cancel_payment(payment, reason)
        if not response.success:
            raise self.exceptions.ApplicationError(response.error_message)
        return Echo(message='success')

    @remote.method(payment_messages.RefundPayment, Echo)
    def refund_payment(self, request):

        ''' Start a refund for a payment. '''

        if not request.payment:
            raise self.exceptions.ApplicationError('No payment provided.')

        payment = ndb.Key(urlsafe=request.payment).get()
        if not payment:
            raise self.exceptions.ApplicationError('No payment found.')

        # TODO: Require reason.
        reason = request.reason
        if not reason:
            reason = "UNKNOWN"

        response = PaymentAPI.refund_payment(payment, reason, request.amount)
        if not response.success:
            raise self.exceptions.ApplicationError(response.error_message)
        return Echo(message='success')

    @remote.method(payment_messages.WithdrawalRequest, payment_messages.WithdrawalRequest)
    def withdraw_funds(self, request):

        ''' Request to withdraw funds. Provides a wepay link to do the actual withdrawal. '''

        if not request.account:
            raise self.exceptions.ApplicationError('No account provided.')

        account = ndb.Key(urlsafe=request.account).get()
        if not account:
            raise self.exceptions.ApplicationError('No accout found.')
        response = PaymentAPI.generate_withdrawal_url(self.user, account, request.amount, request.note)
        if not response.success:
            raise self.exceptions.ApplicationError(response.error_message)
        return response.response.to_message()

    @remote.method(payment_messages.WithdrawalHistory, payment_messages.WithdrawalHistory)
    def withdrawal_history(self, request):

        ''' Get a history of withdrawals for a project account. '''

        # TODO: Permissions.

        if not request.account:
            raise self.exceptions.ApplicationError('No account provided.')

        account_key = ndb.Key(urlsafe=request.account)
        query = WePayWithdrawalTransaction.query(WePayWithdrawalTransaction.account == account_key)

        # Filter by date if given.
        if request.start:
            query = query.filter(Payment.created >= request.start)
        if request.end:
            query = query.filter(Payment.created <= request.end)

        withdrawals = [w.to_message for w in query.fetch()]
        return payment_messages.WithdrawalHistory(withdrawals=withdrawals, start=request.start, end=request.end, account=request.account)

    @remote.method(payment_messages.WithdrawalHistory, payment_messages.WithdrawalHistory)
    def admin_withdrawal_history(self, request):

        ''' Get all of the withdrawals. Admin only. '''

        # TODO: Permissions.

        query = WePayWithdrawalTransaction.query()

        # Filter by date if given.
        if request.start:
            query = query.filter(Payment.created >= request.start)
        if request.end:
            query = query.filter(Payment.created <= request.end)

        withdrawals = [w.to_message for w in query.fetch()]
        return payment_messages.WithdrawalHistory(withdrawals=withdrawals, start=request.start, end=request.end, account=request.account)
