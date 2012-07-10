# -*- coding: utf-8 -*-
from openfire.models.indexer import IndexerModel


######## ======== Index Mappings ======== ########

## IndexMapping - the bottom level of the index tree - mappings from an entry to keys
class IndexMapping(IndexerModel):

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
