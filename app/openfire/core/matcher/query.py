import json
import base64
import hashlib

from apptools.util import json


_query_booleans = frozenset(['NOT', 'OR', 'AND'])


class Query(object):

	''' Contains/wraps a query string, properly formatting it/handling it for storage/translation/lookup. '''

	## == Object State == ##
	__key = None
	__model = None
	__scoped = True
	__filters = {}
	__partial = False
	__original = None
	__namespace = None
	__hash_algorithm = hashlib.sha256

	## == Internal == ##
	def __init__(self, filters=None, namespace=None, scoped=True, partial=False, model=None):

		''' Init an empty Query object. '''

		self.__model = model
		self.__scoped = scoped
		self.__partial = partial
		self.__namespace = namespace

		if filters is not None:
			self.__filters = filters

	## == Comparison == ##
	def __eq__(self):
		pass

	## == String Translation == ##
	def __hash__(self):
		pass

	def __str__(self):
		pass

	def __repr__(self):
		pass

	def __unicode__(self):
		pass

	## == Formatters == ##
	def __json__(self):
		pass

	def __binary__(self):
		pass

	## = High-Level Methods == ##
	def get_key(self, namespace=None):

		''' Retrieve an NDB key for this Query, if assigned. '''

		raise NotImplemented

	def get_hash(self, hash_algorithm=hashlib.sha256):

		''' Retrieve a hashed version of this Query. '''

		return hash_algorithm(base64.b64encode(self.get_string())).hexdigest()

	def get_query(self):

		''' Retrieve an NDB Query built from this Query. '''

		raise NotImplemented

	def get_string(self):

		''' Retrieve a formatted querystring built from this Query. '''

		fblocks = []

		# pack filters
		for p, v in self.__filters.items():
			if p == '*':
				fblocks.append(v)
			else:
				fblocks.append(':'.join([p, v]))

		return fblocks.join(' ')

	@classmethod
	def from_string(cls, querystring, **kwargs):

		''' Build a Query object from a query string. '''

		## process querystring
		filtergroups = {}
		for filtergroup in map(lambda x: x.split(':'), querystring.strip().split(' ')):
			if len(filtergroup) > 1:
				key, value = filtergroup[0], filtergroup[1]
			else:
				key, value = '*', filtergroup[0]

			filtergroups[key] = value

		return cls(filters=filtergroups, **kwargs)

	@classmethod
	def from_model(cls, querymodel, **kwargs):

		''' Build a Query object from a MatcherQuery model. '''

		return cls.from_string(querymodel.query, namespace=querymodel.namespace, model=querymodel)

	@classmethod
	def from_query(cls, dbquery, **kwargs):

		''' Build a Query object from an NDB Query. '''

		raise NotImplementedError
