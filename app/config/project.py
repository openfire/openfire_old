# -*- coding: utf-8 -*-

"""

    ######################################## AppTools Project configuration. ########################################

    Main project configuration stuff, designed to be changed according to the app's desired environment and status.

"""

config = {}


## App settings
config['apptools.project'] = {

    'name': 'openfire',        # Change this to your app's name

    'version': {               # Change this according to your app's version
        'major': 0,
        'minor': 2,
        'micro': 0,
        'build': 20120911,
        'release': 'ALPHA'
    }

}

## Development/debug settings
config['apptools.project.dev'] = {
  # Not yet in use
}

## Output layer settings
config['apptools.project.output'] = {

    # Output Configuration

    'minify': True,      # whether to minify page output or not
    'optimize': True,     # whether to use the async script loader or not
    'standalone': False,  # whether to render only the current template, or the whole context (ignores "extends")

    'analytics': {  # Analytics Settings
        'enable': True,              # whether to insert analytics code
        'multitrack': True,			 # whether to enable support for multiple trackers
        'anonymize': False,			 # whether to anonymize IPs before analytics
        'account_id': {
            'dev': 'UA-31611943-3',         # used when running from the devserver
            'staging': 'UA-31611943-2',    # used on the staging version of the site
            'production': 'UA-31611943-1'  # used on the production version of the site
        },
        'webclient':{
            'dev': 'https://ssl.google-analytics.com/u/ga_debug.js',
            'http': 'https://deliver.openfi.re/analytics/ga.js',
            'https': 'https://deliver.openfi.re/analytics/ga.js'
        }
    },

    'appcache': {  # HTML5 appcaching
        'enable': False,                       # whether to enable
        'manifest': 'scaffolding-v1.appcache'  # manifest to link to
    },

    'assets': {  # Asset API
        'minified': True,        # whether to switch to minified assets or not
        'serving_mode': 'local',  # 'local' or 'cdn' (CDN prefixes all assets with an absolute URL)
        'cdn_prefix': ['d2d3v83fgqizie.cloudfront.net']          # CDN prefix/prefixes - a string is used globally, a list of hostnames is selected from randomly for each asset
    },

    'headers': {  # Default Headers (only supported headers are shown)
        'Cache-Control': 'no-cache',  # default to not caching dynamic content
        'X-UA-Compatible': 'IE=edge,chrome=1',  # http://code.google.com/chrome/chromeframe/
        'Access-Control-Allow-Origin': '*.openfi.re *.lyr9.net beta.openfi.re staging.openfi.re'      # allow crossdomain access from anywhere
    }

}

## Caching
config['apptools.project.cache'] = {

    # Caching Configuration

    'key_seperator': '::',
    'prefix': 'dev',
    'prefix_mode': 'explicit',
    'prefix_namespace': False,
    'namespace_seperator': '::',

    'adapters': {

        # Instance Memory
        'fastcache': {
            'default_ttl': 600
        },

        # Memcache API
        'memcache': {
            'default_ttl': 10800
        },

        # Backend Instance Memory
        'backend': {
            'default_ttl': 10800
        },

        # Datastore Caching
        'datastore': {
            'default_ttl': 86400
        }

    }

}

config['apptools.project.output.template_loader'] = {

    # Template Loader Config

    'force': True,              # Force enable template loader even on Dev server
    'debug': True,             # Enable dev logging
    'use_memory_cache': False,  # Use handler in-memory cache for template source
    'use_memcache': False,      # Use Memcache API for template source

}

# Pipelines Configuration
config['apptools.project.pipelines'] = {

    'debug': False,  # Enable basic serverlogs
    'logging': {

        'enable': False,       # Enable the pipeline logging subsystem
        'mode': 'serverlogs',  # 'serverlogs', 'xmpp' or 'channel'
        'channel': '',         # Default channel to send to (admin channels are their email addresses, this can be overridden on a per-pipeline basis in the dev console)
        'jid': '',             # Default XMPP JID to send to (this can be overridden on a per-pipeline basis in the dev console)

    }

}
