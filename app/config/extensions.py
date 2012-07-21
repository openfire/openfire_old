# -*- coding: utf-8 -*-

"""

    ######################################## output extension configuration. ########################################

"""

config = {}

## DynamicContent extension - manages injection of dynamic, editable content into template AST's
config['openfire.output.extension.DynamicContent'] = {

    'debug': True,
    'enabled': True,
    'logging': True,

    'config': {
        'default_namespace': '::'.join(['of', 'tpl', 'dynamic', 'system'])
    }

}

## FragmentCache extension - makes caching possible in the template via a {% cache %} tag
config['openfire.output.extension.FragmentCache'] = {

    'debug': True,
    'enabled': True,
    'logging': True,

    'config': {
        'timeout': 1200,  # default timeout of 5 minutes
        'prefix': '::'.join(['of', 'tpl', 'source', 'fragment'])
    }

}

## ThreadedBytecodeCache extension - caches compiled template bytecode in thread memory
config['openfire.output.extension.ThreadedBytecodeCache'] = {

    'debug': True,
    'enabled': True,
    'logging': True,

    'config': {
        'timeout': 1200,  # default timeout of 5 minutes
        'prefix': '::'.join(['of', 'tpl', 'bytecode', 'tcache'])
    }

}

## MemcachedBytecodeCache extension - caches compiled template bytecode in memcache
config['openfire.output.extension.MemcachedBytecodeCache'] = {

    'debug': True,
    'enabled': True,
    'logging': True,

    'config': {
        'timeout': 1200,
        'prefix': '::'.join(['of', 'tpl', 'bytecode', 'mcache'])
    }

}
