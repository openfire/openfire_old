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
from openfire.pipelines.primitive import matcher as pipelines

## SDK Imports
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import prospective_search as matcher


## CoreMatcherAPI - manages prospective search API-based features, and the related datamodel/dispatch structure
class CoreMatcherAPI(CoreAPI):

    ''' The Core Matcher API manages prospective search queries, and what to do when documents are found to match. '''

    ## == API State == ##
    queries = []
    hash_algorithm = hashlib.sha256

    @webapp2.cached_property
    def config(self):

		''' Cached config shortcut. '''

		return config.config.get('openfire.matcher', {})

	@webapp2.cached_property
	def logging(self):

		''' Cached, named logging pipe. '''

		return debug.AppToolsLogger(path='openfire.core.matcher', name='CoreMatcherAPI')._setcondition(self.config.get('logging', False))

	## == Low-Level Methods == ##
	@ndb.tasklet
	def _return(self, *args, **kwargs):

		''' Raise an NDB Return exception. '''

		raise ndb.Return(*args, **kwargs)

	@ndb.tasklet
	def _run_query_async(self, query, resultset_callback=None, item_callback=None):

		''' Asynchronously run a database query. '''

		pass

	@ndb.tasklet
	def _batch_fulfill_async(self, batch, resultset_callback=None, item_callback=None):

		''' Asynchronously retrieve a list of keys. '''

		pass

	def _get_matcher_subscriptions(self, document, rangestart='', topic=None, max_results=1000, expires_before=None):

		''' Wrapper to the prospective search API's list_subscriptions method. '''

		return matcher.list_subscriptions(document, rangestart, topic, max_results, expires_before)

	def _get_matcher_subscription(self, document, sub_id, topic=None):

		''' Get a single subscription from the prospective search API using the get_subscription method. '''

		return matcher.get_subscription(document, sub_id, topic)

	def _match_document(self, document, topic=None, result_key=None, result_relative_url=webapp2.uri_for('internal/matcher-match'), result_task_queue='trigger', result_batch_size=100, result_return_document=True):

		''' Match a document against registered prospective search API queries. '''

		return matcher.match(document, topic, result_key, result_relative_url, result_task_queue, result_batch_size, result_return_document)

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

		if not hash:
			if not isinstance(query, Query):
				query = Query.from_string(query)
			hash = query.get_hash()

		return ndb.Key(models.MatcherQuery, hash, parent=self._build_namespace_key(keyname=namespace))

	def _build_subscription_key(self, user=None, hash=None, query=None, namespace=None):

		''' Build a key for a MatcherSubscription. '''

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

		return ndb.Key(models.MatcherSubscription, hash, parent=query)

	## == Mid-level Methods == ##
	def _create_namespace(self, name, kinds=[]):

		''' Create a MatcherNamespace record. '''

		return models.MatcherNamespace(id=self.hash_algorithm(name).hexdigest(), topic=name, kinds=(isinstance(kinds, list) and map(lambda x: isinstance(x, basestring) and x or x.__name__, kinds) or [])).put()

	def _resolve_namespace(self, key=None, keyname=None, hash=None, create=True, kinds=None):

		''' Resolve a MatcherNamespace by its keyname, and create it if it does not exist. '''

		if not key:
			if not hash:
				hash = self.hash_algorithm(keyname).hexdigest()
			key = ndb.Key(models.MatcherNamespace, hash)
		namespace = key.get()
		if namespace is None:
			if create:
				if kinds:
					return self._create_namespace(name=keyname, kinds=kinds)
				else:
					return self._create_namespace(name=keyname)
		return namespace

	def _create_query(self, query, namespace=None):

		''' Create a MatcherQuery record. '''

		pass

	def _resolve_query(self, querystring, namespace=None):

		''' Resolve a MatcherQuery by its namespace and/or query string. '''

		pass

	def _create_decorator(self, parent, decorator, target):

		''' Create a decorator record. '''

		pass

	def _resolve_decorator(self, parent, decorator, target):

		''' Check to see if a decorator record exists. '''

		pass

	def _create_subscription(self, user, query, namespace):

		''' Create a subscription record. '''

		pass

	def _resolve_subscription(self, user, query, namespace):

		''' Check to see if a subscription exists. '''

		pass

	## == High-Level Methods == ##
	@ndb.tasklet
	def subscribe(self, user, subject, query=None, namespace=None):

		''' Create a new subscription. '''

		# resolve namespace
		if not namespace:
			namespace = self._resolve_namespace(key=_build_namespace_key(keyname=subject.key.kind()))

		# resolve query
		if not isinstance(query, Query):
			if isinstance(query, basestring):
				query = Query.from_string(query)
			elif isinstance(query, ndb.Query):
				raise ValueError('No support for translating NDB queries yet.')

	@ndb.tasklet
	def unsubscribe(self, subscription_id):

		''' Remove an existing subscription. '''

		pass

	@ndb.tasklet
	def match(self, document):

		''' Match a document against registered prospective search queries. '''

		pass

	@ndb.tasklet
	def namespaces(self, kind=None):

		''' Get a list of existing namespaces. '''

		if kind:
			future = yield self._run_query_async(self._build_keysonly_query(kind=models.MatcherNamespace).filter(models.MatcherNamespace.kind == kind), count=True, resultset_callback=self._batch_fulfill_async, eventual_callback=self._return)
		else:
			future = yield self._run_query_async(self._build_keysonly_query(kind=models.MatcherNamespace), count=True, resultset_callback=self._batch_fulfill_async, eventual_callback=self._return)

		yield future

	@ndb.tasklet
	def subscribers(self, namespace, query=None):

		''' Get a list of subscribers to a query or all queries in a namespace. '''

		pass
