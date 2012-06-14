from protorpc import remote
from protorpc import message_types
from openfire.messages import indexer
from openfire.services import RemoteService


class IndexerService(RemoteService):

	''' Remote service for controlling the internal indexing engine. '''

	@remote.method(indexer.QueueJobRequest, message_types.VoidMessage)
	def index(self, response):

		''' Manually index something. '''

		pass

	@remote.method(message_types.VoidMessage, indexer.QueuedJobsResponse)
	def queued(self, response):

		''' Return a list of pending indexer jobs. '''

		pass

	@remote.method(message_types.VoidMessage, message_types.VoidMessage)
	def purge(self, request):

		''' Purge all pending indexer jobs, or just one. '''

		pass

	@remote.method(message_types.VoidMessage, message_types.VoidMessage)
	def rebuild(self, request):

		''' Trigger a manual index rebuild. '''

		pass