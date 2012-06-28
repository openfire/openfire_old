# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel


######## ======== Search Tracking ======== ########

## UserSearch - stored for each search a user performs
class UserSearch(AppModel):

    ''' Tracks a user search. '''

    pass


## SearchKeyword - stored for each keyword in each search performed, for the purpose of collecting stats
class SearchKeyword(AppModel):

    ''' Represents a single search keyword, that has a history of being entered by a user in a query at least once. '''

    pass


## SearchResults - a stored set of search results returned & by the system
class SearchResults(AppModel):

    ''' Represents a set of search results served to a user. '''

    pass
