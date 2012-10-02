# -*- coding: utf-8 -*-

"""

    ######################################## layer9 configuration. ########################################

"""

config = {}

config['layer9.appfactory'] = {

	'enabled': True,
	'logging': True,

	'headers': {
		'full_prefix': 'X-AppFactory',
		'compact_prefix': 'XAF',
		'use_compact': False
	}

}

config['layer9.appfactory.upstream'] = {

}

config['layer9.appfactory.frontline'] = {

	'debug': True

}

config['layer9.appfactory.controller'] = {

}
