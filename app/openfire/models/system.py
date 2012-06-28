# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


## SystemProperty - used to store little values at runtime
class SystemProperty(ndb.Expando):

    ''' Sets a new system property, for persistently remembering random stuff. '''

    name = ndb.StringProperty(required=True, indexed=True)
    path = ndb.StringProperty(required=True, indexed=True)
    modified = ndb.DateTimeProperty('m', auto_now=True, indexed=True)
    created = ndb.DateTimeProperty('c', auto_now_add=True, indexed=True)
    # values set in expando at runtime

    @classmethod
    def set(cls, name, path, **kwargs):

        ''' Set + overwrite a system property, with an arbitrary amount of key=>value pairs. '''

        return cls(id=name, name=name, path=path, **kwargs).put()

    @classmethod
    def get(cls, name, path):

        ''' Gets a system property by name and path. '''

        return cls.get_by_id(name)
