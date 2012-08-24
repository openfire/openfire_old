import config
from openfire.core.payment import wepay_api
from openfire.models.payment import WePayUserPaymentAccount, WePayCreditCard

class CoreWePayAPI(object):

    ''' A shim to all WePay API functionality for openfire. '''

    def __init__(self, *args, **kwargs):

        ''' Load the wepay config values. '''

        self.config = config.config.get('openfire.wepay', {})

    def get_wepay_object(self, access_token=None):

        ''' Helper method to create and return a WePay object. '''

        return wepay_api.WePay(access_token=access_token, production=self.config.get('use_production', False))

    def generate_oauth_url(self, user):

        ''' Generate a wepay oauth2 url for the user to authenticate openfire. '''

        wepay_obj = self.get_wepay_object()
        user_email = ''
        if user.email and len(user.email):
            user_email = user.email[0].address
        options = {
            'state': user.key.urlsafe(),
            'user_name': '%s %s' % (user.firstname, user.lastname),
            'user_email': user_email
        }
        return wepay_obj.get_authorization_url(
            redirect_uri=self.config.get('redirect_uri', ''),
            client_id=self.config.get('client_id', ''),
            options=options,
            scope=self.config.get('auth_scope', ''),
        )

    def create_account_for_user(self, user, code):

        ''' Save new account info for a user. '''

        obj = self.get_wepay_object()
        token_response = obj.get_token(
            redirect_uri=self.config.get('redirect_uri', ''),
            client_id=self.config.get('client_id', ''),
            client_secret=self.config.get('client_secret', ''),
            code=code,
        )
        account = WePayUserPaymentAccount(
            user=user,
            wepay_user_id=token_response.get('user_id', ''),
            wepay_access_token=token_response.get('access_token', ''),
            wepay_token_expires=token_response.get('expires_in', None), # TODO: Convert format if needed?
        )
        account.put()
        return account

    def create_payment_account(self, name, description, wepay_account_id):

        ''' Create a payment account for a wepay account. '''

        # Get the access_token for this account ID.
        # TODO: Generate the key somehow instead of query/fetch?
        accounts = WePayUserPaymentAccount.query(WePayUserPaymentAccount.wepay_user_id == wepay_account_id).fetch()
        if not accounts and len(accounts):
            return None # TODO: Better errors.

        account = accounts[0]
        params = {
            'name': name,
            'description': description,
        }
        try:
            obj = self.get_wepay_object(access_token=account.wepay_access_token)
            response = obj.call('/account/create', params=params)
        except wepay_api.WePayError, e:
            return None # TODO: Better error with wepay re-auth url.
        return response['account_id']


    def save_cc_for_user(self, user, cc_info):

        ''' Create a credit card entity in WePay, link it to a user account, and authorize it. '''

        # Make the WePay API call.
        wepay_obj = self.get_wepay_object()
        response = wepay_obj.call('/credit_card/create', {
            'client_id': self.config.get('client_id', ''),
            'user_name': cc_info.user_name,
            'email': cc_info.email,
            'cc_number': cc_info.cc_num,
            'cvv': cc_info.ccv,
            'expiration_month': cc_info.expire_month,
            'expiration_year': cc_info.expire_year,
            'address': {
                'address1': cc_info.address1,
                'address2': cc_info.address2,
                'city': cc_info.city,
                'state': cc_info.state,
                'country': cc_info.country,
                'zip': cc_info.zipcode
            }
        })

        # Save the credit card object linked to the user.
        wepay_cc = WePayCreditCard(
            owner=user,
            description=cc_info.cc_num[:4],
            wepay_cc_id=response['credit_card_id'],
            wepay_cc_state=response['state'],
            save_for_reuse=cc_info.save_for_reuse,
        )
        wepay_cc.put()

        # Authorize the credit card since we are not going to charge it immediately.
        auth_response = wepay_obj.call('/credit_card/authorize', {
            'client_id': self.config.get('client_id', ''),
            'client_secret': self.config.get('client_secret', ''),
            'credit_card_id': wepay_cc.wepay_cc_id
        })
        if auth_response['state'] != wepay_cc.wepay_cc_state:
            wepay_cc.wepay_cc_state = auth_response['state']
            wepay_cc.put()

        return wepay_cc


    def execute_payments(self, payments):

        ''' Execute many payments at once using WePay. '''

        pass

    def refund_payments(self, payments):

        ''' Refund payments. '''

        pass


WePayAPI = CoreWePayAPI()
