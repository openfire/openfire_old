# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from google.appengine.api import mail

from openfire.pipelines.primitive import TransportPipeline


## MailPipeline - abstract parent for all Mail API-related pipelines
class MailPipeline(TransportPipeline):

    ''' Abstract parent class for low-level mail pipelines. '''

    pass


## SendEmail - sends an email via the AppEngine Mail API
class SendEmail(MailPipeline):

    ''' Sends an email via the App Engine Mail API. '''

    def run(self, sender, to, subject, body, **kwargs):

		''' Pass through to mail.send_mail. '''

		return mail.send_mail(sender, to, subject, body, **kwargs)


## SendAdminsEmail - sends an email to all openfire admins
class SendAdminsEmail(MailPipeline):

	''' Sends an email to an administrative address. '''

	def run(self, sender, subject, body, **kwargs):

		''' Pass through to mail.send_mail_to_admins. '''

		return mail.send_mail_to_admins(sender, subject, body, **kwargs)


## IncomingEmail - fired when an email is received by openfire
class IncomingEmail(MailPipeline):

    ''' Fired when an email is received. '''

    def run(self, **kwargs):

		''' Process email. '''

		pass
