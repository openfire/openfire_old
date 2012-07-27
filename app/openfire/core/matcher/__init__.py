# -*- coding: utf-8 -*-

## Basic Imports
import config
import hashlib
import webapp2

## AppTools Imports
from apptools.util import debug

## Core Imports
from openfire.core import CoreAPI
from openfire.core.matcher.query import Query

## Models
from openfire.models import user as user_m
from openfire.models import matcher as models
from openfire.models import social as social_m
from openfire.pipelines.primitive import matcher as pipelines

## SDK Imports
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import prospective_search as matcher

## Globals
_keys_only_opt = ndb.QueryOptions(keys_only=True, limit=3, produce_cursors=False, read_policy=ndb.EVENTUAL_CONSISTENCY, hint=ndb.QueryOptions.ANCESTOR_FIRST, deadline=5)
_projection_opt = ndb.QueryOptions(keys_only=False, limit=3, produce_cursors=False, read_policy=ndb.EVENTUAL_CONSISTENCY, hint=ndb.QueryOptions.ANCESTOR_FIRST, deadline=5)


## CoreMatcherAPI - manages prospective search API-based features, and the related datamodel/dispatch structure
class CoreMatcherAPI(CoreAPI):

    ''' The Core Matcher API manages prospective search queries, and what to do when documents are found to match. '''

    ## == API State == ##
    queries = []
    hash_algorithm = hashlib.sha256

    ## == Low-Level Methods == ##
    @webapp2.cached_property
    def config(self):

        ''' Cached config shortcut. '''

        return config.config.get('openfire.matcher', {})

    @webapp2.cached_property
    def logging(self):

        ''' Cached, named logging pipe. '''

        return debug.AppToolsLogger(path='openfire.core.matcher', name='CoreMatcherAPI')._setcondition(self.config.get('logging', False))

    def _flatten(self, list_of_lists):

        ''' Flatten a potential list-of-lists into a single list. '''

        if isinstance(list_of_lists, list) and len(list_of_lists) == 1:
            return list_of_lists[0]
        else:
            return list_of_lists

    @ndb.tasklet
    def _return(self, result, *args, **kwargs):

        ''' Raise an NDB Return exception. '''

        # If it's a future, block to return
        if isinstance(result, ndb.Future):
            if isinstance(result, ndb.MultiFuture):
                result = map(self._flatten, result.get_result())
            else:
                result = result.get_result()

        raise ndb.Return(result, *args, **kwargs)

    @ndb.tasklet
    def _run_query_async(self, query, count=False, future=None, resultset_callback=None, item_callback=None):

        ''' Asynchronously run a database query. '''

        # if we just counted
        if future:

            # we have a limit
            count = future.get_result()

            # there are no results
            if count == 0:
                yield resultset_callback([])

        # if we should count first, kick off a count and call self with the result
        elif not isinstance(count, int) and count is True:
            future = query.count_async(**kwargs)
            future.add_callback(self._run_query_async, query, False, future, resultset_callback, item_callback, **kwargs)
            yield future

        else:

            # if we want to go over things in batch
            if resultset_callback and not item_callback:
                if isinstance(count, int):
                    future = query.fetch_async(count, **kwargs)
                else:
                    future = query.fetch_async(**kwargs)

            # if we want to go over things one at a time
            elif item_callback and not resultset_callback:
                if isinstance(count, int):
                    future = query.map_async(item_callback, limit=count, **kwargs)
                else:
                    future = query.map_async(item_callback, **kwargs)

            yield future

    @ndb.tasklet
    def _batch_fulfill_async(self, batch, resultset_callback=None, item_callback=None, **kwargs):

        ''' Asynchronously retrieve a batch of keys. '''

        # if it's a future, we're probably coming from a now-finished query
        if isinstance(batch, ndb.Future):
            batch = batch.get_result()

        # if it's not a list make it a list (obvs cuz this is _batch_ fulfill async)
        if not isinstance(batch, list):
            batch = [batch]

        # build operations
        op = ndb.get_multi_async(batch, **kwargs)

        # if we want results in batch
        if resultset_callback and not item_callback:

            # build a dependent multifuture that waits on all to finish
            multifuture = ndb.MultiFuture()

            # add each operation as a dependent
            for f in op:
                multifuture.add_dependent(f)

            # close dependents
            multifuture.complete()

            # add callback to catch results in batch
            multifuture.add_callback(resultset_callback, multifuture)

        # if we want results one at a time
        elif item_callback and not resultset_callback:

            # add the item callback to each future
            for f in op:
                f.add_callback(item_callback, f)

        yield tuple(op)

    def _get_matcher_subscriptions(self, document, rangestart='', topic=None, max_results=1000, expires_before=None):

        ''' Wrapper to the prospective search API's list_subscriptions method. '''

        return matcher.list_subscriptions(document, rangestart, topic, max_results, expires_before)

    def _get_matcher_subscription(self, document, sub_id, topic=None):

        ''' Get a single subscription from the prospective search API using the get_subscription method. '''

        return matcher.get_subscription(document, sub_id, topic)

    def _matcher_subscribe(self, document, querystring, sub_id, topic=None, lease_duration_sec=0):

        ''' Create a subscription using the prospective search API's subscribe method. '''

        return matcher.subscribe(document, querystring, sub_id, topic, lease_duration_sec)

    def _match_document(self, document, topic=None, result_key=None, result_relative_url=None, result_task_queue='trigger', result_batch_size=100, result_return_document=True):

        ''' Match a document against registered prospective search API queries. '''

        if result_relative_url is None:
            result_relative_url = webapp2.uri_for('internal/matcher-match')
        return matcher.match(document, topic, result_key, result_relative_url, result_task_queue, result_batch_size, result_return_document)

    def _build_keysonly_query(self, kind, parent=None, **kwargs):

        ''' Build a keys-only ndb.Query object with the _keys_only options object. '''

        return kind.query(ancestor=parent, default_options=_keys_only_opt.merge(ndb.QueryOptions(**kwargs)))

    def _build_projection_query(self, kind, properties, parent=None, **kwargs):

        ''' Build a projection ndb.Query object with the default _projection_opt options object. '''

        return kind.query(ancestor=parent, default_options=_projection_opt.merge(ndb.QueryOptions(projection=properties, **kwargs)))

    def _build_decorator_key(self, parent, decorator, keyname):

        ''' Build a key for a decorator record. '''

        return ndb.Key(decorator, keyname, parent=parent)

    def _build_namespace_key(self, keyname=None, hash=None):

        ''' Build a key for a MatcherNamespace. '''

        if isinstance(keyname, ndb.Key):
            return keyname
        if not hash:
            return ndb.Key(models.MatcherNamespace, self.hash_algorithm(keyname).hexdigest())
        elif isinstance(hash, basestring):
            return ndb.Key(models.MatcherNamespace, hash)
        else:
            return False

    def _build_query_key(self, query=None, hash=None, namespace=None):

        ''' Build a key for a MatcherQuery. '''

        if isinstance(query, ndb.Key):
            return query

        if not hash:
            if not isinstance(query, Query):

                # if it's a querystring
                if isinstance(query, basestring):
                    query = Query.from_string(query)

                # if it's an NDB query
                elif isinstance(query, ndb.Query):
                    query = Query.from_query(query)

            hash = query.get_hash()

        return ndb.Key(models.MatcherQuery, hash, parent=self._build_namespace_key(keyname=namespace))

    def _build_subscription_key(self, user=None, hash=None, query=None, namespace=None):

        ''' Build a key for a MatcherSubscription. '''

        if isinstance(user, ndb.Key):
            if user.kind() == 'MatcherSubscription':
                return user

        if not hash:
            if isinstance(user, ndb.Model):
                ukey = user.key
            elif isinstance(user, basestring):

                # stringified key first
                try:
                    ukey = ndb.Key(urlsafe=user)
                except:
                    ukey = ndb.Key(user_m.User, user)

            hash = ukey.urlsafe()

        if not isinstance(query, Query):
            query = self._build_query_key(query=query, namespace=namespace)
        else:
            query = query.get_key()

        return ndb.Key(models.MatcherSubscription, hash, parent=query)

    ## == Mid-level Methods == ##
    @ndb.tasklet
    def _create_namespace(self, name, kinds=None, **kwargs):

        ''' Create a MatcherNamespace record. '''

        if kinds is None:
            kinds = []

        yield models.MatcherNamespace(id=self.hash_algorithm(name).hexdigest(), topic=name, kinds=(isinstance(kinds, list) and map(lambda x: isinstance(x, basestring) and x or x.__name__, kinds) or []), **kwargs).put_async()

    @ndb.tasklet
    def _resolve_namespace(self, key=None, keyname=None, hash=None, create=True, kinds=None, **kwargs):

        ''' Resolve a MatcherNamespace by its keyname, and create it if it does not exist. '''

        if not key:
            if not hash:
                hash = self.hash_algorithm(keyname).hexdigest()
            key = ndb.Key(models.MatcherNamespace, hash)
        namespace = key.get()
        if namespace is None:
            if create:
                if kinds:
                    yield self._create_namespace(name=keyname, kinds=kinds, **kwargs)
                else:
                    yield self._create_namespace(name=keyname, **kwargs)
        yield self._return(namespace)

    @ndb.tasklet
    def _create_query(self, query, namespace, **kwargs):

        ''' Create a MatcherQuery record and accompanying Query object. '''

        if isinstance(query, basestring):
            query = yield models.MatcherQuery(key=self._build_query_key(query=query, namespace=namespace), query=Query.from_string(query).get_string(), namespace=self._build_namespace_key(namespace), **kwargs).put_async()
        elif isinstance(query, ndb.Query):
            query = yield models.MatcherQuery(key=self._build_query_key(query=query, namespace=namespace), query=Query.from_query(query).get_string(), namespace=self._build_namespace_key(namespace), **kwargs).put_async()
        elif isinstance(query, Query):
            query = yield models.MatcherQuery(key=self._build_query_key(query=query, namespace=namespace), query=Query.get_string(), namespace=self._build_namespace_key(namespace), **kwargs).put_async()
        yield self._return(Query.from_model(query))

    @ndb.tasklet
    def _resolve_query(self, query, namespace=None, **kwargs):

        ''' Resolve a MatcherQuery by its namespace and/or query string, and create it if it does not exist. '''

        # normalize query
        if isinstance(query, basestring):
            query = Query.from_string(query)
        elif isinstance(query, ndb.Query):
            query = Query.from_query(query)

        # get the query in all namespaces
        if namespace is None:
            query_q = yield self._run_query_async(self._build_keysonly_query(kind=models.MatcherQuery).filter(models.MatcherQuery.query == query.get_string()), count=True, resultset_callback=self._return)
        else:
            query_q = yield models.MatcherQuery.get_by_id_async(query.get_hash(), parent=self._build_namespace_key(namespace))
            query_q = query_q.get_result()
            if query_q is None:
                query_q = yield self._create_query(query, namespace, **kwargs)

        yield self._return(query_q)

    @ndb.tasklet
    def _create_decorator(self, parent, decorator, target, **kwargs):

        ''' Create a decorator record. '''

        if isinstance(target, ndb.Key):
            target = target.urlsafe()

        if isinstance(parent, basestring):
            parent = ndb.Key(urlsafe=parent)

        future = yield decorator(key=ndb.Key(decorator, target, parent=parent), subject=parent, **kwargs).put_async()
        yield self._return(future)

    @ndb.tasklet
    def _resolve_decorator(self, parent, decorator, target, **kwargs):

        ''' Check to see if a decorator record exists, and create one if not. '''

        if isinstance(target, ndb.Key):
            target = target.urlsafe()

        if isinstance(parent, basestring):
            parent = ndb.Key(urlsafe=parent)

        key = ndb.Key(decorator, target, parent=parent).get()
        if key is None:
            yield self._create_decorator(parent, decorator, target, **kwargs)
        else:
            yield self._return(key)

    @ndb.tasklet
    def _create_subscription(self, user, query, namespace, document, **kwargs):

        ''' Create a subscription record. '''

        # normalize user
        if not isinstance(user, ndb.Key):
            if isinstance(user, basestring):
                user = ndb.Key(urlsafe=user)
            elif isinstance(user, ndb.Model):
                user = user.key

        # make subscription and matcher subscription
        subscription = yield models.MatcherSubscription(key=self._build_subscription_key(user=user.urlsafe(), query=query.get_key(), namespace=namespace), user=user, query=query, **kwargs).put_async()
        matcher_subscription = self._matcher_subscribe(document, query.get_string(), subscription.get_result().urlsafe(), topic=namespace.urlsafe(), lease_duration_sec=0)

        yield self._return((subscription, matcher_subscription))

    @ndb.tasklet
    def _resolve_subscription(self, user, query, namespace, document, **kwargs):

        ''' Check to see if a subscription exists, and create one if not '''

        if not isinstance(user, ndb.Key):
            if isinstance(user, basestring):
                user = ndb.Key(urlsafe=user)
            elif isinstance(user, ndb.Model):
                user = user.key

        if not isinstance(query, Query):
            if isinstance(query, basestring):
                query = Query.from_string(query)
            elif isinstance(query, ndb.Query):
                query = Query.from_query(query)

        namespace = self._build_namespace_key(namespace)
        key = ndb.Key(key=self._build_subscription_key(user, query, namespace)).get()
        if key is None:
            yield self._create_subscription(user, query, namespace, document, **kwargs)
        else:
            yield self._return(key)

    ## == High-Level Methods == ##
    @ndb.synctasklet
    def subscribe(self, user, subject, query=None, namespace=None, decorator=social_m.Follow, **kwargs):

        ''' Create a new subscription. '''

        subscription_f = ndb.MultiFuture()

        # resolve namespace
        if not namespace:
            namespace = yield self._resolve_namespace(key=_build_namespace_key(keyname=subject.key.kind()))
            subscription_f.add_dependent(namespace)

        # resolve query
        if not isinstance(query, Query):
            if isinstance(query, basestring):
                query = Query.from_string(query)
            elif isinstance(query, ndb.Query):
                query = Query.from_query(query)
            query = yield self._resolve_query(query, namespace)
            subscription_f.add_dependent(query)

        # create/resolve subscription
        subscription = yield self._resolve_subscription(user, query, namespace, **kwargs)
        subscription_f.add_dependent(subscription)

        # create/resolve decorator
        decorator = yield self._resolve_decorator(subject, decorator, user, user=user, subscription=subscription)
        subscription_f.add_dependent(decorator)
        subscription_f.complete()

        yield self._return(subscription_f)

    @ndb.synctasklet
    def unsubscribe(self, subscription_id):

        ''' Remove an existing subscription. '''

        pass

    @ndb.synctasklet
    def match(self, document):

        ''' Match a document against registered prospective search queries. '''

        pass

    @ndb.synctasklet
    def namespaces(self, kind=None):

        ''' Get a list of existing namespaces. '''

        if kind:
            future = yield self._run_query_async(self._build_keysonly_query(kind=models.MatcherNamespace).filter(models.MatcherNamespace.kind == kind), count=True, resultset_callback=self._batch_fulfill_async, eventual_callback=self._return)
        else:
            future = yield self._run_query_async(self._build_keysonly_query(kind=models.MatcherNamespace), count=True, resultset_callback=self._batch_fulfill_async, eventual_callback=self._return)

        yield future

    @ndb.synctasklet
    def subscribers(self, namespace, query=None):

        ''' Get a list of subscribers to a query or all queries in a namespace. '''

        namespace = self._build_namespace_key(namespace)
        if query is None:
            queries = yield self._run_query_async(self._build_keysonly_query(kind=models.MatcherQuery, parent=namespace))
        else:
            queries = [query]

        subscriptions_q = ndb.MultiFuture()
        for query in queries:

            future = yield self._batch_fulfill_async(self._run_query_async(self._build_keysonly_query(kind=models.MatcherSubscription, parent=query)))
            subscriptions_q.add_dependent(future)

        subscriptions_q.complete()
        yield self._return(subscriptions_q)
