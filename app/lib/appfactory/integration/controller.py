import config
import webapp2

from apptools.util import debug

from appfactory.integration.abstract import CommandBus


class ControllerBus(CommandBus):

	## == Internal Methods == ##
	@webapp2.cached_property
	def config(self):

		''' Named config pipe. '''

		return config.config.get('layer9.appfactory.controller')

	@webapp2.cached_property
	def logging(self):

		''' Named logging pipe. '''

		return debug.AppToolsLogger(path='appfactory.integration.controller', name='ControllerBus')._setcondition(self.config.get('debug', False))

	def dump(self, handler, result):

		''' Dump controller state to memcache for later statistics generation. '''

		self.logging.info('Dumped AppFactory Controller state.')


IntegrationBridge = ControllerBus()
