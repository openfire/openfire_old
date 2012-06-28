# -*- coding: utf-8 -*-
import config

from openfire.models import AppModel
from google.appengine.ext import ndb


class UserSession(ndb.Model):

	''' Represents a user session. '''

	_SESSION_TTL = config.config.get('openfire.sessions').get('ttl', 300)

	sid = ndb.StringProperty('s', required=True, indexed=False)
	data = ndb.JsonProperty('d', compressed=True)
	addr = ndb.StringProperty('a', required=True, indexed=True)
	user = ndb.KeyProperty('u', required=False, indexed=True, default=None)
	touched = ndb.DateTimeProperty('t', auto_now=True, indexed=True)

class SessionData(ndb.Model):

	''' Stores data about a session. '''

	session = ndb.KeyProperty('s', required=True, indexed=True)
	csrf = ndb.StringProperty('csrf', repeated=True, indexed=True)
	data = ndb.JsonProperty('d', compressed=True)
	addr = ndb.StringProperty('a', required=True, indexed=True)
	touched = ndb.DateTimeProperty('t', auto_now=True, indexed=True)
	created = ndb.DateTimeProperty('c', auto_now_add=True, indexed=True)
	user = ndb.KeyProperty('u', required=False, indexed=True, default=None)
	authenticated = ndb.BooleanProperty('ath', default=False, indexed=True)
	events = ndb.KeyProperty('e', repeated=True, indexed=True)
	established = ndb.DateTimeProperty('e', auto_now_add=True, indexed=False)
