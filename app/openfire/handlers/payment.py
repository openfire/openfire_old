# -*- coding: utf-8 -*-
from openfire.handlers import WebHandler


class PaymentHandler(WebHandler):

    ''' openfire payment handler. '''

    def get(self):

        ''' Handle WePay responses. '''

        return self.response.write('coming soon')
