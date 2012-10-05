# -*- coding: utf-8 -*-
import webapp2
from config import config
from mailsnake import MailSnake
from openfire.pipelines import AppPipeline


## MailChimpEmailEntry - fired when an email address must be added to a MailChimp list
class MailChimpEmailEntry(AppPipeline):

    ''' Adds an email to a list in MailChimp. '''

    @webapp2.cached_property
    def config(self):

        ''' Named config pipe. '''

        return config.get('openfire.notifications').get('transports').get('email')

    @webapp2.cached_property
    def debug(self):

        ''' Named debug flag. '''

        return config.get('openfire.pipelines.integration.mailchimp.MailChimpEmailEntry').get('debug', True)

    @webapp2.cached_property
    def logging(self):

        ''' Named logging pipe. '''

        return debug.AppToolsLogger(path='openfire.pipelines.integration.mailchimp', name='MailChimpEmailEntry')._setcondition(self.debug)

    def run(self, apikey, **kwargs):

        ''' Connect to mailchimp and send over a new email to add. '''

        self.logging.info
        api_client = MailSnake(apikey)
        result = api_client.listSubscribe(**kwargs)
        return result
