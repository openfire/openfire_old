# -*- coding: utf-8 -*-
import config
from google.appengine.ext import ndb


class UserSession(ndb.Model):

	''' Represents a user session. '''

	_SESSION_TTL = config.config.get('openfire.sessions').get('ttl', 300)

	sid = ndb.StringProperty('s', required=True, indexed=False)
	data = ndb.JsonProperty('d', compressed=True)
	addr = ndb.StringProperty('a', required=True, indexed=True)
	user = ndb.KeyProperty('u', required=False, indexed=True, default=None)
	touched = ndb.DateTimeProperty('t', auto_now=True, indexed=True)
	established = ndb.DateTimeProperty('e', auto_now_add=True, indexed=False)
