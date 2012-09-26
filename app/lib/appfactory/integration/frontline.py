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

	## == ##
	@webapp2.cached_property
	def config(self):

		''' Named config pipe. '''

		return config.config.get('layer9.appfactory.frontline')

	@webapp2.cached_property
	def logging(self):

		''' Named logging pipe. '''

		return debug.AppToolsLogger(path='appfactory.integration.frontline', name='FrontlineBus')._setcondition(self.config.get('debug', False))

	## == ##
	def __flags(self, handler, value): self.logging.critical("FLAGS!!!!!! %s" % value)
	def __agent(self, handler, value): self.logging.critical("AGENT!!!!!! %s" % value)
	def __broker(self, handler, value): self.logging.critical("BROKER!!!!!! %s" % value)
	def __version(self, handler, value): self.logging.critical("VERSION!!!!!! %s" % value)
	def __protocol(self, handler, value): self.logging.critical("PROTOCOL!!!!!! %s" % value)
	def __hostname(self, handler, value): self.logging.critical("HOSTNAME!!!!!! %s" % value)
	def __frontline(self, handler, value): self.logging.critical("FRONTLINE!!!!!! %s" % value)
	def __entrypoint(self, handler, value): self.logging.critical("ENTRYPOINT!!!!!! %s" % value)

	trigger = datastructures.DictProxy({

		'flags': __flags,
		'agent': __agent,
		'broker': __broker,
		'version': __version,
		'protocol': __protocol,
		'hostname': __hostname,
		'frontline': __frontline,
		'entrypoint': __entrypoint

	})

	## == ##
	def _dispatch(self, handler, header, value):

		''' Dispatch internal functions to change aspects of the environment or request based on a sniffed header. '''

		handler._triggered = {}
		self.logging.info('Dispatching action for header "%s".' % (header))

		if hasattr(self.trigger, header.lower()):
			try:
				value = getattr(self.trigger, header.lower())(self, handler, value)
			except Exception, e:
				self.logging.error('Unhandled exception "%s" encountered when triggering functionality on AppFactory standard header "%s", set at value "%s".' % (e, header, value))
				if config.debug:
					raise
				else:
					return False
			else:
				self.logging.debug('Dispatched action completed with no issues.')
		return value

	def sniff(self, handler):

		''' Sniff a request for headers that were added by the AppFactory upstream servers. '''

		self.logging.info('Sniffing request for AppFactory frontline headers.')
		self.logging.info('REQUEST DUMP:')
		self.logging.info(str(handler.request))

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
				sniffed.append((i, handler.request.headers[header_i]))

		for header_s, value in sniffed:
			self.logging.info('Dispatching sniffed header action for header "%s".' % header_s)
			try:
				self._dispatch(handler, header_s, value)
			except:
				self.logging.error('Encountered an error dispatching detected AppFactory trigger header "%s".' % header_s)

		return sniffed

	def dump(self, handler):

		''' Dump the upstream state to memcache, so stats and realtime operations can be introspected and displayed. '''

		pass


IntegrationBridge = FrontlineBus()
