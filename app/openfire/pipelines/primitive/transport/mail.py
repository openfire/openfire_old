# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import TransportPipeline


class MailPipeline(TransportPipeline):

    ''' Abstract parent class for low-level mail pipelines. '''

    pass


class SendEmail(MailPipeline):

    ''' Sends an email via the App Engine Mail API. '''

    pass


class IncomingEmail(MailPipeline):

    ''' Fired when an email is received. '''

    pass
