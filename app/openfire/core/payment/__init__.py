from openfire.core.payment.wepay import WePayAPI
from openfire.models.payment import Payment, ProjectAccount, WePayProjectAccount

class CorePaymentAPI(object):

    ''' A core API for payments. '''

    def _calculate_commission(self, amount):

        ''' Calculate how much commission openfire should take from a particular pledge. '''

        # TODO
        return 1

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

    def account_for_project_key(self, project_key):

        ''' Return the payment account for the given project key, or none. '''

        # TODO: Make it so that the id of the payment account key is the urlsafe key of the project.
        return None

    def save_user_cc(self, user, cc_info):

        ''' Adds a credit card money source to a user. '''

        return WePayAPI.save_cc_for_user(user, cc_info)

    def back_project(self, project_key, tier_key, amount, money_source):

        ''' Create a payment that records the contribution amount that will be charged if the project ignites. '''

        description = 'todo: make description'
        payment = Payment(
            amount=amount,
            commission=self._calculate_commission(amount),
            description=description,
            status='p',
            from_user=money_source.owner,
            from_money_source=money_source,
            to_project=project_key,
            to_account=self.account_for_project_key(project_key),
        )
        payment.put()
        return payment

    def charge_payments(self):

        ''' Charge many payments at once when a project goal is completed. '''

        pass

    def refund_payments(self, payments):

        ''' Refund payments. '''

        pass


# Payment API singleton.
PaymentAPI = CorePaymentAPI()
