# -*- coding: utf-8 -*-
"""

    ###################################### Asset configuration. ######################################

    ~~~  Description:  ~~~

    In this config file, you can specify registered assets for use in the AppTools Assets API.
    This all corresponds to the directory structure under app/assets. Place your static files in
    app/assets/< js | style | ext >/static, and then register them in the proper section below.

    If you register your scripts, stylesheets, and other stuff here, you can generate URLs to your
    static content directly in the template, handler, service, model or pipeline!


    ~~~ Generating Asset URLs ~~~

    In a template:
        {{ asset.script('jquery', 'core') }}   ## library first, package second (see below for definitions)

    In a handler/pipeline/service/model:
        self.get_script_url('jquery', 'core')  ## generated asset URLs honor output settings (e.g. CDN)


    ~~~ Package Config Structure ~~~

    '<type>': {

        ('<package name>', '<type/subdirectory/path>'): {

            'config': {
                'min': True | False,                    # whether it's possible to serve a minified version of this asset (converts filename to <name>.min.<type>. turn on minified assets in output config to activate)
                'version_mode': '<getvar | filename>',  # whether to add the package's version to the URL as a getvar or as part of the filename
                'bundle': '<your.bundle.js>'            # a name for your bundle, so you can combine assets and serve the optimized version if you want
            },

            'assets': {
                '<asset name>': {'min': True | False, 'version': '<version>'},  # override package `min` value, and specify the package version for cachebusting, when versioning is activated
            }

        }

"""
config = {}


# Installed Assets
config['apptools.project.assets'] = {

    'debug': False,    # Output log messages about what's going on.
    'verbose': False,  # Raise debug-level messages to 'info'.

    # JavaScript Libraries & Includes
    'js': {


        ### Core Dependencies ###
        ('core', 'core'): {

            'config': {
                'version_mode': 'getvar',
                'bundle': 'core.bundle.min.js'
            },

            'assets': {
                'modernizr': {'min': False, 'version': '2.0.6-c'},          # Modernizr - browser polyfill + compatibility testing
                'jquery': {'min': True, 'version': '1.8.0'},                # jQuery: Write Less, Do More!
                'jquery-full': {'min': True, 'version': '1.8.0', 'name': 'jquery.full'},
                'd3': {'name': 'd3.v2', 'min': True, 'version': '2.9.6'},   # D3 - Visualizations
                'jacked': {'min': True, 'version': '1.0'},                  # Jacked - tweening animation engine
            }

        },

        ### AppToolsJS ###
        ('apptools', 'apptools'): {

            'config': {
                'version_mode': 'getvar',
                'bundle': 'apptools.bundle.min.js'
            },

            'assets': {
                'base': {'min': True, 'version': 1.5},  # RPC, events, dev, storage, user, etc (see $.apptools)
                'admin': {'name': 'base.admin', 'min': True, 'version': 1.5}  # RPC, events, dev, storage, user, etc (see $.apptools)
            }

        },

        ### Openfire ###
        ('openfire', 'openfire'): {

            'config': {
                'version_mode': 'getvar',
                'bundle': 'openfire.bundle.min.js'
            },

            'assets': {
                'app': {'min': True, 'version': 0.3},  # openfire app base
                'admin': {'name': 'app.admin', 'min': True, 'version': 0.3}  # openfire app base for admins
            }

        },

        ### jQuery Plugins ###
        ('jquery', 'core/jquery'): {

            'config': {
                'version_mode': 'getvar',
                'bundle': 'jquery.bundle.min.js'
            },

            'assets': {
                ## jquery core is included in "core" (see above)
                'easing': {'path': 'interaction/easing.min.js'},          # Easing transitions for smoother animations
                'mousewheel': {'path': 'interaction/mousewheel.min.js'},  # jQuery plugin for mousewheel events + interactions
                'scrollsuite': {'path': 'interaction/scroller.min.js'},   # ScrollTo, LocalScroll & SerialScroll
                'fancybox': {'path': 'interaction/fancybox2.min.js'}      # Clean + responsive CSS3 modals (note: needs a license for commercial apps)
            }

        },

    },


    # Cascading Style Sheets
    'style': {

        # Source (SASS) Stylesheets
        ('source', 'source'): {

            'assets': {

                ## Core
                'base': {'name': '_base.sass', 'module': '_core', 'version': 0.2},
                'h5bp': {'name': '_h5bp.sass', 'module': '_core', 'version': 0.2},
                'init': {'name': '_initializer.sass', 'module': '_core', 'version': 0.3},
                'config': {'name': '_config.sass', 'module': '_core', 'version': 0.2},
                'fonts': {'name': '_fonts.sass', 'module': '_core', 'version': 0.2},
                'media': {'name': '_mediaqueries.sass', 'module': '_core', 'version': 0.2},
                'print': {'name': '_print.sass', 'module': '_core', 'version': 0.2},

                ## Partials
                'social': {'name': '_social.sass', 'module': '_partials', 'version': 0.2},
                'widgets': {'name': '_widgets.sass', 'module': '_partials', 'version': 0.2},
                'superbar': {'name': '_superbar.sass', 'module': '_partials', 'version': 0.2},
                'loginbox': {'name': '_loginbox.sass', 'module': '_partials', 'version': 0.2},

                ## Openfire
                'bbq': {'name': 'bbq.sass', 'module': 'openfire', 'version': 0.2},
                'landing': {'name': 'landing.sass', 'module': 'openfire', 'version': 0.2},
                'profile': {'name': 'profile.sass', 'module': 'openfire', 'version': 0.2},
                'project': {'name': 'project.sass', 'module': 'openfire', 'version': 0.2},

                ## Main
                'ie': {'name': 'ie.sass', 'version': 0.2},
                'bbq': {'name': 'bbq.sass', 'version': 0.2},
                'main': {'name': 'main.sass', 'version': 0.2},
                'admin': {'name': 'admin.sass', 'version': 0.2},
                'mobile': {'name': 'mobile.sass', 'version': 0.2},
                'jasmine': {'name': 'jasmine.sass', 'version': 0.2},
                'security': {'name': 'security.sass', 'version': 0.2},

            }

        },

        # Compiled (CSS) Stylesheets
        ('compiled', 'compiled'): {

            'config': {
                'min': True,
                'version_mode': 'getvar'
            },

            'assets': {
                'main': {'version': 0.4},  # reset, main, layout, forms
                'ie': {'version': 0.4},    # fixes for internet explorer (grrr...)
                'print': {'version': 0.4},  # proper format for printing
                'admin': {'version': 0.4},   # admin
                'security': {'version': 0.3}  # login/register/etc
            }

        },

        # Content-section specific stylesheets
        ('openfire', 'compiled/openfire'): {

            'config': {
                'min': True,
                'version_mode': 'getvar'
            },

            'assets': {
                'landing': {'version': 0.5},  # styles for the landing
                'proposal': {'version': 0.2},  # styles for the proposal page
                'project': {'version': 0.4},  # styles for the project page
                'profile': {'version': 0.3}   # styles for the profile page
            }

        },

    },


    # Other Assets
    'ext': {
     },

}


config['js.loader'] = {

    # loader config
    "config": {

        "enabled": False,
        "autoload": False,
        "modules": ['search', 'picker', 'visualization'],
        "externals": ['channel', 'maps_v3', 'plusone', 'fbjssdk'],

        "context": {
            "key": "AIzaSyAtnLmsmOnkw8NQZROonSjvam6KqaD3UY0",
            "appid": "468309289847671"
        }

    },

    # external JS scripts
    "external": [

        ("fbjssdk", "//connect.facebook.net/en_US/all.js#xfbml=1&appId=%(appid)s"),
        ("maps_v3", "//maps.googleapis.com/maps/api/js?key=%(key)s&sensor=false"),
        ("channel", "//open-fire-staging.appspot.com/channel.js?s=%(sid)s"),
        ("plusone", "//apis.google.com/js/plusone.js")

    ],

    # loader-compatible modules
    "modules": [

        {
            "name": "search",
            "version": "1.0",
            "language": "en"
        },

        {
            "name": "maps",
            "version": "2.x",
            "language": "en"
        },

        {
            "name": "feeds",
            "version": "1.0",
            "language": "en"
        },

        {
            "name": "language",
            "version": "1.0",
            "language": "en",
        },

        {
            "name": "data",
            "version": "1.0",
            "language": "en",
        },

        {
            "name": "earth",
            "version": "1.0",
            "language": "en",
        },

        {
            "name": "visualization",
            "version": "1.0",
            "language": "en",
            "packages": [

                'corechart',
                'geochart',
                'map',
                'table'

            ]
        },

        {
            "name": "picker",
            "version": "1.0",
            "language": "en",
        }

    ]

}
