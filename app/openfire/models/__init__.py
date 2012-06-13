# -*- coding: utf-8 -*-
## openfire models init.

from google.appengine.ext import ndb

class ModelMixin(object):

    def kind(self):
        return '__mixin__'


class MessageConverterMixin(ModelMixin):

    ''' Mixin class for automagically generating a ProtoRPC Message class from a model. '''

    def to_message(self, include=None, exclude=None):
        response = self._message_class()

        if self.key is not None:
            response.key = unicode(self.key.urlsafe())
        else:
            response.key = None

        for k, v in self.to_dict(include=include, exclude=exclude).items():
            if hasattr(response, k):
                if isinstance(v, ndb.Key):
                    setattr(response, k, v.urlsafe())
                else:
                    setattr(response, k, v)

        return response

    @classmethod
    def from_message(cls, message, key=None, **kwargs):

        if hasattr(message, 'key') and key is None:
            obj = cls(key=ndb.key.Key(urlsafe=message.key), **kwargs)
        elif key is not None and isinstance(key, ndb.key.Key):
            obj = cls(key=ndb.key.Key(urlsafe=key.urlsafe()), **kwargs)
        elif key is not None and isinstance(key, basestring):
            obj = cls(key=ndb.key.Key(urlsafe=key), **kwargs)
        else:
            obj = cls(**kwargs)

        for k, v in cls._properties.items():
            if k == 'key':
                continue
            if hasattr(message, k):
                try:
                    setattr(obj, str(k), getattr(message, k))

                except TypeError:
                    if k is not None and k not in [False, True, '']:

                        try:
                            setattr(obj, str(k), str(getattr(message, k)))
                        except TypeError:
                            continue

                else:
                    continue


        return obj
