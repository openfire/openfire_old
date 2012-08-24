from google.appengine.ext import ndb
from protorpc import remote
from openfire.messages import search, common
from openfire.services import RemoteService
from openfire.models.indexer.index import Index
from openfire.models.indexer.entry import IndexEntry
from openfire.models.user import Topic


class SearchService(RemoteService):

    ''' Remote service for searching openfire data. '''

    @remote.method(search.QuickSearchRequest, search.SearchResponse)
    def quick(self, request):

        ''' Quick, fuzzy, keyword-based fulltext/universal search. '''

        return search.SearchResponse()

    @remote.method(search.AdvancedSearchRequest, search.SearchResponse)
    def advanced(self, request):

        ''' Advanced, filter/sort-based fulltext/universal search. '''

        return search.SearchResponse()

    @remote.method(search.AutocompleteRequest, search.SearchResponse)
    def autocomplete(self, request):

        ''' Generalized autocomplete. Returns ids of keys. '''

        ids = []
        if request.index:
            query = IndexEntry.query(IndexEntry.substrings == request.query, ancestor = ndb.Key(Index, request.index))
        else:
            query = IndexEntry.query(IndexEntry.substrings == request.query)
        for key in query.iter(keys_only=True):
            ids.append(key.id())
        return search.SearchResponse(ids=ids)

    @remote.method(search.AutocompleteRequest, common.Topics)
    def topic_autocomplete(self, request):

        ''' Topic specific autocomplete. '''

        topics = []
        query = IndexEntry.query(IndexEntry.substrings == request.query, ancestor = ndb.Key(Index, 'topic'))
        topic_keys = [ndb.Key(Topic, k.id()) for k in query.iter(keys_only=True)]
        for topic in ndb.get_multi(topic_keys):
            topics.append(topic.to_message())
        return common.Topics(topics=topics)
