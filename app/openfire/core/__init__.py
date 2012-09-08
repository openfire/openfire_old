# -*- coding: utf-8 -*-
#from apptools.util import platform


#@platform.PlatformInjector
class CoreAPI(object):

	''' Abstract parent to all openfire core APIs. '''

	pass


def construct_enum(*sequence, **names):

    ''' Helper function to construct an enum that we can use for things like error codes. '''

    return type('Enum', (), dict(zip(sequence, range(len(sequence))), **names))
