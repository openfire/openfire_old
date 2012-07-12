# -*- coding: utf-8 -*-
import logging
import datetime

from google.appengine.api import channel
from openfire.models.transport import channel as models
from openfire.pipelines.primitive import TransportPipeline


## ChannelPipeline - parent to all Channel API-related pipelines
class ChannelPipeline(TransportPipeline):

    ''' Abstract parent class for low-level channel pipelines. '''

    api = channel


## ChannelConnect - fired when a channel is connected
class ChannelConnect(ChannelPipeline):

    ''' Fired when a channel is connected. '''

    def run(self, client_id):

        ''' Tracks a new channel connection. '''

        push_channel = models.PushChannel.query().filter(models.PushChannel.client_id == client_id).get(limit=1)
        if push_channel is None:
            logging.error('Failed to update PushChannel record with CONNECTED status because it could not be found.')
            return False
        else:
            push_channel.live = True
            push_channel.connected = datetime.datetime.now()
            return push_channel.put().urlsafe()


## ChannelDisconnect - fired when a channel is disconnected
class ChannelDisconnect(ChannelPipeline):

    ''' Fired when a channel is disconnected. '''

    def run(self, client_id):

        ''' Updates a connection as 'disconnected. '''

        push_channel = models.PushChannel.query().filter(models.PushChannel.client_id == client_id).get(limit=1)
        if push_channel is None:
            logging.error('Failed to update PushChannel record with CONNECTED status because it could not be found.')
            return False
        else:
            push_channel.live = False
            push_channel.disconnected = datetime.datetime.now()
            return push_channel.put().urlsafe()


## ChannelPush - pushes a message to a connected client
class ChannelPush(ChannelPipeline):

    ''' Push a channel message to a client. '''

    def run(self, client_id, message):

        ''' Pushes a message to a connected push channel. '''

        return self.api.send_message(client_id, message)
