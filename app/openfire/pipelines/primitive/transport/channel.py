# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import TransportPipeline


class ChannelPipeline(TransportPipeline):

    ''' Abstract parent class for low-level channel pipelines. '''

    pass


class ChannelConnect(ChannelPipeline):

    ''' Fired when a channel is connected. '''

    pass


class ChannelDisconnect(ChannelPipeline):

    ''' Fired when a channel is disconnected. '''

    pass


class ChannelPush(ChannelPipeline):

    ''' Push a channel message to a client. '''

    pass
