# -*- coding: utf-8 -*-
import datetime
from google.appengine.ext import ndb
from google.appengine.api import mail

from openfire.models.transport import mail as models
from openfire.pipelines.primitive import TransportPipeline


## MailPipeline - abstract parent for all Mail API-related pipelines
class MailPipeline(TransportPipeline):

    ''' Abstract parent class for low-level mail pipelines. '''

    api = mail


## SendEmail - sends an email via the AppEngine Mail API
class SendEmail(MailPipeline):

    ''' Sends an email via the App Engine Mail API. '''

    def run(self, sender, to, subject, body, **kwargs):

        ''' Pass through to mail.send_mail. '''

        return self.api.send_mail(sender, to, subject, body, **kwargs)


## SendAdminsEmail - sends an email to all openfire admins
class SendAdminsEmail(MailPipeline):

    ''' Sends an email to an administrative address. '''

    def run(self, sender, subject, body, **kwargs):

        ''' Pass through to mail.send_mail_to_admins. '''

        return self.api.send_mail_to_admins(sender, subject, body, **kwargs)


## IncomingEmail - fired when an email is received by openfire
class IncomingEmail(MailPipeline):

    ''' Fired when an email is received. '''

    def run(self, sender, to, subject, body, cc=[], bcc=[], reply_to=None, html=None, attachments=[], headers={}):

        ''' Process an incoming email. '''

        ## validate email address
        if self.api.check_valid_email(to, 'to') and self.api.check_valid_email(sender, 'sender'):

            ## validate cc
            if cc and len(cc) > 0:
                cc = [email for email in cc if self.api.check_valid_email(email, 'cc')]

            ## validate bcc
            if bcc and len(bcc) > 0:
                bcc = [email for email in bcc if self.api.check_valid_email(email, 'bcc')]

            ## check reply-to
            if reply_to:
                if not self.api.is_email_valid(reply_to):
                    reply_to = sender

            ## package message headers
            message_headers = []
            if len(headers) > 0:
                for key, value in headers.items():
                    message_headers.append(models.EmailHeader(key=key, value=value))

            ## generate message bodies
            message_bodies = []
            if body:
                message_bodies.append(models.EmailBody(content_type='text/plain', content=body))
            if html:
                message_bodies.append(models.EmailBody(content_type='text/html', content=html))

            return models.IncomingEmail(**{

                'subject': subject,
                'sender': sender,
                'to': to,
                'cc': cc,
                'attachments': attachments,
                'original': body,
                'has_text': body is not None,
                'has_html': html is not None,
                'body': message_bodies,
                'headers': message_headers

            }).put().urlsafe()
