# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel

from openfire.messages import common as messages
from openfire.pipelines.model import social as pipelines


######## ======== Abstract Social Models ======== ########

## Comment - abstract model for a text-based comment left on a site datapoint by a user
class Comment(AppModel):

    ''' Represents a comment made by a user on some site object. '''

    _message_class = messages.Comment
    _pipeline_class = pipelines.CommentPipeline

    user = ndb.KeyProperty('u', indexed=True, required=True)
    content = ndb.StringProperty('c', indexed=True, required=True)
    reply_to = ndb.KeyProperty('r', indexed=True, default=None)
    subject = ndb.KeyProperty('s', indexed=True)


## Follow - abstract model for a request to subscribe to a site datapoint, added by a user
class Follow(AppModel):

    ''' Describes a user's desire to follow some site object. '''

    _message_class = messages.Follow
    _pipeline_class = pipelines.FollowPipeline

    class NotificationOptions(AppModel):

	    ''' Describes notification options. '''

	    frequency = ndb.StringProperty(choices=['REALTIME', 'DAILY', 'WEEKLY'], default=['REALTIME'])
	    transport = ndb.StringProperty(choices=['EMAIL', 'XMPP', 'TEXT'], default=['EMAIL'], repeated=True)

    user = ndb.KeyProperty('u', indexed=True, required=True)
    subject = ndb.KeyProperty('sj', indexed=True, required=True)
    subscription = ndb.KeyProperty('sb', indexed=True, required=True)
    options = ndb.LocalStructuredProperty(NotificationOptions, compressed=True)
