from google.appengine.ext import ndb
from apptools.services.builtin import Echo
from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.messages import payment as payment_messages
#from openfire.models.payment import Payment

from openfire.core.payment import PaymentAPI


class PaymentService(RemoteService):

    ''' Payment service api. '''

    @remote.method(message_types.VoidMessage, payment_messages.AuthURL)
    def get_auth_url(self, request):

        ''' Generate an oauth url that the user can visit to authorize the openfire app. '''

        url = PaymentAPI.generate_auth_url(request.sessions.user)
        return payment_messages.AuthURL(url=url)

    @remote.method(payment_messages.UserPaymentAccount, payment_messages.UserPaymentAccount)
    def get_user_payment_account(self, request):

        ''' Get payment account info for a user. '''

        account = ndb.Key(urlsafe=request.key).get()
        return account.to_message()

    @remote.method(payment_messages.ProjectAccount, payment_messages.ProjectAccount)
    def create_project_payment_account(self, request):

        ''' Create a wepay sub-account on a user's payment account to collect money for a project. '''

        project_key = ndb.Key(urlsafe=request.project)
        project_account = PaymentAPI.create_project_payment_account(project_key, request.name,
                request.description, request.wepay_account_id)
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

    @remote.method(payment_messages.BackProject, Echo)
    def back_project(self, request):

        ''' Back a project with a credit card. Save and authorize the CC info, create a payment for tipping point. '''

        # If no money source is given, save the cc info as a money source first.
        if not request.money_source and request.new_cc:
            money_source = PaymentAPI.save_user_cc(request.session.user, request.new_cc)
        elif request.money_source:
            money_source = request.money_source
        else:
            # TODO: No money source provided?
            return Echo(message='No money source provided.')

        # Make a record of the payment amount to be charged if the projects ignites.
        payment = PaymentAPI.back_project(request.project, request.tier, request.amount, money_source)
        if not payment:
            # TODO: What to do on error?
            return Echo(message='There was an error...try again?')
        return Echo(message='Thanks for contributing!')

    @remote.method(payment_messages.MoneySources, payment_messages.MoneySources)
    def money_sources(self, request):

        ''' List money sources (saved credit cards) for a user account. '''

        return payment_messages.MoneySources()

    @remote.method(payment_messages.RemoveMoneySource, Echo)
    def remove_money_source(self, request):

        ''' Remove a money source from a user payment account. '''

        return Echo(message='success?')

    @remote.method(payment_messages.MoneySources, payment_messages.MoneySources)
    def admin_money_sources(self, request):

        ''' List all money sources. Admin only. '''

        return payment_messages.MoneySources()

    @remote.method(payment_messages.PaymentHistory, payment_messages.PaymentHistory)
    def payment_history(self, request):

        ''' Display a history of payments for a user or project. '''

        return payment_messages.PaymentHistory()

    @remote.method(payment_messages.PaymentHistory, payment_messages.PaymentHistory)
    def admin_payment_history(self, request):

        ''' View all payment history. Admin only. '''

        return payment_messages.PaymentHistory()

    @remote.method(payment_messages.RefundPayment, payment_messages.RefundPayment)
    def refund_payment(self, request):

        ''' Start a refund for a payment. '''

        return payment_messages.RefundPayment()

    @remote.method(payment_messages.WithdrawalRequest, payment_messages.WithdrawalRequest)
    def withdraw_funds(self, request):

        ''' Request to withdraw funds. Provides a wepay link to do the actual withdrawal. '''

        return payment_messages.WithdrawalRequest()

    @remote.method(payment_messages.WithdrawalHistory, payment_messages.WithdrawalHistory)
    def withdrawal_history(self, request):

        ''' Get a history of withdrawals for a user. '''

        return payment_messages.WithdrawalHistory()

    @remote.method(payment_messages.WithdrawalHistory, payment_messages.WithdrawalHistory)
    def admin_withdrawal_history(self, request):

        ''' Get all of the withdrawals. Admin only. '''

        return payment_messages.WithdrawalHistory()
