# -*- coding: utf-8 -*-
from openfire.pipelines.model import ModelPipeline


## UserSearchPipeline - fired when a UserSearch entity is put/deleted
class UserSearchPipeline(ModelPipeline):

    ''' Processes user search puts/deletes. '''

    _model_binding = 'openfire.models.search.UserSearch'


## SearchKeywordPipeline - fired when a SearchKeyword entity is put/deleted
class SearchKeywordPipeline(ModelPipeline):

    ''' Processes search keyword puts/deletes. '''

    _model_binding = 'openfire.models.search.SearchKeyword'


## SearchResultsPipeline - fired when a SearchResults entity is put/deleted
class SearchResultsPipeline(ModelPipeline):

    ''' Processes search result puts/deletes. '''

    _model_binding = 'openfire.models.search.SearchResults'
