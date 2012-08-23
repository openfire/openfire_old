from google.appengine.ext import ndb
from protorpc import remote
from openfire.messages import search
from openfire.services import RemoteService
from openfire.models.indexer.index import Index
from openfire.models.indexer.entry import IndexEntry


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

            ''' Generalized autocomplete. '''

            ids = []
            if request.index:
                query = IndexEntry.query(IndexEntry.substrings == request.query, ancestor = ndb.Key(Index, request.index))
            else:
                query = IndexEntry.query(IndexEntry.substrings == request.query)
            for key in query.iter(keys_only=True):
                ids.append(key.id())
            return search.SearchResponse(ids=ids)
