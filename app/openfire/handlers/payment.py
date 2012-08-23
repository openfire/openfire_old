# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.handlers import WebHandler
from openfire.core.payment.wepay import WePayAPI


class PaymentHandler(WebHandler):

    ''' openfire payment handler. '''

    def post(self, code, state):

        ''' Handle WePay responses. '''

        user_key = ndb.Key(urlsafe=state)
        user = user_key.get()
        if not user:
            self.logging.error('Failed to decode and find user key for state "%s" during wepay oauth.' % state)

        account = WePayAPI.create_user_payment_account(user, code)
        if not account:
            self.logging.error('Failed to wepay user payment account in oauth callback handler.')

        return self.redirect('/me')
