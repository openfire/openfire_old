# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import StoragePipeline


## DatastorePipeline - abstract parent for all datastore-related pipelines
class DatastorePipeline(StoragePipeline):

    ''' Abstract parent class for low-level datstore pipelines. '''

    pass


## DatastoreTransaction - parent for all transactional pipelines
class DatastoreTransaction(DatastorePipeline):

    ''' Abstract class representing a transactional datastore mutation. '''

    pass


## SystemProperty - yield a persisted system property
class SystemProperty(DatastorePipeline):

    ''' Store a SystemProperty expando. '''

    pass


## RunFixture - run a data fixture at a given path
class RunFixture(DatastorePipeline):

    ''' Run a fixture at a given path. '''

    pass


## RunPutTrigger - run a model class' put trigger pipeline
class RunPutTrigger(DatastoreTransaction):

    ''' Given a key, run the model's put trigger on the entity at that key. '''

    pass


## RunDeleteTrigger - run a model class' delete trigger pipeline
class RunDeleteTrigger(DatastoreTransaction):

    ''' Given a key, run the model's delete trigger on the entity at that key. '''

    pass


## RunHeartbeatTrigger - run a model class' heartbeat trigger pipeline
class RunHeartbeatTrigger(DatastoreTransaction):

    ''' Given a key, run the model's heartbeat trigger on the entity at that key. '''

    pass


## RunGarbageCollector - run the garbage collector over all entities of a given kind
class RunGarbageCollector(DatastoreTransaction):

    ''' Kick off a garbage collection routine for a given model. '''

    pass


## QueueForDelete - queue an entity to be pruned/deleted via garbage collection
class QueueForDelete(DatastoreTransaction):

    ''' Queue a model for TTL/heartbeat pruning. '''

    pass


## CascadeDeletes - cascade a key-based delete to all child entities
class CascadeDeletes(DatastoreTransaction):

    ''' Delete all children, given an ancestor parent key. '''

    pass


## SchemaUpdate - cascade a schema update over all entities in a range
class SchemaUpdate(DatastoreTransaction):

    ''' Update a model's schema. '''

    pass


## TouchEntity - pull and put an entity such that any `modified` timestamps update
class TouchEntity(DatastoreTransaction):

    ''' Touch an entity, souch that any `modified` timestamps update. '''

    pass
