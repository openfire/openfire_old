from google.appengine.ext import ndb
from openfire.models.sessions import UserSession


class SessionDataContainer(object):

	''' Deferred sessiondata container. '''

	def __init__(self, **kwargs):

		''' Provision data container. '''

		self._sid = None       # session ID
		self._init = False    # fulfilled flag
		self._data = {}       # session data
		self._dirty = {}      # dirty keys
		self._queue = []      # mutation ops
	
		## Accept SID, future + manager via kwargs
		self._sid = kwargs.get('sid')           # current session ID
		self._future = kwargs.get('future')    # ndb data future
		self._manager = kwargs.get('manager')  # session manager


	#### ++++ Internal Methods ++++ ####
	def _retrieve(self):

		''' Asyncronously retrieve session data for a given SID. '''

		return self._manager.get_data(self._sid)

	def _resolve(self, block=False):

		''' Lazy-load a SessionData entity. '''

		if self._init is False:  # we haven't even tried yet
			future = self._future = self._retrieve()
			self._init = True
			if block:
				self._data = future.get_result()
				self._future = True
				return self._data
			else:
				return future

		else:  # if we've already *tried* to get a session...
			if self._future is True:  # if we already have the full session...
				return self._data

			else:  # we've already tried, and we're still waiting
				if block:
					self._data = future.get_result()
					self._future = True
					return self._data
				else:
					return future

	def _get(self, name):

		''' Retrieve an item from session storage. '''

		if not name.startswith('_'):
			if self._init is False:  # first lazy-load access
				if name in self._dirty:  # could it be in the mutation queue?
					future = self._resolve(False)  # trigger an async get
					return self._queue[self._dirty[name]]  # we got lucky
				else:
					return self._resolve(True).get(name)
		else:
			return object.__getattribute__(self, name)

	def _set(self, name, value):

		''' Set an item in session storage. '''

		if not name.startswith('_'):
			if self._init is False:  # first lazy-load access
				future = self._resolve(False)  # trigger an async get
		else:
			return object.__setattr__(self, name, value)


	#### ++++ External Methods ++++ ####
	def __contains__(self, name):
	
		''' Returns True if the session contains the data point. '''
	
		if self._future:
			return name in self._data
		else:
			return name in self._retrieve(True)

	def __getattr__(self, name):
	
		''' `value = session.key` syntax '''
	
		return object.__getattribute__(self, '_get')(name)

	def __setattr__(self, name, value):
	
		''' `session.key = value` syntax '''
	
		return object.__getattribute__(self, '_set')(name, value)

	def __getitem__(self, name):

		''' `value = session[key]` syntax '''

		return object.__getattribute__(self, '_get')(name)

	def __setitem__(self, name, value):

		''' `session[key] = value` syntax '''

		return object.__getattribute__(self, '_set')(name, value)
