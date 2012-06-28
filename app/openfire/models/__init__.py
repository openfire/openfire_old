# -*- coding: utf-8 -*-
## openfire models init.

# Base Imports
import config
import webapp2

# AppTools Imports
from apptools.util import debug

# External Imports
from google.appengine.ext import ndb

# Openfire Imports
from openfire.pipelines.model import ModelPipeline


## ModelMixin - abstract parent object for model mixin classes
class ModelMixin(object):

    def kind(self):

        ''' Return a dummy kind name, because we're a mixin. '''

        return '__mixin__'


## PipelineTriggerMixin - allows bound pipelines to be constructed and started automatically when NDB hooks fire on models
class PipelineTriggerMixin(ModelMixin):

    ''' Mixin class that provides pipeline-based model triggers. '''

    _pipeline_class = None

    ### === Internal Properties === ###
    @webapp2.cached_property
    def __config(self):

        ''' Private cached shortcut to config. '''

        return config.config.get('openfire.datamodel.integration.pipelines', {})

    @webapp2.cached_property
    def __logging(self):

        ''' Private cached shortcut to logging pipe. '''

        return debug.AppToolsLogger('openfire.datamodel.mixins', 'PipelineTriggerMixin')._setcondition(self.__config.get('logging', False))

    ### === Internal Methods === ###
    def _construct_hook_pipeline(self, action):

        ''' Conditionally trigger a hooked model-driven pipeline. '''

        if hasattr(self, '_pipeline_class'):
            if self._pipeline_class is not None:
                if isinstance(self.__pipeline_class, ModelPipeline):
                    if hasattr(self._pipeline_class, action):
                        self.__logging.info('Pipeline has hook for action `%s`.' % action)
                        return self._pipeline_class(**{
                            'key': self.key.urlsafe(),
                            'action': action
                        })
                    else:
                        self.__logging.error('Model-attached pipeline (on model "%s") is not an instance of ModelPipeline (of type "%s").' % (self, self.__pipeline_class))
                        return
        else:
            self.__logging.info('No hooked pipeline detected for model "%s" on action "%s".' % (self, action))
        return

    def _trigger_hook_pipeline(self, action, start=False):

        ''' Try to construct a pipeline for a given trigger hook, and optionally start it. '''

        if action not in frozenset(['put', 'delete']):
            self.__logging.warning('Triggered NDB hook action is not `put` or `delete`. Ignoring.')
            return
        else:
            self.__logging.info('Valid hook action for potential pipeline hook. Trying to construct/resolve.')
            p = self._construct_hook_pipeline(action)
            if p is not None:
                if start:
                    self.__logging.info('Starting hooked pipeline...')
                    pipeline = p.start(self.__config.get('trigger_queue', 'default'))
                    self.__logging.info('Hooked pipeline away: "%s"' % pipeline)
                    return pipeline
                return p
        return

    ### === Hook Methods === ###
    def _post_put_hook(self):

        ''' This hook is run after an AppModel is put using NDB. '''

        if self.__config.get('enable', False):
            self.__logging.info('Pipelines-NDB integration hooks enabled.')
            self._trigger_hook_pipeline('put', self.__config.get('autostart', False))
        return

    def _post_delete_hook(self):

        ''' This hook is run after an AppModel is deleted using NDB. '''

        if self.__config.get('enable', False):
            self.__logging.info('Pipelines-NDB integration hooks enabled.')
            self._trigger_hook_pipeline('delete', self.__config.get('autostart', False))
        return


## MessageConverterMixin - allows us to automatically convert an NDB model to or from a bound ProtoRPC message class
class MessageConverterMixin(ModelMixin):

    ''' Mixin class for automagically generating a ProtoRPC Message class from a model. '''

    _message_class = None

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


## AppModel - abstract parent class to all openfire app models, brings together mixins, default functions and default properties
class AppModel(ndb.Model, MessageConverterMixin, PipelineTriggerMixin):

    ''' Abstract, top-level model for all openfire models. '''

    # NDB Cache Policy
    _use_cache = True
    _use_memcache = True
    _use_datastore = True

    # Timestamps
    modified = ndb.DateTimeProperty('_tm', auto_now=True, indexed=True)
    created = ndb.DateTimeProperty('_tc', auto_now_add=True, indexed=True)
