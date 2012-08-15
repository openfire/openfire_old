# -*- coding: utf-8 -*-
import config
import webapp2

class NamespaceBridge(object):

    ''' Used to put all our datastore data into a namespace. '''

    @webapp2.cached_property
    def _namespace_config(self):

        ''' Cached access to multitenancy config for this handler. '''

        return config.config.get('openfire.multitenancy', {})

    def prepare_namespace(self, request):

        ''' Set the namespace for this request. '''

        if self._namespace_config.get('enabled', False):
            current_version = request.environ.get('CURRENT_VERSION_ID')
            # If the current version is not set, this is probably a test, so don't set a namespace.
            if current_version:
                version_namespace = current_version.split('-')[0]

                # if no manually-provided namespace is available, default to the app's current macro version
                if self._namespace_config.get('namespace', None) is None:
                    self.logging.info('Setting datastore namespace to "%s".' % version_namespace)
                    self.api.multitenancy.set_namespace(self._namespace_config.get('namespace', version_namespace))
                    return

                # else, set the namespace that is set in config
                else:
                    self.logging.info('Setting dev datastore namespace to "%s".' % self._namespace_config.get('namespace'))
                    self.api.multitenancy.set_namespace(self._namespace_config.get('namespace'))
                    return
