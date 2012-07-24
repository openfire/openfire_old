# -*- coding: utf-8 -*-

''' main.py - everything starts here. '''

try:
    import bootstrap
    bootstrap.AppBootstrapper.prepareImports()  # fix imports
except ImportError:
    pass

import warmup as w
from pipeline.handlers import _APP as pipeline_wsgi
from apptools import dispatch


def main(environ=None, start_response=None):

    ''' INCEPTION! :) '''

    return dispatch.gateway(environ, start_response)


def warmup(environ=None, start_response=None):

    ''' Instance warmup '''

    return w.Warmup(environ, start_response)


def backend(environ=None, start_response=None):

    ''' Backend warmup '''

    return w.Warmup(environ, start_response)


def pipelines(environ=None, start_response=None):

    ''' GAE Pipelines '''

    return pipeline_wsgi(environ, start_response)

if __name__ == '__main__':
    main()
