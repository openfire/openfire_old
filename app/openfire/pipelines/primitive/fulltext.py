# -*- coding: utf-8 -*-
from google.appengine.api import search
from openfire.pipelines import AppPipeline


## FulltextPipeline - parent to all fulltext-related pipelines
class FulltextPipeline(AppPipeline):

    ''' Abstract parent class for low-level fulltext pipelines. '''

    api = search


## ListIndexes
class ListIndexes(FulltextPipeline):

    ''' List available fulltext search indexes for a given (and possibly empty) namespace. '''

    def run(self, *args, **kwargs):

        return self.api.list_indexes(*args, **kwargs)


## NewDocument
class NewDocument(FulltextPipeline):

    ''' Create a new document and add it to an index, creating the index if it does not exist. '''

    def run(self, *args, **kwargs):

        raise NotImplemented  # @TODO


## ListDocuments
class ListDocuments(FulltextPipeline):

    ''' List available documents in an index. '''

    def run(self, index_name, *args, **kwargs):

        return self.api.Index(index_name).list_documents(*args, **kwargs)


## Search
class Search(FulltextPipeline):

    ''' Perform a fulltext search. '''

    def run(self, *args, **kwargs):

        raise NotImplemented  # @TODO
