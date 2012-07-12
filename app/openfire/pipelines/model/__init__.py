# -*- coding: utf-8 -*-

from apptools.util import debug

from google.appengine.ext import ndb
from openfire.pipelines import AppPipeline


## ModelPipeline - abstract parent for all model-triggered pipelines
class ModelPipeline(AppPipeline):

    ''' Abstract parent for all model-triggered pipelines. '''

    _model_binding = None
    logging = debug.AppToolsLogger(path='openfire.pipelines.model', name='ModelPipeline')._setcondition(True)  # @TODO: hookup logging condition & extend/cache this

    def run(self, **kwargs):

        ''' Run a model action pipeline. '''

        key = None
        entity = None
        action = kwargs.get('action', 'heartbeat')  # default to heartbeat, which is idempotent and safe

        if 'key' in kwargs and action != 'delete':
            key = kwargs.get('key')
            if key:
                # import model
                m_path = self._model_binding.split('.')
                m = __import__('.'.join(m_path[0:-1]), globals(), locals(), [m_path[-1]])

                # build and get
                entity = ndb.Key(urlsafe=kwargs.get('key')).get()
                if not isinstance(entity, getattr(m, m_path[-1])):
                    self.logging.error('Loaded entity is not of proper bound type `%s`, but instead got `%s`.' % (self._model_binding, getattr(m, m_path[-1])))
                    self.logging.critical("Failed to execute triggered model pipeline.")
                    return 500
        else:
            if 'key' in kwargs:
                key = ndb.Key(urlsafe=kwargs.get('key'))

        if hasattr(self, action):
            method = getattr(self, action)

        if method is not None and entity is not None:
            return method(*[key, entity])

        else:
            return method(*[key])
