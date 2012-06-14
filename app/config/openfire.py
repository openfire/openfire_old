# -*- coding: utf-8 -*-

"""

    ######################################## openfire configuration. ########################################

"""

config = {}

config['openfire'] = {
	
	'version': '__NULL__'

}

config['openfire.sessions'] = {
	
	'ttl': 300,  # timeout in seconds for stale session records
	'logging': True,  # enable logging if you want to know what's going on
	'cookieless': False,  # whether to enable cookieless (localstorage-based) sessions
	'salt': 'j09h8v9b&!V!V6vcvkcudv11',  # used for custom meals

	'frontends': {

		'cookies': {
			'ttl': '86400',
			'name': 'ofsession',
			'enabled': True
		},

		'localstorage': {
			'ttl': '86400',
			'name': 'ofsn',
			'enabled': False
		},

	},

	'backends': {

		'threadcache': {
			'ttl': '120',
			'enabled': False
		},

		'memcache': {
			'ttl': '1200',
			'enabled': True
		},

		'datastore': {
			'ttl': '2400',
			'enabled': True
		}

	}

}

config['openfire.classes.WebHandler'] = {
	
}