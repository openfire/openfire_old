# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import StoragePipeline


class MemcachePipeline(StoragePipeline):

    ''' Abstract parent class for low-level datstore pipelines. '''

    pass


class Set(MemcachePipeline):

    ''' Set operation in memcache. '''

    pass


class Add(MemcachePipeline):

    ''' Add operation in memcache. '''

    pass


class Replace(MemcachePipeline):

    ''' Replace operation in memcache. '''

    pass


class Delete(MemcachePipeline):

    ''' Delete operation in memcache. '''

    pass


class Increment(MemcachePipeline):

    ''' Increment a value in memcache. '''

    pass


class Decrement(MemcachePipeline):

    ''' Decrement a value in memcache. '''

    pass


class Offset(MemcachePipeline):

    ''' Offset multiple values in memcache. '''

    pass


class Flush(MemcachePipeline):

    ''' Flush all values in memcache. '''

    pass


class GetStats(MemcachePipeline):

    ''' Get memcache stats. '''

    pass
