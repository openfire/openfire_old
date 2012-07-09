# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models import AppModel


######## ======== Index Structure ======== ########

## Index - container for index entries, collects special indexes and global indexes
class Index(AppModel):

    ''' A container for traversible index entries. '''

    @classmethod
    def new(cls, name, **kwargs):

        ''' Factory method to create a new Index. '''

        return cls(id=name, **kwargs)

    def add(self, value, **kwargs):

        ''' Shortcut factory method to add an IndexEntry to an index. '''

        return IndexEntry.new(self, value, **kwargs)


## IndexEntry - hierarchical stop for *values* in the index
class IndexEntry(AppModel):

    ''' A value entry in the index. '''

    @classmethod
    def new(cls, index, value, **kwargs):

        ''' Factory method to create and attach a new IndexEntry. '''

        if isinstance(index, ndb.Model):
            index = index.key
        elif isinstance(index, basestring):
            index = ndb.Key(urlsafe=index)
        return cls(id=value, parent=index, **kwargs)

    def map(self, key, **kwargs):

        ''' Shortcut factory method to add an IndexMapping to an IndexEntry. '''

        return IndexMapping.new(self, key, **kwargs)


######## ======== Index Mutations ======== ########

## IndexMapping - the bottom level of the index tree - mappings from an entry to keys
class IndexMapping(AppModel):

    ''' A mapping: entry => key. '''

    @classmethod
    def new(cls, entry, key, **kwargs):

        ''' Factory method to create and attach a new IndexMapping. '''

        if isinstance(entry, basestring):
            entry = ndb.Key(urlsafe=key)
        elif isinstance(entry, ndb.Model):
            entry = entry.key
        if isinstance(key, ndb.Key):
            key = key.urlsafe()
        return cls(id=key, parent=entry)


## IndexEvent - generated for our index audit log
class IndexEvent(AppModel):

    ''' An event performed by the indexer, like rebuilding/optimizing/creating indexes. '''

    pass


## IndexMutation - a set of mutations applied, as part of an IndexEvent
class IndexMutation(AppModel):

    ''' A mutation event on the mapping/entry/index, built as part of an index event. '''

    pass
