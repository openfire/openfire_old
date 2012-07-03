# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import StoragePipeline


class DatastorePipeline(StoragePipeline):

    ''' Abstract parent class for low-level datstore pipelines. '''

    pass


class DatastoreTransaction(DatastorePipeline):

    ''' Abstract class representing a transactional datastore mutation. '''

    pass


class SystemProperty(DatastorePipeline):

    ''' Store a SystemProperty expando. '''

    pass


class RunFixture(DatastorePipeline):

    ''' Run a fixture at a given path. '''

    pass


class RunPutTrigger(DatastoreTransaction):

    ''' Given a key, run the model's put trigger on the entity at that key. '''

    pass


class RunDeleteTrigger(DatastoreTransaction):

    ''' Given a key, run the model's delete trigger on the entity at that key. '''

    pass


class RunHeartbeatTrigger(DatastoreTransaction):

    ''' Given a key, run the model's heartbeat trigger on the entity at that key. '''

    pass


class RunGarbageCollector(DatastoreTransaction):

    ''' Kick off a garbage collection routine for a given model. '''

    pass


class QueueForDelete(DatastoreTransaction):

    ''' Queue a model for TTL/heartbeat pruning. '''

    pass


class CascadeDeletes(DatastoreTransaction):

    ''' Delete all children, given an ancestor parent key. '''

    pass


class SchemaUpdate(DatastoreTransaction):

    ''' Update a model's schema. '''

    pass


class TouchEntity(DatastoreTransaction):

    ''' Touch an entity, souch that any `modified` timestamps update. '''

    pass
