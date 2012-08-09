from google.appengine.ext import ndb
from apptools.services.builtin import Echo
from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.messages import common as common_messages
from openfire.models.user import Topic


class TopicService(RemoteService):

    ''' Topic service api. '''

    @remote.method(common_messages.TopicRequest, common_messages.Topic)
    def get(self, request):

        ''' Get a single topic. '''

        topic_key = ndb.Key('Topic', request.slug)
        topic = topic_key.get()
        return topic.to_message()


    @remote.method(message_types.VoidMessage, common_messages.Topics)
    def list(self, request):

        ''' Return a list of topics. '''

        topics = Topic.query().fetch()
        messages = []
        for topic in topics:
            messages.append(topic.to_message())
        return common_messages.Topics(topics=messages)


    @remote.method(common_messages.Topic, common_messages.Topic)
    def put(self, request):

        ''' Create or edit a topic. '''

        if not request.key:
            # Create a new topic.
            topic = Topic(key=ndb.Key('Topic', request.slug))
        else:
            # Get the topic to edit.
            topic_key = ndb.Key(urlsafe=self.decrypt(request.key))
            topic = topic_key.get()

        if not topic:
            # Return blank on error.
            return common_messages.Topic()

        # Update the topic.
        topic.mutate_from_message(request)
        topic.put()

        return topic.to_message()


    @remote.method(common_messages.TopicRequest, Echo)
    def delete(self, request):

        ''' Remove a topic. '''

        topic_key = ndb.Key(urlsafe=self.decrypt(request.key))
        topic_key.delete()
        return Echo(message='Topic removed')
