# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel

# Model Attachments
from openfire.messages import activity as messages
from openfire.pipelines.model import activity as pipelines


## Activity - a single activity item, generated from an action entity
class Activity(AppModel):

    ''' Represents a single materialized site activity item. '''

    _message_class = messages.Activity
    _pipeline_class = pipelines.ActivityPipeline

    pass


## ActivityStream - a collection of Activity items that are globally visible for a certain period of time
class ActivityStream(AppModel):

    ''' Represents a materialized activity stream for sitewide content. '''

    _message_class = messages.ActivityStream
    _pipeline_class = pipelines.ActivityStreamPipeline

    pass
