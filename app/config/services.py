# -*- coding: utf-8 -*-

"""

    ###################################### Services configuration. ######################################

    Configuration for the AppTools service layer, including a list of installed userland API services.


"""

import hashlib

config = {}

# Project Services
config['apptools.project.services'] = {

    'debug': False,    # Return extra debug info in responses
    'enabled': True,  # Disable API services system wide
    'logging': False,  # Logging for service request handling

    # Module-level (default) config (NOT IMPLEMENTED YET)
    'config': {

        'hmac_hash': hashlib.sha512,  # Hash algorithm to use for HMAC signatures
        'url_prefix': '/_api/rpc',  # Prefix for all service invocation URLs
        'secret_key': 'VNoibcXBx(*3&@!v1v1y2v2ob0(((hcd8hcdb8112',  # Secret key for generating HMAC signings

    },

    # Installed API's
    'services': {

        ## Debug, development, uptime, etc methods for infrastructure/testing/monitoring use
        'system': {
            'enabled': True,
            'service': 'apptools.services.builtin.SystemService',
            'methods': ['echo', 'hello', 'whoareyou', 'manifest'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Assets API - allows asset sync, AJAX access to asset URLs, and dynamic manifest access
        'assets': {
            'enabled': True,
            'service': 'apptools.services.builtin.AssetsService',
            'methods': ['image_url', 'script_url', 'style_url', 'blob_url', 'manifest', 'generate_upload_url'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Activity API - general and personal site activity.
        'activity': {
            'enabled': True,
            'service': 'openfire.services.activity.ActivityService',
            'methods': ['site_metrics', 'known_backers', 'known_followers'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Alerts API - used for managing subscriptions on site items
        'alerts': {
            'enabled': False,
            'service': 'openfire.services.alerts.AlertsService',
            'methods': ['subscribe', 'unsubscribe', 'edit', 'subscriptions', 'pending', 'all'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Auth API - allows async login/logout, session management, and related stuff
        'auth': {
            'enabled': False,
            'service': 'openfire.services.auth.AuthService',
            'methods': ['login', 'logout', 'session', 'request', 'verify', 'thirdparty', 'renew', 'signup'],

            'config': {
                'caching': 'none',
                'security': 'private',
                'recording': 'none'
            }
        },

        ## BBQ API - admin stuff (shhh!)
        'bbq': {
            'enabled': False,
            'service': 'openfire.services.bbq.BBQService',
            'methods': ['grant', 'revoke', 'flush_cache', 'create_user'],

            'config': {
                'caching': 'none',
                'security': 'private',
                'recording': 'none'
            }

        },

        ## Category API - provides structured information about openfire categories
        'category': {
            'enabled': True,
            'service': 'openfire.services.category.CategoryService',
            'methods': ['get', 'list', 'put', 'delete'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Content API - allows saving/retrieving of small content snippets
        'content': {
            'enabled': False,
            'service': 'openfire.services.content.ContentService',
            'methods': ['get', 'put', 'sync'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Indexer API - allows programmatic control of openfire's content indexer
        'indexer': {
            'enabled': False,
            'service': 'openfire.services.indexer.IndexerService',
            'methods': ['index', 'queued', 'purge', 'rebuild'],

            'config': {
                'caching': 'none',
                'security': 'private',
                'recording': 'none'
            }
        },

        ## Project API - provides structured information about openfire projects
        'project': {
            'enabled': True,
            'service': 'openfire.services.project.ProjectService',
            'methods': ['get', 'list', 'put', 'comment', 'comments', 'post', 'posts', 'add_media', 'media', 'follow', 'followers', 'backers', 'back', 'suspend', 'shutdown'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Proposal API - provides methods dealing with proposals for openfire projects
        'proposal': {
            'enabled': True,
            'service': 'openfire.services.proposal.ProposalService',
            'methods': ['get', 'list', 'put', 'comment', 'comments', 'promote', 'suspend', 'reject'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Realtime API - used for establishing/managing a realtime/push session
        'realtime': {
            'enabled': False,
            'service': 'openfire.services.realtime.RealtimeService',
            'methods': ['establish', 'renew', 'ping', 'manifest'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        },

        ## Search API - provides methods to retrieve/traverse quick/autocomplete/fulltext search results
        'search': {
            'enabled': False,
            'service': 'openfire.services.search.SearchService',
            'methods': ['quick', 'advanced', 'autocomplete'],

            'config': {
                'caching': 'none',
                'security': 'private',
                'recording': 'none'
            }
        },

        ## User API - allows user profiles/data and facepiles to be retrieved
        'user': {
            'enabled': False,
            'service': 'openfire.services.user.UserService',
            'methods': ['profile', 'account', 'follow', 'followers'],

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            }
        }

    }  # End services

}  # End services


## Global Services
config['apptools.services'] = {

    'logging': True,

    'hooks': {
        'appstats': {'enabled': False},  # RPC profiling
        'apptrace': {'enabled': False},  # memory usage profiling
        'profiler': {'enabled': False}   # CPU usage profiling
    },

    'mappers': [

        # Feed-Format Mappers
        {'name': 'RSS', 'enabled': False, 'path': 'apptools.services.mappers.RSSRPCMapper'},
        {'name': 'ATOM', 'enabled': False, 'path': 'apptools.services.mappers.ATOMRPCMapper'},

        # *RPC Mappers
        {'name': 'XMLRPC', 'enabled': False, 'path': 'apptools.services.mappers.XMLRPCMapper'},
        {'name': 'JSONRPC', 'enabled': True, 'path': 'apptools.services.mappers.JSONRPCMapper'},

        # Other Mappers
        {'name': 'Protobuf', 'enabled': True, 'path': 'apptools.services.mappers.ProtobufRPCMapper'},
        {'name': 'URLEncoded', 'enabled': True, 'path': 'apptools.services.mappers.URLEncodedRPCMapper'}

    ],

    'middleware': [

        ('authentication', {

            ## Configuration for authentication middleware

            'enabled': True,
            'debug': True,
            'path': 'apptools.services.middleware.AuthenticationMiddleware',
            'args': {

            }

        }),

        ('monitoring', {

            ## Configuration for monitoring middleware

            'enabled': True,
            'debug': True,
            'path': 'apptools.services.middleware.MonitoringMiddleware',
            'args': {

            }

        }),

        ('authorization', {

            ## Configuration for authorization middleware

            'enabled': True,
            'debug': True,
            'path': 'apptools.services.middleware.AuthorizationMiddleware',
            'args': {

            }

        }),

        ('caching', {

            ## Configuration for caching middleware

            'enabled': True,
            'debug': True,
            'path': 'apptools.services.middleware.CachingMiddleware',
            'args': {

            }

        })

    ],

    ## Configuration profiles that can be assigned to services
    'middleware_config': {

        ## Response + data caching middleware
        'caching': {

            'profiles': {

                ## No caching
                'none': {

                    'localize': False,
                    'default_ttl': None,  # Default Time-to-Live for cached items

                    'activate': {
                        'local': False,    # Local browser-side caching, if supported
                        'request': False,  # Caching of full API responses by hashed API requests
                        'internal': False  # Caching inside the remote service object
                    }

                },


                ## Cache things as they are pulled/used by clients
                'lazy': {

                    'localize': False,
                    'default_ttl': 60,

                    'activate': {
                        'local': False,
                        'request': True,
                        'internal': True
                    },

                },

                ## Cache things as they are used, but set low timeouts to avoid stale data
                'safe': {

                    'localize': False,
                    'default_ttl': 60,

                    'activate': {
                        'local': False,
                        'request': False,
                        'internal': True
                    }

                },

                ## Cache things before they are accessed, predictively, and with long timeouts
                'aggressive': {

                    'localize': False,
                    'default_ttl': 120,

                    'activate': {
                        'local': True,
                        'request': True,
                        'internal': True
                    }

                }

            },

            'default_profile': 'none'  # Default caching profile for APIs that don't specify one

        },

        ## Security and permissions enforcement middleware
        'security': {

            'profiles': {

                ## APIs with no security features
                'none': {

                    'expose': 'all',  # Whether to expose existence of this API to javascript clients

                    ## Client authentication
                    'authentication': {
                        'enabled': False
                    },

                    ## Client authorization
                    'authorization': {
                        'enabled': False
                    }

                },

                ## APIs marked public
                'public': {

                    'expose': 'all',

                    'authentication': {
                        'enabled': False,
                        'mode': None
                    },

                    'authorization': {
                        'enabled': False,
                        'mode': None
                    }

                },

                ## APIs marked private
                'private': {

                    'expose': 'admin',

                    'authentication': {
                        'enabled': False,
                        'mode': None
                    },

                    'authorization': {
                        'enabled': False,
                        'mode': None
                    }

                }

            },

            'default_profile': 'public'

        },

        ## Recording and logging middleware
        'recording': {

            'profiles': {

                'none': {
                    'mode': None
                },

                'minimal': {
                    'mode': None
                },

                'full': {
                    'mode': None
                },

                'debug': {
                    'mode': None
                }

            },

        },

    },

    ### Default config values
    'defaults': {

        'module': {},
        'service': {

            'config': {
                'caching': 'none',
                'security': 'none',
                'recording': 'none'
            },

            'args': {

            }

        }

    },

}
