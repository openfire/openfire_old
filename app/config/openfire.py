# -*- coding: utf-8 -*-

"""

    ######################################## openfire configuration. ########################################

"""

config = {}

config['openfire'] = {

    'version': '0.1-alpha'

}

config['openfire.meta'] = {

    'icon': '',
    'logo': '',
    'author': 'a collaboration between labor lapsus L3C + momentum labs',
    'publisher': 'openfire now!',
    'copyright': 'openfire, (c) 2012',
    'robots': 'index,follow',
    'revisit': '7 days',

    'description': '',

    'keywords': [
        'positive disruption',
        'innovation',
        'technology',
        'crowdfunding',
        'entrepreneurship',
        'social good',
        'small business'
    ],

    'opengraph': {

        'title': 'openfire: momentum for positive disruption!',
        'type': 'website',
        'determiner': 'a',
        'locale': 'en_US',
        'url': 'https://openfi.re',
        'site_name': 'openfire',

        'location': {
            'latitude': '37.751185',
            'longitude': '-122.442443',
            'address': '531 Grand View Avenue',
            'locality': 'San Francisco',
            'region': 'California',
            'zipcode': '94114',
            'country': 'United States of America',
            'email': 'disrupt@openfi.re',
            'phone': '(866) 252-0640'
        },

        'facebook': {
            'app_id': '468309289847671',
            'admins': ['642005650']
        }

    },

    'apple': {

        'touch_icon': '',
        'precomposed': '',
        'startup_icon': '',
        'status_bar_style': '',
        'app_capable': ''

    },

    'google': {

        'site_verification': ''

    }

}

config['openfire.sessions'] = {

    'ttl': 86400,  # timeout in seconds for stale session records
    'logging': False,  # enable logging if you want to know what's going on
    'cookieless': True,  # whether to enable cookieless (localstorage-based) sessions
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

    'debug': False,
    'logging': False

}

config['openfire.datamodel'] = {

    'namespacing': {
        'enabled': False,
        'mode': 'appversion'
    }

}

config['openfire.datamodel.integration.pipelines'] = {

    'enable': True,  # enable/disable pipelines integration
    'logging': False,  # enable/disable logging
    'autostart': False,  # automatically kick off bound pipelines
    'trigger_queue': 'default'  # task queue to send pipelines to

}
