from openfire.core.payment.wepay import WePayAPI
from openfire.models.payment import WePayProjectAccount

class CorePaymentAPI(object):

    ''' A core API for payments. '''

    def generate_auth_url(self, user):

        ''' Generate and return an auth url for openfire. '''

        return WePayAPI.generate_oauth_url(user)

    def create_user_payment_account(self, user, **kwargs):

        ''' Links an already created 3rd party account to an openfire user. '''

        return WePayAPI.create_account_for_user(user, **kwargs)

    def create_project_payment_account(self, project_key, name, description, wepay_account_id):

        ''' Create a sub account for a user to use to collect payments for a project. '''

        account_id = WePayAPI.create_payment_account(name, description, wepay_account_id)
        new_account = WePayProjectAccount(project=project_key, name=name, description=description, wepay_account_id=account_id)
        new_account.put()
        return new_account

    def add_payment_source(self):

        ''' Adds a payment source to a user. '''

        pass

    def charge_payments(self):

        ''' Charge many payments at once when a project goal is completed. '''

        pass

    def refund_payments(self, payments):

        ''' Refund payments. '''

        pass


# Payment API singleton.
PaymentAPI = CorePaymentAPI()
