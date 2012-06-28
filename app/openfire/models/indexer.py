# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel


######## ======== Index Structure ======== ########

## Index - container for index entries, collects special indexes and global indexes
class Index(AppModel):

    ''' A container for traversible index entries. '''

    pass


## IndexEntry - hierarchical stop for *values* in the index
class IndexEntry(AppModel):

    ''' A value entry in the index. '''

    pass


######## ======== Index Mutations ======== ########

## IndexMapping - the bottom level of the index tree - mappings from an entry to keys
class IndexMapping(AppModel):

    ''' A mapping: entry => key. '''

    pass


## IndexEvent - generated for our index audit log
class IndexEvent(AppModel):

    ''' An event performed by the indexer, like rebuilding/optimizing/creating indexes. '''

    pass


## IndexMutation - a set of mutations applied, as part of an IndexEvent
class IndexMutation(AppModel):

    ''' A mutation event on the mapping/entry/index, built as part of an index event. '''

    pass
