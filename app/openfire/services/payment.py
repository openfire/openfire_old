from google.appengine.ext import ndb
from apptools.services.builtin import Echo
from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.messages import payment as payment_messages
from openfire.models.payment import MoneySource, Payment, Transaction, WePayWithdrawalTransaction, WePayUserPaymentAccount
from openfire.models.user import User
from openfire.models.project import Project

from openfire.core.payment import PaymentAPI


class PaymentService(RemoteService):

    ''' Payment service api. '''

    @remote.method(payment_messages.AuthURL, payment_messages.AuthURL)
    def get_auth_url(self, request):

        ''' Generate an oauth url that the user can visit to authorize the openfire app. '''

        url = PaymentAPI.generate_auth_url(self.user)
        return payment_messages.AuthURL(url=url)

    @remote.method(payment_messages.UserPaymentAccount, payment_messages.UserPaymentAccount)
    def get_user_payment_account(self, request):

        ''' Get payment account info for a user. '''

        if not request.key:
            return payment_messages.UserPaymentAccount()

        account = ndb.Key(urlsafe=request.key).get()
        return account.to_message()

    @remote.method(payment_messages.ProjectAccount, payment_messages.ProjectAccount)
    def create_project_payment_account(self, request):

        ''' Create a wepay sub-account on a user's payment account to collect money for a project. '''

        if not request.project:
            return payment_messages.ProjectAccount()

        project_key = ndb.Key(urlsafe=request.project)
        project = project_key.get()

        # If an account already exists, just return that.
        existing_account = PaymentAPI.account_for_project(project)
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

        project_account = PaymentAPI.create_project_payment_account(project_key, name, description, account)
        return project_account.to_message()

    @remote.method(payment_messages.ProjectAccount, payment_messages.ProjectAccount)
    def get_project_payment_account(self, request):

        ''' Get payment account info for a project. '''

        if not request.project:
            return payment_messages.ProjectAccount()

        if not request.key:
            return payment_messages.ProjectAccount()
        account = ndb.Key(urlsafe=request.key).get()
        return account.to_message()

    @remote.method(payment_messages.ProjectAccount, payment_messages.ProjectAccount)
    def update_account_balance(self, request):

        ''' Update the balance of a project account. '''

        if not request.key:
            return payment_messages.ProjectAccount()
        account = ndb.Key(urlsafe=request.key).get()
        PaymentAPI.update_account_balance(account)
        return account.to_message()

    @remote.method(payment_messages.BackProject, Echo)
    def back_project(self, request):

        ''' Back a project with a credit card. Save and authorize the CC info, create a payment for tipping point. '''

        if not self.user:
            return Echo(message='You are not logged in.')
        if not request.project:
            return Echo(message='No project provided.')

        project_key = ndb.Key(urlsafe=request.project)
        project = project_key.get()
        if not project:
            return Echo(message='Failed to find project.')

        # If no money source is given, save the cc info as a money source first.
        if not request.money_source and request.new_cc:
            money_source = PaymentAPI.save_user_cc(self.user, request.new_cc)
        elif request.money_source:
            money_source = ndb.Key(urlsafe=request.money_source).get()
        else:
            return Echo(message='No money source provided.')

        # Make a record of the payment amount to be charged if the projects ignites.
        payment = PaymentAPI.back_project(project, project.active_goal, ndb.Key(urlsafe=request.tier), float(request.amount), money_source)
        if not payment:
            # TODO: What to do on error?
            return Echo(message='There was an error...try again?')
        return Echo(message='Thanks for contributing!')

    @remote.method(payment_messages.MoneySources, payment_messages.MoneySources)
    def money_sources(self, request):

        ''' List money sources (saved credit cards) for a user account. '''

        if not self.user:
            return payment_messages.MoneySources()
        sources = MoneySource.query(MoneySource.owner == self.user.key, MoneySource.save_for_reuse == True).fetch()
        msgs = []
        for source in sources:
            msgs.append(source.to_message())
        return payment_messages.MoneySources(user=self.user.key.urlsafe(), sources=msgs)

    @remote.method(payment_messages.RemoveMoneySource, Echo)
    def remove_money_source(self, request):

        ''' Remove a money source from a user payment account by setting save for reuse to false. '''

        if not request.source:
            return Echo(message='No money source provided.')

        source_key = ndb.Key(urlsafe=request.source)
        source = source_key.get()
        if not source:
            return Echo(message='Money source not found.')

        source.save_for_reuse = False
        source.put()

        return Echo(message='success')

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
            return payment_messages.PaymentHistory()

        target_key = ndb.Key(urlsafe=request.target)
        kind = target_key.kind()
        query = None
        if kind == User:
            query = Payment.query(Payment.from_user == target_key)
        elif kind == Project:
            query = Payment.query(Payment.to_project == target_key)
        else:
            # Not user nor project.
            return payment_messages.PaymentHistory()

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
            return Echo(message='No payment provided.')

        payment_key = ndb.Key(urlsafe=request.payment)
        payment = payment_key.get()
        if not payment:
            return Echo(message='Payment not found.')

        reason = request.reason
        if not reason:
            reason = "UNKNOWN"
        canceled = PaymentAPI.cancel_payment(payment, reason)
        if not canceled:
            return Echo(message='Failed to cancel payment.')
        return Echo(message='success')

    @remote.method(payment_messages.RefundPayment, Echo)
    def refund_payment(self, request):

        ''' Start a refund for a payment. '''

        if not request.payment:
            return Echo(message='No payment provided.')

        payment_key = ndb.Key(urlsafe=request.payment)
        payment = payment_key.get()
        if not payment:
            return Echo(message='Payment not found.')

        reason = request.reason
        if not reason:
            reason = "UNKNOWN"
        refunded = PaymentAPI.refund_payment(payment, reason, request.amount)
        if not refunded:
            return Echo(message='Failed to refund payment.')
        return Echo(message='success')

    @remote.method(payment_messages.WithdrawalRequest, payment_messages.WithdrawalResponse)
    def withdraw_funds(self, request):

        ''' Request to withdraw funds. Provides a wepay link to do the actual withdrawal. '''

        if not request.account:
            return payment_messages.WithdrawalResponse()

        account_key = ndb.Key(urlsafe=request.account)
        account = account_key.get()
        if not account:
            return payment_messages.WithdrawalRequest()
        withdrawal_url = PaymentAPI.generate_withdrawal_url(self.user, account, request.amount, request.note)
        return payment_messages.WithdrawalResponse(url=withdrawal_url)

    @remote.method(payment_messages.WithdrawalHistory, payment_messages.WithdrawalHistory)
    def withdrawal_history(self, request):

        ''' Get a history of withdrawals for a project account. '''

        # TODO: Permissions.

        if not request.account:
            return payment_messages.WithdrawalHistory()

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
