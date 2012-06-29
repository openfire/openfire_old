# -*- coding: utf-8 -*-

''' main.py - everything starts here. '''

try:
    import bootstrap
    bootstrap.AppBootstrapper.prepareImports()  # fix imports
except ImportError:
    pass

import warmup as w
from apptools import dispatch


def main(environ=None, start_response=None):

    ''' INCEPTION! :) '''

    return dispatch.gateway(environ, start_response)


def warmup(environ=None, start_response=None):

    ''' Instance warmup '''

    return w.Warmup(environ, start_response)

if __name__ == '__main__':
    main()
