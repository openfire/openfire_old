from protorpc import remote
from openfire.messages import search
from openfire.services import RemoteService


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

		return search.SearchResponse()
