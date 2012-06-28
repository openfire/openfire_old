# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel


## Activity - a single activity item, generated from an action entity
class Activity(AppModel):

    ''' Represents a single materialized site activity item. '''

    pass


## ActivityStream - a collection of Activity items that are globally visible for a certain period of time
class ActivityStream(AppModel):

    ''' Represents a materialized activity stream for sitewide content. '''

    pass
