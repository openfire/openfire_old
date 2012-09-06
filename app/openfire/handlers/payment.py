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


class WePayIPNHandler(WebHandler):

    ''' A hander dedicated to the WePay IPN system. '''

    def _process_wepay_update(self, checkout_id, withdrawal_id):

        ''' Common method to process the checkout or withdrawal id. '''

        if checkout_id:
            return PaymentAPI.payment_updated(int(checkout_id))
        if withdrawal_id:
            return PaymentAPI.withdrawal_updated(int(withdrawal_id))
        return None

    def post(self):

        ''' Handle WePay IPN posts to update a checkout or withdrawal. '''

        checkout_id = self.request.POST.get('checkout_id', None)
        withdrawal_id = self.request.POST.get('withdrawal_id', None)
        self._process_wepay_update(checkout_id, withdrawal_id)
        return self.redirect('/')

    def get(self):

        ''' Fake WePay IPN posts with a get url for dev purposes. '''

        checkout_id = self.request.GET.get('checkout_id', None)
        withdrawal_id = self.request.GET.get('withdrawal_id', None)
        self._process_wepay_update(checkout_id, withdrawal_id)
        return self.redirect('/')
