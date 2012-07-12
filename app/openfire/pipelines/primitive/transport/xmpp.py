# -*- coding: utf-8 -*-
from google.appengine.api import xmpp
from openfire.pipelines.primitive import TransportPipeline


## XMPPPipeline - parent to all XMPP API-related pipelines
class XMPPPipeline(TransportPipeline):

    ''' Abstract parent class for low-level XMPP/Jabber pipelines. '''

    api = xmpp


## XMPPError - fires when an error is reported by the XMPP API
class XMPPError(XMPPPipeline):

    ''' Handle an XMPP error notification. '''

    def run(self):

        ''' Document the error. '''

        pass


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

    def run(self):

        ''' Process an incoming XMPP message. '''

        pass


## SubscribeXMPP - subscribe a JID via XMPP
class SubscribeXMPP(XMPPPipeline):

    ''' Process an incoming XMPP subscription routine. '''

    def run(self):

        ''' Process an incoming subscribe request. '''

        pass


## UnSubscribeXMPP - unsubscribe a JID via XMPP
class UnSubscribeXMPP(XMPPPipeline):

    ''' Process an incoming XMPP unsubscription routine. '''

    def run(self):

        ''' Process an incoming unsubscribe request. '''

        pass
