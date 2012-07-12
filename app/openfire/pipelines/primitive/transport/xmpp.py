# -*- coding: utf-8 -*-
from google.appengine.api import xmpp

from openfire.models.transport import xmpp as models
from openfire.pipelines.primitive import TransportPipeline


## XMPPPipeline - parent to all XMPP API-related pipelines
class XMPPPipeline(TransportPipeline):

    ''' Abstract parent class for low-level XMPP/Jabber pipelines. '''

    api = xmpp


## XMPPError - fires when an error is reported by the XMPP API
class XMPPError(XMPPPipeline):

    ''' Handle an XMPP error notification. '''

    def run(self, sender, stanza):

        ''' Document the error. '''

        return models.XMPPError(sender=sender, stanza=stanza).put().urlsafe()


## SendXMPP - send an XMPP message to the given jabber ID
class SendXMPPMessage(XMPPPipeline):

    ''' Send an XMPP message. '''

    def run(self, *args, **kwargs):

        ''' Sends an XMPP message. '''

        return self.api.send_message(*args, **kwargs)


## SendXMPP - send an XMPP message to the given jabber ID
class SendXMPPInvite(XMPPPipeline):

    ''' Send an XMPP message. '''

    def run(self, jid, from_jid=None):

        ''' Sends an XMPP message. '''

        return self.api.send_invite(jid, from_jid)


## GetPresenceXMPP - get another JID's presence
class GetPresenceXMPP(XMPPPipeline):

    ''' Get an XMPP JID's presence. '''

    def run(self, jid, from_jid=None, get_show=None):

        ''' Get a JID's presence. '''

        return self.api.get_presence(jid, from_jid, get_show)


## SendPresenceXMPP - send an openfire JID's presence
class SendPresenceXMPP(XMPPPipeline):

    ''' Send an openfire JID's presence to another JID. '''

    def run(self, *args, **kwargs):

        ''' Send an openfire JID's presence. '''

        return self.api.send_presence(*args, **kwargs)


## ReceiveXMPP - process an incoming XMPP message
class ReceiveXMPP(XMPPPipeline):

    ''' Process an incoming XMPP message. '''

    def run(self, to, sender, body, stanza=None, message_type='normal', raw_xml=False):

        ''' Process an incoming XMPP message. '''

        ## resolve channel or create
        channel = models.XMPPChannel.get_by_id(sender)
        if channel is not None:
            channel = channel.key

        return models.XMPPMessage(**{

            'direction': 'inbound',
            'jid': to,
            'channel': channel,
            'from_jid': sender,
            'message_type': message_type,
            'body': body,
            'stanza': stanza,
            'raw_xml': raw_xml

        })


## SubscribeXMPP - subscribe a JID via XMPP
class SubscribeXMPP(XMPPPipeline):

    ''' Process an incoming XMPP subscription routine. '''

    def run(self):

        ''' Process an incoming subscribe request. '''

        raise NotImplemented  # not needed yet (@TODO)


## UnSubscribeXMPP - unsubscribe a JID via XMPP
class UnSubscribeXMPP(XMPPPipeline):

    ''' Process an incoming XMPP unsubscription routine. '''

    def run(self):

        ''' Process an incoming unsubscribe request. '''

        raise NotImplemented  # not needed yet (@TODO)
