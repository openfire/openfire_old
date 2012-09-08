import config
import datetime
from google.appengine.ext import ndb
from openfire.core.payment import wepay_api
from openfire.core.payment.common import CorePaymentResponse, OFPaymentError
from openfire.models.payment import (WePayUserPaymentAccount, WePayCreditCard, WePayCheckoutTransaction,
        WePayWithdrawalTransaction, Payment)

WEPAY_CHECKOUT_STATUS_DICT = {
    'new': 'n',
    'authorized': 'a',
    'reserved': 'r',
    'captured': 'cp',
    'settled': 's',
    'cancelled': 'c',
    'refunded': 'rf',
    'charged back': 'cb',
    'failed': 'f',
    'expired': 'e',
}

WEPAY_WITHDRAWAL_STATUS_DICT = {
    'new': 'n',
    'authorized': 'a',
    'captured': 'cp',
    'settled': 's',
    'cancelled': 'c',
    'refunded': 'rf',
    'failed': 'f',
    'expired': 'e',
}

CHECKOUT_TO_TRANSACTION = {
    'new': 'i',
    'authorized': 'p',
    'reserved': 'p',
    'captured': 'c',
    'settled': 'c',
    'cancelled': 'x',
    'refunded': 'r',
    'charged back': 'r',
    'failed': 'e',
    'expired': 'e',
}

CHECKOUT_TO_PAYMENT = {
    'new': 'p',
    'authorized': 'x',
    'reserved': 'x',
    'captured': 'ex',
    'settled': 'ex',
    'cancelled': 'c',
    'refunded': 'rd',
    'charged back': 'rd',
    'failed': 'err',
    'expired': 'err',
}

WITHDRAWAL_TO_TRANSACTION = {
    'new': 'i',
    'authorized': 'p',
    'captured': 'c',
    'settled': 'c',
    'cancelled': 'x',
    'refunded': 'r',
    'failed': 'e',
    'expired': 'e',
}


class CoreWePayAPI(object):

    ''' A shim to all WePay API functionality for openfire. '''

    def __init__(self, *args, **kwargs):

        ''' Load the wepay config values. '''

        self.config = config.config.get('openfire.wepay', {})

    def _convert_from_wepay_checkout_status(self, wepay_status):

        ''' Convert WePay checkout status to openfire database values. '''

        return WEPAY_CHECKOUT_STATUS_DICT.get(wepay_status, '')

    def _convert_from_wepay_withdrawal_status(self, wepay_status):

        ''' Convert WePay checkout status to openfire database values. '''

        return WEPAY_WITHDRAWAL_STATUS_DICT.get(wepay_status, '')

    def _checkout_to_transaction_status(self, wepay_status):

        ''' Convert WePay checkout status to openfire transaction status database values. '''

        return CHECKOUT_TO_TRANSACTION.get(wepay_status, '')

    def _checkout_to_payment_status(self, wepay_status):

        ''' Convert WePay checkout status to openfire payment status database values. '''

        return CHECKOUT_TO_PAYMENT.get(wepay_status, '')

    def _withdrawal_to_transaction_status(self, wepay_status):

        ''' Convert WePay withdrawal status to openfire transaction status database values. '''

        return WITHDRAWAL_TO_TRANSACTION.get(wepay_status, '')


    # External.

    def get_wepay_object(self, access_token=None):

        ''' Helper method to create and return a WePay object. '''

        return wepay_api.WePay(access_token=access_token, production=self.config.get('use_production', False))

    def generate_oauth_url(self, user):

        ''' Generate a wepay oauth2 url for the user to authenticate openfire. '''

        wepay_obj = self.get_wepay_object()
        user_email = ''
        if user.email and len(user.email):
            user_email = user.email[0].id()
        options = {
            'state': user.key.urlsafe(),
            'user_name': '%s %s' % (user.firstname, user.lastname),
            'user_email': user_email
        }
        response = CorePaymentResponse()
        try:
            wepay_response = wepay_obj.get_authorization_url(
                redirect_uri=self.config['redirect_uri'],
                client_id=self.config[self.config['use_production'] and 'production' or 'staging']['client_id'],
                options=options,
                scope=self.config['auth_scope'],
            )
            response.success = True
            response.response = wepay_response
        except wepay_api.WePayError as e:
            response.error_code = OFPaymentError.WEPAY_OAUTH_URL
            response.error_message = e.message
        return response


    def create_account_for_user(self, user, code):

        ''' Save new account info for a user. '''

        obj = self.get_wepay_object()
        response = CorePaymentResponse()

        try:
            token_response = obj.get_token(
                redirect_uri=self.config.get('redirect_uri', '/me'),
                client_id=self.config[self.config['use_production'] and 'production' or 'staging']['client_id'],
                client_secret=self.config[self.config['use_production'] and 'production' or 'staging']['client_secret'],
                code=code,
            )
            response.success = True
        except wepay_api.WePayError as e:
            response.error_code = OFPaymentError.WEPAY_CREATE_ACCOUNT_FOR_USER
            response.error_message = e.message

        if response.success:
            # Currently we do not set an explicit key to the new user payment account.
            account = WePayUserPaymentAccount(
                user=user.key,
                wepay_user_id=token_response.get('user_id', ''),
                wepay_access_token=token_response.get('access_token', ''),
                wepay_token_expires=token_response.get('expires_in', None), # TODO: Convert format if needed?
            )
            account.put()
            response.response = account

        return response

    def create_payment_account(self, name, description, wepay_account_id):

        ''' Create a payment account for a wepay account. '''

        response = CorePaymentResponse()

        # Get the access_token for this account ID.
        # TODO: Generate the key somehow instead of query/fetch?
        accounts = WePayUserPaymentAccount.query(WePayUserPaymentAccount.wepay_user_id == wepay_account_id).fetch()
        account = None
        if not accounts and len(accounts):
            response.error_code = OFPaymentError.NO_WEPAY_ACCOUNT_FOUND
            response.error_message = "No WePay use account found for given account id."
        else:
            account = accounts[0]

        if account:
            params = {
                'name': name,
                'description': description,
            }
            obj = self.get_wepay_object(access_token=account.wepay_access_token)
            try:
                account_response = obj.call('/account/create', params=params)
                response.success = True
                response.response = account_response['account_id']
            except wepay_api.WePayError as e:
                response.error_code = OFPaymentError.WEPAY_NEED_REAUTH
                response.error_message = e.message

        return response

    def update_account_balance(self, account):

        ''' Update the account balance for the given account. '''

        response = CorePaymentResponse()
        access_token = self.config[self.config['use_production'] and 'production' or 'staging']['access_token']
        wepay_obj = self.get_wepay_object(access_token=access_token)
        try:
            balance_response = wepay_obj.call('/account/balance', {'account_id': account.wepay_account_id})
            account.balance = balance_response['pending_balance']
            account.put()
            response.success = True
            response.response = account
        except wepay_api.WePayError as e:
            response.error_code = OFPaymentError.WEPAY_UPDATE_BALANCE
            response.error_message = e.message

        return response

    def save_cc_for_user(self, user, cc_info):

        ''' Create a credit card entity in WePay, link it to a user account, and authorize it. '''

        # Make the WePay API call.
        response = CorePaymentResponse()
        wepay_obj = self.get_wepay_object()
        cc_params = {
            'client_id': self.config[self.config['use_production'] and 'production' or 'staging']['client_id'],
            'user_name': cc_info.user_name,
            'email': cc_info.email,
            'cc_number': cc_info.cc_num,
            'cvv': cc_info.ccv,
            'expiration_month': cc_info.expire_month,
            'expiration_year': cc_info.expire_year,
            'address': {
                'address1': cc_info.address1,
                'city': cc_info.city,
                'state': cc_info.state,
                'country': cc_info.country,
                'zip': cc_info.zipcode
            }
        }
        # Only add the address2 if it is populated.
        if cc_info.address2:
            cc_params['address']['address2'] = cc_info.address2

        try:
            cc_response = wepay_obj.call('/credit_card/create', cc_params)
            response.success = True
        except wepay_api.WePayError as e:
            response.error_code = OFPaymentError.WEPAY_CC_CREATE
            response.error_message = e.message


        if response.success:
            # Save the credit card object linked to the user.
            wepay_cc = WePayCreditCard(
                owner=user.key,
                description=cc_info.cc_num[:4],
                wepay_cc_id=cc_response['credit_card_id'],
                wepay_cc_state=cc_response['state'],
                save_for_reuse=cc_info.save_for_reuse,
            )
            wepay_cc.put()
            response.response = wepay_cc

            auth_response = {}
            try:
                # Authorize the credit card since we are not going to charge it immediately.
                auth_response = wepay_obj.call('/credit_card/authorize', {
                    'client_id': self.config[self.config['use_production'] and 'production' or 'staging']['client_id'],
                    'client_secret': self.config[self.config['use_production'] and 'production' or 'staging']['client_secret'],
                    'credit_card_id': wepay_cc.wepay_cc_id
                })
            except wepay_api.WePayError as e:
                response.success = False
                response.error_code = OFPaymentError.WEPAY_CC_AUTHORIZE
                response.error_message = e.message

            if response.success:
                wepay_cc.wepay_cc_state = auth_response['state']
                if auth_response.get('credit_card_name', None):
                    wepay_cc.description = auth_response['credit_card_name']
                wepay_cc.put()

        return response

    def execute_payment(self, payment):

        ''' Execute one payment using WePay. '''

        # Begin a checkout transaction.
        response = CorePaymentResponse()
        transaction = WePayCheckoutTransaction(
            action='ex',
            status='i',
            payment=payment.key,
        )
        transaction.put()
        response.response = transaction

        payment.current_transaction = transaction.key
        payment.all_transactions.append(transaction.key)
        payment.status = 'x'
        payment.put()

        money_source = payment.from_money_source.get()

        # Make the WePay create checkout API call.
        access_token = payment.to_account.get().payment_account.get().wepay_access_token
        wepay_obj = self.get_wepay_object(access_token=access_token)

        try:
            checkout_response = wepay_obj.call('/checkout/create', {
                # Required.
                'account_id': payment.to_account.get().wepay_account_id,
                'short_description': payment.description,
                'type': 'GOODS', # TODO: Would it be OK to use DONATION?
                'amount': payment.amount,

                # Required for cc tokenization.
                'payment_method_type': 'credit_card',
                'payment_method_id': money_source.wepay_cc_id,

                # Internal payment settings.
                'reference_id': transaction.key.urlsafe(),
                'app_fee': payment.commission,
                'fee_payer': 'Payee',
                'redirect_uri': self.config.get('redirect_uri', '/me'),
                'callback_uri': self.config.get('callback_uri', '/_payment/ipn'),
                'auto_capture': True,

                # Other fields that are not required but we could use.
                #'long_description': ,
                #'payer_email_message': ,
                #'payee_email_message': ,
                #'require_shipping': ,
                #'shipping_fee': ,
                #'charge_tax': ,
                #'prefill_info': ,
                #'funding_sources': ,

                # Other fields that are not required and we should never use.
                #'mode': ,
                #'preapproval_id': ,
            })
            response.success = True
        except wepay_api.WePayError as e:
            response.error_code = OFPaymentError.WEPAY_CHECKOUT_CREATE
            response.error_message = e.message

        if response.success:
            # Update the transaction with the returned checkout ID and state.
            transaction.wepay_checkout_id = checkout_response['checkout_id']
            transaction.wepay_checkout_status = self._convert_from_wepay_checkout_status(checkout_response['state'])
            transaction.status = self._checkout_to_transaction_status(checkout_response['state'])
            transaction.put()

            # Update money source use times.
            use_time = datetime.datetime.now()
            if not money_source.first_use:
                money_source.first_use = use_time
            money_source.last_use = use_time
            money_source.put()

        else:
            transaction.status = 'e'
            transaction.put()
            payment.status = 'err'
            payment.put()

        return response

    def cancel_payment(self, transaction, reason):

        ''' Cancel a payment. '''

        # Make the WePay cancel checkout API call.
        response = CorePaymentResponse()
        access_token = self.config[self.config['use_production'] and 'production' or 'staging']['access_token']
        wepay_obj = self.get_wepay_object(access_token=access_token)
        params = {
            'checkout_id': transaction.wepay_checkout_id,
            'cancel_reason': reason,
        }
        try:
            cancel_response = wepay_obj.call('/checkout/cancel', params)
            response.success = True
            response.response = cancel_response
        except wepay_api.WePayError as e:
            response.error_code = OFPaymentError.WEPAY_CHECKOUT_CANCEL
            response.error_message = e.message

        if response.success:
            transaction.wepay_checkout_status = self._convert_from_wepay_checkout_status(cancel_response['state'])
            transaction.put()

        return response

    def refund_payment(self, transaction, reason, amount=None):

        ''' Refund a payment. '''

        # Make the WePay refund checkout API call.
        response = CorePaymentResponse()
        access_token = self.config[self.config['use_production'] and 'production' or 'staging']['access_token']
        wepay_obj = self.get_wepay_object(access_token=access_token)
        params = {
            'checkout_id': transaction.wepay_checkout_id,
            'refund_reason': reason,
        }
        if amount != None:
            params['amount'] = amount

        try:
            refund_response = wepay_obj.call('/checkout/refund', params)
            response.success = True
            response.response = refund_response
        except wepay_api.WePayError as e:
            response.error_code = OFPaymentError.WEPAY_CHECKOUT_CANCEL
            response.error_message = e.message

        if response.success:
            transaction.wepay_checkout_status = self._convert_from_wepay_checkout_status(refund_response['state'])
            transaction.put()

        return response

    def checkout_updated(self, checkout_id):

        ''' A checkout was updated. Fetch and save the new state information. '''

        response = CorePaymentResponse()
        access_token = self.config[self.config['use_production'] and 'production' or 'staging']['access_token']
        wepay_obj = self.get_wepay_object(access_token=access_token)

        try:
            checkout_response = wepay_obj.call('/checkout', {'checkout_id': checkout_id})
            response.success = True
        except wepay_api.WePayError as e:
            response.error_code = OFPaymentError.WEPAY_CHECKOUT_CANCEL
            response.error_message = e.message

        if response.success:
            # Look up the transaction from the checkout reference ID.
            transaction_key = ndb.Key(urlsafe=checkout_response['reference_id'])
            transaction = transaction_key.get()
            response.response = transaction

            # Update the transaction if the state has changed.
            new_state = checkout_response['state']
            new_db_state = self._convert_from_wepay_checkout_status(new_state)
            if not new_db_state == transaction.wepay_checkout_status:
                transaction.wepay_checkout_status = new_db_state
                transaction.status = self._checkout_to_transaction_status(new_state)
                transaction.put()

                # Update the payment for which this is the current transaction.
                payments = Payment.query(Payment.current_transaction == transaction.key).fetch()
                for payment in payments:
                    payment.status = self._checkout_to_payment_status(new_state)
                    payment.put()

                # Update the account that the payment is going to.
                balance_response = self.update_account_balance(payment.to_account.get())
                if not balance_response.success:
                    response.error_message += '(Failed to update account balance after checkout update.)'

        return response

    def generate_withdrawal(self, user, account, amount, note):

        ''' Generate a url and object to track withdrawing funds from a payment account. '''

        response = CorePaymentResponse()
        access_token = self.config[self.config['use_production'] and 'production' or 'staging']['access_token']
        wepay_obj = self.get_wepay_object(access_token=access_token)

        try:
            withdrawal_response = wepay_obj.call('/withdrawal/create', {
                'account_id': account.wepay_account_id,
                'amount': amount,
                'note': note,
                'redirect_uri': self.config.get('redirect_uri', '/me'),
                'callback_uri': self.config.get('callback_uri', '/_payment/ipn'),
            })
            response.success = True
        except wepay_api.WePayError as e:
            response.error_code = OFPaymentError.WEPAY_WITHDRAWAL_CREATE
            response.error_message = e.message

        if response.success:
            withdrawal = WePayWithdrawalTransaction(
                action='w',
                account=account.key,
                note=note,
                user=user,
                wepay_withdrawal_id=withdrawal_response['withdrawal_id'],
                wepay_withdrawal_uri=withdrawal_response['withdrawal_uri'],
            )
            withdrawal.put()
            response.response = withdrawal

        return response

    def withdrawal_updated(self, withdrawal_id):

        ''' A withdrawal was updated. Fetch and save the new state information. '''

        response = CorePaymentResponse()
        withdrawal = WePayWithdrawalTransaction.query(WePayWithdrawalTransaction.wepay_withdrawal_id == withdrawal_id).fetch()[0]
        if not withdrawal:
            response.error_code = OFPaymentError.NO_WEPAY_ACCOUNT_FOUND
            response.error_message = "No WePay use account found with given withdrawal id."
        else:
            response.response = withdrawal

        if response.response:
            access_token = self.config[self.config['use_production'] and 'production' or 'staging']['access_token']
            wepay_obj = self.get_wepay_object(access_token=access_token)
            try:
                withdrawal_response = wepay_obj.call('/withdrawal', {'withdrawal_id': withdrawal_id})
                response.success = True
            except wepay_api.WePayError as e:
                response.error_code = OFPaymentError.WEPAY_WITHDRAWAL_CREATE
                response.error_message = e.message

            if response.success:
                new_state = withdrawal_response['state']
                new_db_state = self._convert_from_wepay_withdrawal_status(new_state)
                if not new_db_state == withdrawal.wepay_withdrawal_status:
                    withdrawal.wepay_withdrawal_status = new_db_state
                    withdrawal.status = self._withdrawal_to_transaction_status(new_state)
                    withdrawal.put()

        return response


WePayAPI = CoreWePayAPI()
