## matcher query stuff

class Query(object):

	''' Contains/wraps a query string, properly formatting it/handling it for storage/translation/lookup. '''

	## == Object State == ##
	__model = None
	__scoped = True
	__filters = {}
	__partial = False

	## == Internal == ##
	def __init__(self):
		pass

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
