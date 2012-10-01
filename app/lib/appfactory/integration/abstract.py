import config
import webapp2


class CommandBus(object):

	''' Abstract parent for integration classes that add methods to trigger or respond to AppFactory-specific functionality. '''

	@webapp2.cached_property
	def _l9config(self):

		''' Named config pipe to main Layer9 config. '''

		return config.config.get('layer9.appfactory')
