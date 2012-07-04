# -*- coding: utf-8 -*-
from google.appengine.api import channel
from openfire.pipelines.primitive import TransportPipeline


## ChannelPipeline - parent to all Channel API-related pipelines
class ChannelPipeline(TransportPipeline):

    ''' Abstract parent class for low-level channel pipelines. '''

    pass


## ChannelConnect - fired when a channel is connected
class ChannelConnect(ChannelPipeline):

    ''' Fired when a channel is connected. '''

    pass


## ChannelDisconnect - fired when a channel is disconnected
class ChannelDisconnect(ChannelPipeline):

    ''' Fired when a channel is disconnected. '''

    pass


## ChannelPush - pushes a message to a connected client
class ChannelPush(ChannelPipeline):

    ''' Push a channel message to a client. '''

    pass
