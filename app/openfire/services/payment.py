from google.appengine.ext import ndb
from apptools.services.builtin import Echo
from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.messages import payment as payment_messages
#from openfire.models.payment import Payment


class PaymentService(RemoteService):

    ''' Payment service api. '''

    @remote.method(payment_messages.UserPaymentAccount, payment_messages.UserPaymentAccount)
    def create_user_payment_account(self, request):

        ''' Create a wepay account for a user or link existing wepay account to user. '''

        return payment_messages.UserPaymentAccount()

    @remote.method(payment_messages.UserPaymentAccount, payment_messages.UserPaymentAccount)
    def get_user_payment_account(self, request):

        ''' Get payment account info for a user. '''

        return payment_messages.UserPaymentAccount()

    @remote.method(payment_messages.CreateProjectAccount, payment_messages.ProjectAccount)
    def create_project_payment_account(self, request):

        ''' Create a wepay sub-account on a user's payment account to collect money for a project. '''

        return payment_messages.ProjectAccount()

    @remote.method(payment_messages.ProjectAccount, payment_messages.ProjectAccount)
    def get_project_payment_account(self, request):

        ''' Get payment account info for a project. '''

        return payment_messages.ProjectAccount()

    @remote.method(payment_messages.PaymentHistory, payment_messages.PaymentHistory)
    def payment_history(self, request):

        ''' Display a history of payments for a user or project. '''

        return payment_messages.PaymentHistory()

    @remote.method(payment_messages.PaymentHistory, payment_messages.PaymentHistory)
    def admin_payment_history(self, request):

        ''' View all payment history. Admin only. '''

        return payment_messages.PaymentHistory()

    @remote.method(payment_messages.BackProject, payment_messages.BackProject)
    def back_project(self, request):

        ''' Back a project with a credit card. Save and authorize the CC info, create a payment for tipping point. '''

        return payment_messages.BackProject()

    @remote.method(payment_messages.MoneySources, payment_messages.MoneySources)
    def money_sources(self, request):

        ''' List money sources (saved credit cards) for a user payment account. '''

        return payment_messages.MoneySources()

    @remote.method(payment_messages.RemoveMoneySource, Echo)
    def remove_money_source(self, request):

        ''' Remove a money source from a user payment account. '''

        return Echo(message='success?')

    @remote.method(payment_messages.MoneySources, payment_messages.MoneySources)
    def admin_money_sources(self, request):

        ''' List all money sources. Admin only. '''

        return payment_messages.MoneySources()

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
