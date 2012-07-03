from protorpc import messages


#### ++++ Object Messages ++++ ####
class Keyword(messages.Message):

    ''' A keyword in a search query. '''

    pass


class Filter(messages.Message):

    ''' A filter directive in a search query. '''

    pass


class Sort(messages.Message):

    ''' A sort directive in a search query. '''

    pass


class Search(messages.Message):

    ''' Represents a user search. '''

    pass


class SearchResult(messages.Message):

    ''' A single search result. '''

    pass


class SearchResults(messages.Message):

    ''' A set of search results. '''

    pass


#### ++++ Request Messages ++++ ####
class QuickSearchRequest(messages.Message):

    ''' A request for simple, fuzzy, keyword-based quicksearch. '''

    pass


class AdvancedSearchRequest(messages.Message):

    ''' A request for advanced, filter/sort-based fulltext search. '''

    pass


class AutocompleteRequest(messages.Message):

    ''' A request for autocomplete. '''

    pass


#### ++++ Response Messages ++++ ####
class SearchResponse(messages.Message):

    ''' Response to a search query. '''

    pass
