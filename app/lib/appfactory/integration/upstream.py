import config
import webapp2

from appfactory.integration.abstract import CommandBus


class UpstreamBus(CommandBus):

	''' AppFactory upstream layer integration. '''

	headers = {


	}

	def sniff(self, request):

		''' Sniff a request for headers that were added by the AppFactory upstream servers. '''

		pass

	def dispatch(self, request):

		''' Dispatch internal functions to change aspects of the environment or request based on a sniffed header. '''

		pass

	def dump(self, request):

		''' Dump the upstream state to memcache, so stats and realtime operations can be introspected and displayed. '''

		pass


IntegrationBridge = UpstreamBus()
