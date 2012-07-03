# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import TransportPipeline


class XMPPPipeline(TransportPipeline):

    ''' Abstract parent class for low-level XMPP/Jabber pipelines. '''

    pass


class XMPPError(XMPPPipeline):

    ''' Handle an XMPP error notification. '''

    pass


class SendXMPP(XMPPPipeline):

    ''' Send an XMPP message. '''

    pass


class ReceiveXMPP(XMPPPipeline):

    ''' Process an incoming XMPP message. '''

    pass


class SubscribeXMPP(XMPPPipeline):

    ''' Process an incoming XMPP subscription routine. '''

    pass


class PresenceXMPP(XMPPPipeline):

    ''' Process an incoming XMPP presence routine. '''

    pass
