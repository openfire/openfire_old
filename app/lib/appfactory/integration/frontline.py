import config
import webapp2

from apptools.util import debug
from apptools.util import datastructures

from appfactory.integration.abstract import CommandBus


_FRONTLINE_HEADERS = frozenset(['Frontline',
								'Agent',
								'Hostname',
								'Broker',
								'Protocol',
								'Version',
								'Entrypoint',
								'Flags'])

_FRONTLINE_FLAGS = frozenset(['ap', 'opt'])


class FrontlineBus(CommandBus):

	''' AppFactory Frontline management and integration code. '''

	@webapp2.cached_property
	def config(self):

		''' Named config pipe. '''

		return config.config.get('layer9.appfactory.frontline')

	@webapp2.cached_property
	def logging(self):

		''' Named logging pipe. '''

		return debug.AppToolsLogger(path='appfactory.integration.frontline', name='FrontlineBus')._setcondition(self.config.get('debug', False))

	def sniff(self, handler):

		''' Sniff a request for headers that were added by the AppFactory upstream servers. '''

		self.logging.info('Sniffing request for AppFactory frontline headers.')

		if self._l9config.get('headers', {}).get('use_compact', False):
			prefix = self._l9config.get('headers', {}).get('full_prefix', 'X-AppFactory')
		else:
			prefix = self._l9config.get('headers', {}).get('compact_prefix', 'XAF')

		sniffed = []
		for i in _FRONTLINE_HEADERS:
			header_i = '-'.join([prefix, i])
			self.logging.info('--Looking for header "%s".' % header_i)

			if header_i in handler.request.headers:
				self.logging.info('-----Found!')
				sniffed.append((i, lambda: handler.request.headers[header_i]))

		for header_s, getter in sniffed:
			self.logging.info('Dispatching sniffed header action for header "%s".' % header_s)
			try:
				self.dispatch(handler, header_s, getter)
			except:
				self.logging.error('Encountered an error dispatching detected AppFactory trigger header "%s".' % header_s)




	def dispatch(self, handler, header, value):

		''' Dispatch internal functions to change aspects of the environment or request based on a sniffed header. '''

		pass

	def dump(self, handler):

		''' Dump the upstream state to memcache, so stats and realtime operations can be introspected and displayed. '''

		pass

IntegrationBridge = FrontlineBus()
