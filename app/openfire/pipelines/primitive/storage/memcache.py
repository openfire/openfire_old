# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import StoragePipeline


## MemcachePipeline - abstract parent to all memcache-related pipelines
class MemcachePipeline(StoragePipeline):

    ''' Abstract parent class for low-level datstore pipelines. '''

    pass


## Set - set a value in memcache
class Set(MemcachePipeline):

    ''' Set operation in memcache. '''

    pass


## Add - set a value in memcache only if it doesn't already exist
class Add(MemcachePipeline):

    ''' Add operation in memcache. '''

    pass


## Replace - replace a value in memcache, like `Set`
class Replace(MemcachePipeline):

    ''' Replace operation in memcache. '''

    pass


## Delete - remove an item from memcache
class Delete(MemcachePipeline):

    ''' Delete operation in memcache. '''

    pass


## Increment - increment a number in memcache
class Increment(MemcachePipeline):

    ''' Increment a value in memcache. '''

    pass


## Decrement - decrement a number in memcache
class Decrement(MemcachePipeline):

    ''' Decrement a value in memcache. '''

    pass


## Offset - increment/decrement numerous values in memcache at once
class Offset(MemcachePipeline):

    ''' Offset multiple values in memcache. '''

    pass


## Flush - clear all values from memcache
class Flush(MemcachePipeline):

    ''' Flush all values in memcache. '''

    pass


## GetStats - retrieve statistics about openfire's memcache usage
class GetStats(MemcachePipeline):

    ''' Get memcache stats. '''

    pass
