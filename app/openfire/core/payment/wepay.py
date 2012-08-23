import config
from openfire.core.payment import wepay_api
from openfire.models.payment import WePayUserPaymentAccount

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
            response = obj.call('/account/create/', params=params)
        except wepay_api.WePayError, e:
            return None # TODO: Better error with wepay re-auth url.
        return response['account_id']


    def add_cc_to_account(self):

        ''' Create a credit card entity in WePay and link it to a user account. '''

        pass

    def execute_payments(self, payments):

        ''' Execute many payments at once using WePay. '''

        pass

    def refund_payments(self, payments):

        ''' Refund payments. '''

        pass


WePayAPI = CoreWePayAPI()
