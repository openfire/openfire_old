from openfire.models.transport import TransportModel


class FetchOperation(TransportModel):

	''' Keeps status info and stuff about a queued or finished URLFetch job. '''

	url = ndb.StringProperty(required=True, indexed=True)
	payload = ndb.BlobProperty(default=None)
	method = ndb.StringProperty(default='GET', choices=['GET', 'POST', 'HEAD', 'PUT', 'DELETE'], indexed=True)
	headers = ndb.PickleProperty(default=None)
	allow_truncated = ndb.BooleanProperty(default=False)
	follow_redirects = ndb.BooleanProperty(default=True)
	deadline = ndb.IntegerProperty(default=None)
	validate_certificate = ndb.BooleanProperty(default=None)
	data = ndb.KeyProperty(default=None)
	status = ndb.StringProperty(choices=['queued', 'waiting', 'fetching', 'error', 'success'], default='queued')


class FetchedData(TransportModel):

	''' Keeps data after it has been fetched from a URL. '''

	operation = ndb.KeyProperty(required=True)
	status_code = ndb.IntegerProperty(default=200)
	final_url = ndb.StringProperty(default=None)
	content = ndb.BlobProperty()
	headers = ndb.PickleProperty()
	truncated = ndb.BooleanProperty(default=False)
