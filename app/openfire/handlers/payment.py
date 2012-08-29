# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.handlers import WebHandler
from openfire.core.payment import PaymentAPI


class PaymentHandler(WebHandler):

    ''' openfire payment handler. '''

    def get(self):

        ''' Handle WePay responses. '''

        code = self.request.GET.get('code', None)
        state = self.request.GET.get('state', None)
        if not state:
            self.logging.error('Failed to get any state from the wepay redirect.')
            return self.redirect('/me')

        user_key = ndb.Key(urlsafe=state)
        user = user_key.get()
        if not user:
            self.logging.error('Failed to decode and find user key for state "%s" during wepay oauth.' % state)

        account = PaymentAPI.create_user_payment_account(user, code)
        if not account:
            self.logging.error('Failed to wepay user payment account in oauth callback handler.')

        return self.redirect('/me')
