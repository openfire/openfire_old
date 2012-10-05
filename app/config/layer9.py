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

	'debug': True,
	'enabled': True,

	'preloading': {
		'gather_assets': True,
		'enable_spdy_push': True,
		'enable_link_fallback': True
	},

	'spdy': {

		'push': {

			'assets': {
				'force_priority': False,
				'default_priority': 7
			}

		}

	}

}

config['layer9.appfactory.frontline'] = {

	'debug': True,
	'enabled': True

}

config['layer9.appfactory.controller'] = {

	'debug': True,
	'enabled': True

}
