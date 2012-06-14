from protorpc import messages


#### ++++ Object Messages ++++ ####
class IndexerJob(messages.Message):

	''' A single queued indexer job. '''

	pass


class IndexerJobs(messages.Message):

	''' A list of indexer jobs. '''

	pass


#### ++++ Request Messages ++++ ####
class QueueJobRequest(messages.Message):

	''' A request to manually index (or re-index) an item. '''

	pass


#### ++++ Response Messages ++++ ####
class QueuedJobsResponse(messages.Message):

	''' A response with a list of pending indexer jobs. '''

	pass
