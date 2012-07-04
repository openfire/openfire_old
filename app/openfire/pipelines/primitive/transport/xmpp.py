# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import TransportPipeline


## XMPPPipeline - parent to all XMPP API-related pipelines
class XMPPPipeline(TransportPipeline):

    ''' Abstract parent class for low-level XMPP/Jabber pipelines. '''

    pass


## XMPPError - fires when an error is reported by the XMPP API
class XMPPError(XMPPPipeline):

    ''' Handle an XMPP error notification. '''

    pass


## SendXMPP - send an XMPP message to the given jabber ID
class SendXMPP(XMPPPipeline):

    ''' Send an XMPP message. '''

    pass


## ReceiveXMPP - process an incoming XMPP message
class ReceiveXMPP(XMPPPipeline):

    ''' Process an incoming XMPP message. '''

    pass


## SubscribeXMPP - subscribe a JID via XMPP
class SubscribeXMPP(XMPPPipeline):

    ''' Process an incoming XMPP subscription routine. '''

    pass


## UnSubscribeXMPP - unsubscribe a JID via XMPP
class UnSubscribeXMPP(XMPPPipeline):

    ''' Process an incoming XMPP unsubscription routine. '''

    pass


## PresenceXMPP - process an incoming XMPP presence notification
class PresenceXMPP(XMPPPipeline):

    ''' Process an incoming XMPP presence routine. '''

    pass
