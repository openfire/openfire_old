
class WePayAPI(object):

    ''' A shim to all WePay API functionality for openfire. '''

    def create_account_for_user(self, user):

        ''' Attempt to create a WePay account for a user, and fall back to a url on error. '''

        pass

    def add_cc_to_account(self):

        ''' Create a credit card entity in WePay and link it to a user account. '''

        pass

    def execute_payments(self, payments):

        ''' Execute many payments at once using WePay. '''

        pass

    def refund_payments(self, payments):

        ''' Refund payments. '''

        pass
