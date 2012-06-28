# -*- coding: utf-8 -*-
## openfire models init.

from google.appengine.ext import ndb


class ModelMixin(object):

    def kind(self):

        ''' Return a dummy kind name, because we're a mixin. '''

        return '__mixin__'


class PipelineTriggerMixin(ModelMixin):

    ''' Mixin class that provides pipeline-based model triggers. '''

    pass


class MessageConverterMixin(ModelMixin):

    ''' Mixin class for automagically generating a ProtoRPC Message class from a model. '''

    def to_message(self, include=None, exclude=None):

        ''' Convert an entity instance into a message instance. '''

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

        ''' Convert a message instance to an entity instance. '''

        if (hasattr(message, 'key') and message.key) and key is None:
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

    def mutate_from_message(self, message):

        ''' Copy all the attributes except the key from message to this object. '''

        for k in [f.name for f in message.all_fields()]:
            if k == 'key':
                continue
            if hasattr(self, k) and getattr(message, k):
                try:
                    setattr(self, str(k), getattr(message, k))
                except TypeError:
                    if k is not None and k not in [False, True, '']:
                        try:
                            setattr(self, str(k), str(getattr(message, k)))
                        except TypeError:
                            continue

                except:
                    # TODO: Handle other errors here?
                    try:
                        key = ndb.key.Key(urlsafe=getattr(message, k))
                        setattr(self, str(k), key)
                    except TypeError:
                        continue
                else:
                    continue
        return self


class AppModel(ndb.Model, MessageConverterMixin, PipelineTriggerMixin):

    ''' Abstract, top-level model for all openfire models. '''

    pass
