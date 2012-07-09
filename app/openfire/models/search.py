# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel

# Model Attachments
from openfire.messages import search as messages
from openfire.pipelines.model import search as pipelines


######## ======== Search Tracking ======== ########

## UserSearch - stored for each search a user performs
class UserSearch(AppModel):

    ''' Tracks a user search. '''

    _message_class = messages.Search
    _pipeline_class = pipelines.UserSearchPipeline

    pass


## SearchKeyword - stored for each keyword in each search performed, for the purpose of collecting stats
class SearchKeyword(AppModel):

    ''' Represents a single search keyword, that has a history of being entered by a user in a query at least once. '''

    _message_class = messages.Keyword
    _pipeline_class = pipelines.SearchKeywordPipeline

    pass


## SearchResults - a stored set of search results returned & by the system
class SearchResults(AppModel):

    ''' Represents a set of search results served to a user. '''

    _message_class = messages.SearchResults
    _pipeline_class = pipelines.SearchResultsPipeline

    pass
