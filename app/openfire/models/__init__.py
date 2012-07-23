# -*- coding: utf-8 -*-
## openfire models init.

# Base Imports
import config
import webapp2

# AppTools Imports
from apptools.util import debug

# External Imports
from google.appengine.ext import ndb
from google.appengine.ext.ndb import eventloop

# Openfire Imports
from openfire.pipelines.model import ModelPipeline


## ModelMixin - abstract parent object for model mixin classes
class ModelMixin(object):

    pass


## PipelineTriggerMixin - allows bound pipelines to be constructed and started automatically when NDB hooks fire on models
class PipelineTriggerMixin(ModelMixin):

    ''' Mixin class that provides pipeline-based model triggers. '''

    _pipeline_class = None

    ### === Internal Properties === ###
    __config = config.config.get('openfire.datamodel.integration.pipelines', {})
    __logging = debug.AppToolsLogger('openfire.datamodel.mixins', 'PipelineTriggerMixin')._setcondition(__config.get('logging', False))

    ### === Internal Methods === ###
    @classmethod
    def _construct_hook_pipeline(cls, action, **kwargs):

        ''' Conditionally trigger a hooked model-driven pipeline. '''

        if hasattr(cls, '_pipeline_class'):
            if cls._pipeline_class is not None:
                if issubclass(cls._pipeline_class, ModelPipeline):
                    cls.__logging.info('Valid pipeline found for model `%s`.' % cls)
                    if hasattr(cls._pipeline_class, action):
                        cls.__logging.info('Pipeline has hook for action `%s`.' % action)

                        ## build pipeline params
                        kwargs['action'] = action

                        ## build pipeline
                        return cls._pipeline_class(**kwargs)

                    else:
                        cls.__logging.info('Pipeline does not have a hook defined for action `%s`.' % action)
                        return

                else:
                    cls.__logging.error('Model-attached pipeline (on model "%s") is not an instance of ModelPipeline (of type "%s").' % (cls, cls._pipeline_class))
                    return
        else:
            cls.__logging.info('No hooked pipeline detected for model "%s" on action "%s".' % (cls, action))
        return

    @classmethod
    def _trigger_hook_pipeline(cls, action, start=False, **kwargs):

        ''' Try to construct a pipeline for a given trigger hook, and optionally start it. '''

        if action not in frozenset(['put', 'delete']):
            cls.__logging.warning('Triggered NDB hook action is not `put` or `delete`. Ignoring.')
            return
        else:
            cls.__logging.info('Valid hook action for potential pipeline hook. Trying to construct/resolve.')
            p = cls._construct_hook_pipeline(action, **kwargs)
            cls.__logging.info('Got back pipeline: `%s`.' % p)
            if p:
                if start:
                    cls.__logging.info('Starting hooked pipeline...')
                    pipeline = p.start(queue_name=cls.__config.get('trigger_queue', 'default'))
                    cls.__logging.info('Hooked pipeline away: "%s"' % pipeline)
                    return pipeline
                cls.__logging.info('Autostart is off. NOT starting constructed pipeline.')
                return p
            else:
                cls.__logging.error('Could not construct pipeline! :(')
                return
        return

    ### === Hook Methods === ###
    def _pipelines_post_put_hook(self, future):

        ''' This hook is run after an AppModel is put using NDB. '''

        cls = self.__class__
        if cls.__config.get('enable', False):
            cls.__logging.info('Pipelines-NDB integration hooks enabled.')
            cls._trigger_hook_pipeline('put', cls.__config.get('autostart', False), key=self.key.urlsafe())
        else:
            cls.__logging.info('Pipelines-NDB integration hooks disabled.')
        return

    @classmethod
    def _pipelines_post_delete_hook(cls, key, future):

        ''' This hook is run after an AppModel is deleted using NDB. '''

        if cls.__config.get('enable', False):
            cls.__logging.info('Pipelines-NDB integration hooks enabled.')
            cls._trigger_hook_pipeline('delete', cls.__config.get('autostart', False), key=key.urlsafe())
        else:
            cls.__logging.info('Pipelines-NDB integration hooks disabled.')
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

        def _convert_prop(v):

            if isinstance(v, ndb.Key):
                return v.urlsafe()
            elif hasattr(v, 'isoformat'):
                return v.isoformat()
            else:
                if isinstance(v, (tuple, list)):
                    values = []
                    for i in v:
                        values.append(_convert_prop(v))
                    return values

        for k, v in self.to_dict(include=include, exclude=exclude).items():
            if hasattr(response, k):
                setattr(response, k, _convert_prop(v))

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

    def _post_put_hook(self, future):

        ''' Post-put hook. '''

        self._pipelines_post_put_hook(future)

    @classmethod
    def _post_delete_hook(cls, key, future):

        ''' Post-delete hook. '''

        cls._pipelines_post_delete_hook(key, future)
