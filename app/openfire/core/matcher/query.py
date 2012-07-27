import hashlib

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

		pass

	def get_hash(self, hash_algorithm=None):

		''' Retrieve a hashed version of this Query. '''

		pass

	def get_query(self):

		''' Retrieve an NDB Query built from this Query. '''

		pass

	def get_string(self):

		''' Retrieve a formatted querystring built from this Query. '''

		pass

	@classmethod
	def from_query(cls, dbquery, **kwargs):

		''' Build a Query object from an NDB Query. '''

		pass

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

			filtergroups[key] = filtergroups.get(key, []).append((value))

		return cls(filters=query, **kwargs)

	@classmethod
	def from_model(cls, querymodel, **kwargs):

		''' Build a Query object from a MatcherQuery model. '''

		return cls.from_string(querymodel.query, namespace=querymodel.namespace, model=querymodel)
