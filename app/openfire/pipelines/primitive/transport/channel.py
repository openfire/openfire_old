# -*- coding: utf-8 -*-
from google.appengine.api import channel
from openfire.pipelines.primitive import TransportPipeline


## ChannelPipeline - parent to all Channel API-related pipelines
class ChannelPipeline(TransportPipeline):

    ''' Abstract parent class for low-level channel pipelines. '''

    api = channel


## ChannelConnect - fired when a channel is connected
class ChannelConnect(ChannelPipeline):

    ''' Fired when a channel is connected. '''

    def run(self):

        ''' Tracks a new channel connection. '''

        pass


## ChannelDisconnect - fired when a channel is disconnected
class ChannelDisconnect(ChannelPipeline):

    ''' Fired when a channel is disconnected. '''

    def run(self):

        ''' Updates a connection as 'disconnected. '''

        pass


## ChannelPush - pushes a message to a connected client
class ChannelPush(ChannelPipeline):

    ''' Push a channel message to a client. '''

    def run(self, client_id, message):

        ''' Pushes a message to a connected push channel. '''

        return self.api.send_message(client_id, message)
