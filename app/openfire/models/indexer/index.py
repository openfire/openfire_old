# -*- coding: utf-8 -*-
from webapp2 import import_string
from openfire.models.indexer import IndexerModel

from openfire.models.indexer.entry import IndexEntry


######## ======== Index Structure ======== ########

## Index - container for index entries, collects special indexes and global indexes
class Index(IndexerModel):

    ''' A container for traversible index entries. '''

    # Naming/Basic Info
    name = ndb.StringProperty('n', indexed=True)
    description = ndb.StringProperty('d', indexed=False)

    # Attachment Info
    model_base = ndb.StringProperty('m', default='openire.models.AppModel', indexed=True)

	# Entry Info    
    entry_count = ndb.IntegerProperty('ec', default=0, indexed=True)
    entry_base = ndb.StringProperty('eb', default='openfire.models.indexer.entry.IndexEntry', indexed=True)
    entry_kind = ndb.StringProperty('ek', repeated=True, indexed=True)

    @classmethod
    def new(cls, name, **kwargs):

        ''' Factory method to create a new Index. '''

        return cls(id=name, name=name, **kwargs)

    def add(self, value, entry=IndexEntry, **kwargs):

        ''' Shortcut factory method to add an IndexEntry to an index. '''

        return entry.new(self, value, **kwargs)


######## ======== Index Mutations ======== ########

## IndexEvent - generated for our index audit log
class IndexEvent(IndexerModel):

    ''' An event performed by the indexer, like rebuilding/optimizing/creating indexes. '''

    pass


## IndexMutation - a set of mutations applied, as part of an IndexEvent
class IndexMutation(IndexerModel):

    ''' A mutation event on the mapping/entry/index, built as part of an index event. '''

    pass
