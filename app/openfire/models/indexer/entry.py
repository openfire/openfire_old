# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from openfire.models.indexer import IndexerModel
from openfire.models.indexer.map import IndexMapping


######## ======== Index Entries ======== ########

## IndexEntry - hierarchical stop for *values* in the index
class IndexEntry(IndexerModel):

    ''' A value entry in the index. '''

    @classmethod
    def new(cls, index, value, **kwargs):

        ''' Factory method to create and attach a new IndexEntry. '''

        if isinstance(index, ndb.Model):
            index = index.key
        elif isinstance(index, basestring):
            index = ndb.Key(urlsafe=index)
        return cls(id=value, parent=index, **kwargs)

    def map(self, key, mapping=IndexMapping, **kwargs):

        ''' Shortcut factory method to add an IndexMapping to an IndexEntry. '''

        return mapping.new(self, key, **kwargs)
