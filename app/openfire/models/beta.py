# -*- coding: utf-8 -*-

# Datastore Imports
from google.appengine.ext import ndb
from openfire.models import AppModel

from openfire.messages import beta as messages
from openfire.pipelines.model import beta as pipelines


class Signup(AppModel):

    ''' A user who signed up to be notified of openfire's release! '''

    _message_class = messages.BetaSignup
    _pipeline_class = pipelines.BetaSignupPipeline

    firstname = ndb.StringProperty('f', required=True, indexed=True)
    lastname = ndb.StringProperty('l', default=None, indexed=True)
    email = ndb.StringProperty('e', required=True, indexed=True)
    token = ndb.KeyProperty('t', required=True, indexed=True)
    modified = ndb.DateTimeProperty('m', auto_now=True, indexed=False)
    created = ndb.DateTimeProperty('c', auto_now_add=True, indexed=True)


class InviteToken(AppModel):

	''' An invite, generated for a Signup or manually. '''

	token = ndb.StringProperty('t', required=True, indexed=True)
	signup = ndb.KeyProperty('s', default=None, indexed=True)
	used = ndb.BooleanProperty('u', default=False)
	sent = ndb.BooleanProperty('e', default=False)
	modified = ndb.DateTimeProperty('m', auto_now=True, indexed=False)
	created = ndb.DateTimeProperty('c', auto_now_add=True, indexed=True)
