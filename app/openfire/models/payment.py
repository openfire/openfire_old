# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
from openfire.models import AppModel

from openfire.messages import payments as messages
from openfire.pipelines.model import payment as pipelines


class UserPaymentAccount(AppModel):

    ''' An object to store user account information for third party sites. '''

    _message_class = messages.UserPaymentAccount
    _pipeline_class = pipelines.UserPaymentAccountPipeline

    # openfire user.
    user = ndb.KeyProperty('u', indexed=True, required=True)


class WePayUserPaymentAccount(UserPaymentAccount):

    ''' An object to store WePay specific user account information. '''

    _message_class = messages.UserPaymentAccount
    _pipeline_class = pipelines.UserPaymentAccountPipeline

    # WePay user account info.
    wepay_user_id = ndb.IntegerProperty('wu', indexed=True, required=True)
    wepay_email = ndb.StringProperty('we', indexed=True, required=True)
    wepay_access_token = ndb.StringProperty('wt', indexed=True, required=True)
    wepay_token_expires = ndb.DateTimeProperty('wx', indexed=True, required=False)


class ProjectAccount(polymodel.PolyModel):

    '''An account is a polymodel that is tied to a project.

    It is used for accepting payments for a project.
    '''

    _message_class = messages.ProjectAccount
    _pipeline_class = pipelines.ProjectAccountPipeline

    # Accounts are tied to projects.
    project = ndb.KeyProperty('p', indexed=True, required=True)
    name = ndb.StringProperty('n', indexed=False, required=True)
    description = ndb.StringProperty('d', indexed=False, required=True)

    # Account balance.
    balance = ndb.FloatProperty('b', indexed=True, required=True)

    # If a transaction is currently taking place, we keep its key on the account model.
    current_transaction = ndb.KeyProperty('ct', indexed=True, required=False)

    # All transactions in MRU order.
    transactions = ndb.KeyProperty('t', indexed=True, repeated=True)


class WePayProjectAccount(ProjectAccount):

    ''' An subclass of account for WePay accounts. '''

    _message_class = messages.ProjectAccount
    _pipeline_class = pipelines.ProjectAccountPipeline

    wepay_account_id = ndb.IntegerProperty('wi', indexed=True, required=True)


class Payment(AppModel):

    ''' An object used to track a single payment. '''

    _message_class = messages.Payment
    _pipeline_class = pipelines.PaymentPipeline

    description = ndb.StringProperty('n', indexed=True, required=True)
    amount = ndb.StringProperty('a', indexed=True, required=True)
    commission = ndb.FloatProperty('cut', indexed=True, required=True, default=0.0)

    # Status set: (Initial, Pending, Executing, Executed, Refunding, Refunded, Cancelled, Error).
    status = ndb.StringProperty('s', indexed=True, required=True, choices=[
            'i', 'p', 'x', 'ex', 'rg', 'rd', 'c', 'err'])
    error_message = ndb.StringProperty('em', required=False)

    # If a transaction is currently taking place, we keep its key on the payment model.
    current_transaction = ndb.KeyProperty('ct', indexed=True, required=False)

    # All transactions in mru order.
    transactions = ndb.KeyProperty('t', indexed=True, repeated=True)

    # From and to. All are required except from_account.
    from_user = ndb.KeyProperty('fu', indexed=True, required=True)
    from_account = ndb.KeyProperty('fa', indexed=True, required=False)
    from_money_source = ndb.KeyProperty('fm', indexed=True, required=False)

    to_project = ndb.KeyProperty('tp', indexed=True, required=True)
    to_account = ndb.KeyProperty('ta', indexed=True, required=True)
    to_money_source = ndb.KeyProperty('tm', indexed=True, required=False)

    created = ndb.DateTimeProperty('c', indexed=True, auto_now_add=True)
    updated = ndb.DateTimeProperty('u', indexed=True, auto_add=True)
    archived = ndb.BooleanProperty('x', indexed=True, default=False)


class Transaction(polymodel.PolyModel):

    ''' A polymodel used to track a single third party transaction dealing with payments or accounts. '''

    _message_class = messages.Transaction
    _pipeline_class = pipelines.TransactionPipeline

    # Action: (Execute, Authorize, Cancel, Retry, Refund, Withdrawal).
    action = ndb.StringProperty('a', indexed=True, choices=['ex', 'au', 'c', 'rt', 'rf', 'w'])

    # openfire status: (Initial, Pending, Completed, Cancelled, Error).
    status = ndb.StringProperty('s', indexed=True, choices=['i', 'p', 'c', 'x', 'e'])

    created = ndb.DateTimeProperty('c', indexed=True, auto_now_add=True)
    updated = ndb.DateTimeProperty('u', indexed=True, auto_add=True)
    archived = ndb.BooleanProperty('x', indexed=True, default=False)


class WePayCheckoutTransaction(Transaction):

    ''' A subclass of Transaction to deal with WePay checkout transactions. '''

    _message_class = messages.Transaction
    _pipeline_class = pipelines.TransactionPipeline

    # Associated payment object.
    payment = ndb.KeyProperty('p', indexed=True, required=True)

    # WePay checkout ID.
    wepay_checkout_id = ndb.IntegerProperty('wi', indexed=True, required=True)

    # WePay States: (New, Authorized, Reserved, Captured, Settled, Cancelled, Refunded, Charged Back, Failed, Expired)
    wepay_checkout_status = ndb.StringProperty('ws', indexed=True, required=True, choices=[
            'n', 'a', 'r', 'cp', 's', 'c', 'rf', 'cb', 'f', 'e'])

    # Good or service is required by WePay. Choices are (GOODS, SERVICE, DONATION, PERSONAL).
    good_or_service = ndb.StringProperty('gos', indexed=True, required=True, choices=['g', 's', 'd', 'p'], default='s')


class WePayWithdrawalTransaction(Transaction):

    ''' A subclass of Transaction to deal with WePay specific transactions. '''

    _message_class = messages.WithdrawalRequest
    _pipeline_class = pipelines.TransactionPipeline

    # Account to withdraw funds from.
    account = ndb.KeyProperty('wa', indexed=True, required=True)
    note = ndb.StringProperty('nt', indexed=False, required=False)

    # User withdrawing the funds.
    user = ndb.KeyProperty('us', indexed=True, required=True)

    # Optional money source for the disbursement.
    to_money_source = ndb.KeyProperty('tm', indexed=True, required=False)

    # WePay withdrawal object ID.
    wepay_withdrawal_id = ndb.IntegerProperty('wi', indexed=True, required=True)

    # WePay States: (New, Authorized, Captured, Settled, Cancelled, Refunded, Failed, Expired)
    wepay_withdrawal_status = ndb.StringProperty('ws', indexed=True, required=True, choices=[
            'n', 'a', 'cp', 's', 'c', 'rf', 'f', 'e'])


class MoneySource(polymodel.PolyModel):

    ''' A polymodel used for payment sources such as credit cards and bank accounts. '''

    _message_class = messages.MoneySource
    _pipeline_class = pipelines.MoneySourcePipeline

    # Owner is the User or Project this source is tied to.
    owner = ndb.KeyProperty('t', indexed=True, required=True)

    description = ndb.StringProperty('d')
    is_default = ndb.BooleanProperty('id', default=False)
    is_active = ndb.BooleanProperty('ia', default=True)
    save_for_reuse = ndb.BooleanProperty('s', default=True)

    created = ndb.DateTimeProperty('c', indexed=True, auto_now_add=True)
    updated = ndb.DateTimeProperty('u', indexed=True, auto_add=True)
    first_use = ndb.DateTimeProperty('fu', indexed=True, required=False)
    last_use = ndb.DateTimeProperty('lu', indexed=True, required=False)


class WePayCreditCard(MoneySource):

    ''' A subclass of MoneySource to save WePay credit card info for use and reuse. '''

    _message_class = messages.MoneySource
    _pipeline_class = pipelines.MoneySourcePipeline

    wepay_cc_id = ndb.IntegerProperty('cc', indexed=True, required=False)
    wepay_cc_authorized = ndb.BooleanProperty('wa', indexed=True, default=False)
    wepay_cc_state = ndb.StringProperty('ws', indexed=True, required=False) #, choices=['n']) # Only 'new' listed in API?
