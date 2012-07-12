# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel


## EmailBody - represents a section of an email body, either in plaintext or HTML
class EmailBody(ndb.Model):

    ''' Tiny, embedded entity for denoting email bodies. '''

    content_type = ndb.StringProperty('ct', default='text/plain', indexed=True)
    content = ndb.TextProperty('c', required=True)


## EmailHeader - a key=>value header mapping on an email
class EmailHeader(ndb.Model):

    ''' Tiny, embedded entity for a key=>value email header mapping. '''

    key = ndb.StringProperty('k', required=True)
    value = ndb.StringProperty('v', required=True)


## OutgoingEmail - created for each email sent from openfire
class OutgoingEmail(AppModel):

    ''' Represents a queued (and possibly, sent) outgoing email. '''

    queued = ndb.BooleanProperty('q', default=False)
    subject = ndb.StringProperty('su')
    sender = ndb.StringProperty('se')
    to = ndb.StringProperty('to', repeated=True)
    cc = ndb.StringProperty('cc', repeated=True)
    sent = ndb.DateTimeProperty('dt')
    attachments = ndb.BlobKeyProperty('at', repeated=True)
    original = ndb.BlobProperty('or', required=True, compressed=True)
    has_html = ndb.BooleanProperty('ht', default=False)
    has_text = ndb.BooleanProperty('tx', default=True)
    body = ndb.LocalStructuredProperty(EmailBody, 'b', repeated=True, compressed=True)
    headers = ndb.LocalStructuredProperty(EmailHeader, 'h', repeated=True, compressed=True)


## IncomingEmail - created for each email received by openfire
class IncomingEmail(AppModel):

    ''' Represents a queued (and possibly, processed) incoming email. '''

    subject = ndb.StringProperty('su')
    sender = ndb.StringProperty('se')
    to = ndb.StringProperty('to', repeated=True)
    cc = ndb.StringProperty('cc', repeated=True)
    attachments = ndb.BlobKeyProperty('at', repeated=True)
    original = ndb.BlobProperty('or', required=True, compressed=True)
    has_html = ndb.BooleanProperty('ht', default=False)
    has_text = ndb.BooleanProperty('tx', default=True)
    body = ndb.LocalStructuredProperty(EmailBody, 'b', repeated=True, compressed=True)
    headers = ndb.LocalStructuredProperty(EmailHeader, 'h', repeated=True, compressed=True)
