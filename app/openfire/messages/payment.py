from protorpc import messages

class AuthURL(messages.Message):

    ''' Return an auth url to allow openfire to manage a user's payments. '''

    url = messages.StringField(1)


class UserPaymentAccount(messages.Message):

    ''' Create or get a user payment account. '''

    key = messages.StringField(1)
    user = messages.StringField(2)
    wepay_email = messages.StringField(3)
    wepay_user_id = messages.IntegerField(4)


class ProjectAccount(messages.Message):

    ''' A project payment account. '''

    key = messages.StringField(1)
    project = messages.StringField(2)
    name = messages.StringField(3)
    description = messages.StringField(4)
    wepay_account_id = messages.IntegerField(5)
    balance = messages.FloatField(6)


class Transaction(messages.Message):

    ''' A transaction object. '''

    key = messages.StringField(1)
    action = messages.StringField(2)
    status = messages.StringField(3)
    created = messages.StringField(4)
    updated = messages.StringField(5)
    archived = messages.StringField(6)


class MoneySource(messages.Message):

    ''' A single user money source. '''

    key = messages.StringField(1)
    owner = messages.StringField(2)
    description = messages.StringField(3)
    is_default = messages.BooleanField(4)
    is_active = messages.BooleanField(5)
    save_for_reuse = messages.BooleanField(6)
    created = messages.StringField(7)
    updated = messages.StringField(8)
    first_use = messages.StringField(9)
    last_use = messages.StringField(10)


class Payment(messages.Message):

    ''' A payment object. '''

    key = messages.StringField(1)
    description = messages.StringField(2)
    amount = messages.StringField(3)
    commission = messages.StringField(4)
    status = messages.StringField(5)
    error_message = messages.StringField(6)
    current_transaction = messages.MessageField(Transaction, 7)
    transactions = messages.MessageField(Transaction, 8, repeated=True)
    from_user = messages.StringField(9)
    from_account = messages.MessageField(UserPaymentAccount, 10)
    from_money_source = messages.MessageField(MoneySource, 11)
    to_user = messages.StringField(12)
    to_account = messages.MessageField(UserPaymentAccount, 13)
    to_project_tier = messages.StringField(14)
    created = messages.StringField(15)
    updated = messages.StringField(16)
    archived = messages.StringField(17)


class PaymentHistory(messages.Message):

    ''' A payment history for a user or project. '''

    target = messages.StringField(1)
    payments = messages.MessageField(Payment, 2, repeated=True)
    start = messages.StringField(3)
    end = messages.StringField(4)


class CreditCard(messages.Message):
    cc_num = messages.StringField(1)
    ccv = messages.StringField(2)
    expire_month = messages.StringField(3)
    expire_year = messages.StringField(4)
    user_name = messages.StringField(5)
    email = messages.StringField(6)
    address1 = messages.StringField(7)
    address2 = messages.StringField(8)
    city = messages.StringField(9)
    state = messages.StringField(10)
    country = messages.StringField(11)
    zipcode = messages.StringField(12)
    save_for_reuse = messages.BooleanField(13)


class BackProject(messages.Message):

    ''' Request to back a project with money. '''

    user = messages.StringField(1)
    project = messages.StringField(2)
    tier = messages.StringField(3)
    amount = messages.StringField(4)
    money_source = messages.StringField(5)
    new_cc = messages.MessageField(CreditCard, 6)


class MoneySources(messages.Message):

    ''' User money sources. '''

    user = messages.StringField(1)
    sources = messages.MessageField(MoneySource, 2, repeated=True)


class RemoveMoneySource(messages.Message):

    ''' Remove a money source. '''

    source = messages.StringField(1)


class CancelPayment(messages.Message):

    ''' Cancel a payment that has not yet been charged. '''

    payment = messages.StringField(1)
    reason = messages.StringField(2)


class RefundPayment(messages.Message):

    ''' Start a payment refund. '''

    payment = messages.StringField(1)
    reason = messages.StringField(2)
    amount = messages.StringField(3)


class WithdrawalRequest(messages.Message):

    ''' Request to withdraw funds from a project account. '''

    account = messages.StringField(1)
    amount = messages.StringField(2)
    note = messages.StringField(3)


class WithdrawalResponse(messages.Message):

    ''' Response allowing a user to withdraw funds from the provided url. '''

    url = messages.StringField(1)


class WithdrawalHistory(messages.Message):

    ''' Withdrawal history for a payment account. '''

    account = messages.StringField(1)
    withdrawals = messages.MessageField(WithdrawalRequest, 2, repeated=True)
    start = messages.StringField(3)
    end = messages.StringField(4)
