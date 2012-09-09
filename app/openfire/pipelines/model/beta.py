# -*- coding: utf-8 -*-

## Base Imports
import config
import webapp2

## Debugging
from apptools.util import debug

## Pipeline Imports
from openfire.pipelines.model import ModelPipeline
from openfire.pipelines.integration import mailchimp
from openfire.pipelines.primitive.transport import mail


## BetaSignupPipeline - fired when a put or delete event is dispatched for a Signup entity
class BetaSignupPipeline(ModelPipeline):

    ''' Processes signup puts/deletes. '''

    _model_binding = 'openfire.models.beta.Signup'

    @webapp2.cached_property
    def config(self):

        ''' Named config pipe. '''

        return config.config.get('openfire.placeholder').get('signup')

    @webapp2.cached_property
    def logging(self):

        ''' Named logging pipe. '''

        return debug.AppToolsLogger(path='openfire.pipelines.model.beta', name='BetaSignupPipeline')._setcondition(self.config.get('debug', True))

    def put(self, key, model):

        ''' Send a welcome email to the newly-signed-up user, and kick the user's email over to MailChimp. '''

        self.logging.info('Processing beta signup for email "%s" and token "%s".' % (model.email, model.token))

        ## Pipelines to trigger
        actions = []

        ## Pull config for the beta_welcome notification
        email_cfg = config.config.get('openfire.notifications').get('transports').get('email')
        beta_welcome_cfg = config.config.get('openfire.notifications').get('index').get('beta_welcome')

        ## Send welcome email, if enabled
        if email_cfg.get('enable', False):
            self.logging.info('Email notifications enabled. Sending beta welcome.')
            actions.append(mail.SendMail(**{

                'to': model.email,
                'sender': beta_welcome_cfg.get('sender', email_cfg.get('sender')),
                'subject': beta_welcome_cfg.get('subject'),
                'body': self.render('notifications/beta_welcome.html', signup=model)

            }))

        ## Add to MailChimp, if enabled
        if self.config.get('mailchimp', {}).get('enabled', False):
            self.logging.info('MailChimp integration enabled. Adding user to beta list.')
            actions.append(mailchimp.MailChimpEmailEntry(self.config.get('mailchimp').get('apikey'), **{
                'id': self.config.get('mailchimp').get('listid'),
                'email_address': model.email,
                'email_type': model.email_type,
                'send_welcome': False,
                'double_optin': False,
                'merge_vars': {
                    'FNAME': model.firstname,
                    'LNAME': model.lastname
                }
            }))

        if len(actions) > 0:
            self.logging.info('Running %s result pipelines.' % str(len(actions)))
            started = yield actions
