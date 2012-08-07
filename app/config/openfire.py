# -*- coding: utf-8 -*-

"""

    ######################################## openfire configuration. ########################################

"""

config = {}

config['openfire'] = {

    'version': '0.2-alpha'

}

config['openfire.meta'] = {

    'icon': 'https://d2ipw8y1masjpy.cloudfront.net/static/branding/icons/of_favicon_32x32.ico',
    'logo': 'https://d2ipw8y1masjpy.cloudfront.net/static/branding/openfire_transparent_optimized.png',
    'author': 'a collaboration between labor lapsus L3C + momentum labs',
    'publisher': 'openfire now!',
    'copyright': 'openfire, (c) 2012',
    'robots': 'index,follow',
    'revisit': '7 days',

    'description': 'openfire brings technologists, investors, developers and crowdfunders together around one thing: putting momentum behind disruptive innovation.',

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

config['openfire.security'] = {

    'config': {
        'cipher': 'AES',
        'pad16': True,
        'bad_logon_limit': 5,

        'wsec': {
            'hash': 'sha512',
        },

        'random': {
            'blocks': {
                'salt': """B#SE3!I@'zI*}U&O~dB?%~Q1zC9yhuP\D\t%i%58U'ol,|2l*+u|b,;\Gm=s?\V6B*'C[DGq"@"Oa;lOk#Uj}GZ~DYG$W;},E"cu/`((jn`70F43O\m>^j~mqAIKW~cbdIQg.>h0aVK*RU5a{n<Hlm{)1vGLG1}1V4HNXmCR-h>ah(`Q~}1xiHTTTDm8Gm`a3PNU!b&J<R[/V'#0z"]S8Of`Z:fR3{hdwm6-+@46Oowy}3vB@4&>D.@jOs3\JLJp""",
                'pepper': """;^-lmpd24h8ac5JxGq;+ph?&i]Ov;YvZ5kk~'>7tt!oFaBU{'lSVE+"*?:#i^y\b.]Sq3>j;XA{eF)tsVg!+Q4>LEA+[]N_sGwa?=g3jd3q4I)'t0G=$6s1t1VmS;B["}C'$e()Q84&_FMM#gQ!De.f1ci+C'j>/MUlv>aJZ81H%z&#5=Mq5x0y$6N.}~:n{py%B]j,,~r?sgG|}fra<KlI\S{ZT_Gmdbw:,JK|+8x9@p'_|3p&*>@GQ*DiS\mcT"""
            }
        },

        'extensions': {

            ## enable/disable openid and openid providers completely
            'openid': {
                'enabled': True
            },

            ## enable/disable oauth and oauth providers completely
            'oauth': {
                'enabled': True
            },

            ## enable/disable appengine/google integrated auth completely
            'appengine': {
                'enabled': True
            }

        }
    },

    ## openid-based logon
    'authentication': {

        ## enable/disable simple authentication
        'debug': False,
        'simple': False,
        'logging': False,

        'federation': {

            'enabled': True,

            'providers': [

                {'name': 'googleplus',
                    'label': 'Google',
                    'mode': 'openid',
                    'enabled': True,
                    'key': '483525084916-mvr4tcfceh2gfko0tvu7fcu3n1mg7kjp.apps.googleusercontent.com',
                    'secret': '1_1CnL7xof86FaCAk-Cu7Vnv',
                    'endpoint': 'www.google.com/accounts/o8/id'
                },

                {'name': 'facebook',
                    'label': 'Facebook',
                    'mode': 'oauth',
                    'enabled': True,
                    'key': '468309289847671',  # must match your App ID, above!
                    'secret': 'be5bb557db98c34e4959ab32cb7761c2',

                    'scopes': [

                        {'name': 'email', 'enabled': True},
                        {'name': 'user_about_me', 'enabled': True},
                        {'name': 'user_hometown', 'enabled': True},
                        {'name': 'user_interests', 'enabled': True},
                        {'name': 'user_likes', 'enabled': True},
                        {'name': 'user_location', 'enabled': True},
                        {'name': 'user_website', 'enabled': True},
                        {'name': 'publish_stream', 'enabled': True}

                    ]
                },

                {'name': 'github',
                    'label': 'GitHub',
                    'mode': 'oauth',
                    'enabled': False,
                    'key': '405567cb2d2d69fc4726',
                    'secret': '7d8016fed2e1294b0ff13de8ed71e73007a98e76',

                    'endpoints': {
                        'authorize': 'https://github.com/login/oauth/authorize',
                        'access_token': 'https://github.com/login/oauth/access_token'
                    }
                },

                {'name': 'linkedin',
                    'label': 'LinkedIn',
                    'mode': 'oauth',
                    'enabled': False,
                    'key': '',
                    'secret': ''
                },

                {'name': 'twitter',
                    'label': 'Twitter',
                    'mode': 'oauth',
                    'enabled': True,
                    'key': 'g33xdYigl64t87rF4NS2Q',
                    'secret': 'G6OyizYQDJTRVGmRbdKFDKiwRxJ8Dv0eTlE3KMMAk',

                    'endpoints': {
                        'token': 'https://api.twitter.com/oauth/request_token',
                        'authorize': 'https://api.twitter.com/oauth/authorize',
                        'access_token': 'https://api.twitter.com/oauth/access_token'
                    }
                },

                {'name': 'angellist',
                    'label': 'AngelList',
                    'mode': 'oauth',
                    'enabled': False,
                    'key': '',
                    'secret': ''
                }
            ]
        }

    },

    'encryption': {
        'simple': True,    # simple b64 encryption for development
        'advanced': False  # advanced AES symmetrical encryption for production
    }

}

config['openfire.multitenancy'] = {
    'enabled': True,
    'namespace': 'federated_auth'
}

config['openfire.output'] = {

    'extensions': {

        'config': {
            'enabled': True,
            'debug': False,
            'logging': True
        },

        'installed': {

            'FragmentCache': {
                'enabled': True,
                'path': 'openfire.core.output.extensions.fragment.FragmentCache'
            },

            'DynamicContent': {
                'enabled': True,
                'path': 'openfire.core.output.extensions.content.DynamicContent'
            },

            'ThreadedBytecodeCache': {
                'enabled': False,
                'path': 'openfire.core.output.extensions.bytecache.ThreadedBytecodeCache'
            },

            'MemcacheBytecodeCache': {
                'enabled': True,
                'path': 'openfire.core.output.extensions.memcache.MemcachedBytecodeCache'
            }
        }

    }

}

config['openfire.matcher'] = {

    'logging': True,

}

config['openfire.classes.WebHandler'] = {

    'debug': False,
    'logging': True,

    'integrations': {

        'gravatar': {
            'enabled': True,
            'endpoints': {
                'http': 'www.gravatar.com',
                'https': 'secure.gravatar.com'
            }
        }

    },

    'extensions': {
        'load': ['FragmentCache', 'DynamicContent', 'MemcacheBytecodeCache']
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
        }

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
    'trigger_queue': 'trigger'  # task queue to send pipelines to

}
