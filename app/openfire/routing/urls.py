# -*- coding: utf-8 -*-

"""

    URL definitions.

"""

from webapp2 import Route

from webapp2_extras.routes import PathPrefixRoute
from webapp2_extras.routes import HandlerPrefixRoute

rules = [

    HandlerPrefixRoute('openfire.handlers.', [

        ## === Main URLs === ##
        Route('/', name='landing', handler='main.Landing'),
        Route('/offline', name='offline', handler='main.Offline'),

        ## Temporary dev URLS
        Route('/_dev/data', name='default/data', handler='dev.DevModels'),
        Route('/_dev/jasmine', name='unittests', handler='dev.JasmineTests'),

        ## === About URLs === ##
        HandlerPrefixRoute('about.', [
            Route('/about', name='about', handler='About'),
            Route('/terms', name='terms', handler='Terms'),
            Route('/privacy', name='privacy', handler='Privacy'),
            Route('/support', name='support', handler='Support'),
        ]),

        ## === User URLs === ##
        HandlerPrefixRoute('user.', [
            Route('/me', name='user/me', handler='UserProfile'),
            Route('/users', name='user/landing', handler='UserLanding'),
            Route('/user/<key>', name='user/profile/bykey', handler='UserProfile'),
            Route('/user/<username>', name='user/profile', handler='UserProfile'),
            Route('/user/<username>/account', name='user/account', handler='UserAccount'),
        ]),

        ## === Propose URLs === ##
        HandlerPrefixRoute('propose.', [
            Route('/propose', name='propose/landing', handler='ProposeLanding'),
            Route('/proposal/<key>', name='proposal/home', handler='ProposalHome'),
        ]),

        ## === Project URLs === ##
        HandlerPrefixRoute('project.', [
            Route('/projects', name='project/landing', handler='ProjectLanding'),
            Route('/project/<key>', name='project/home', handler='ProjectHome'),
        ]),

        ## === BBQ URLs === ##
        HandlerPrefixRoute('bbq.', [
            Route('/bbq', name='bbq', handler='Moderate'),
        ]),

        ## === Security URLs === ##
        HandlerPrefixRoute('security.', [
            Route('/login', name='auth/login', handler='Login'),
            Route('/logout', name='auth/logout', handler='Logout'),
            Route('/register', name='auth/register', handler='Register'),
            Route('/login/with/<provider>', name='auth/login-with', handler='Login'),
            Route('/thirdparty/<provider>', name='auth/provider', handler='Provider'),
            Route('/_auth/<action>', name='auth/action', handler='FederatedAction'),
            Route('/_auth/<action>/<provider>', name='auth/action-provider', handler='FederatedAction'),
            Route('/_ah/login_required', name='appengine/federated', handler='Login')
        ]),

        ## === Internal URLs === ##
        HandlerPrefixRoute('internal.', [
            PathPrefixRoute('/_internal', [

                HandlerPrefixRoute('matcher.', [
                    PathPrefixRoute('/matcher', [

                        Route('/match', name='internal/matcher-match', handler='Match'),
                        Route('/notify', name='internal/matcher-notify', handler='Notify')

                    ])
                ]),

                Route('/tick/cache', name='internal/cache-flush', handler='NoOp'),
                Route('/tick/garbage', name='internal/garbage-collector', handler='NoOp')
            ])
        ]),

        ## === Media and Asset URLs === ##
        HandlerPrefixRoute('media.', [
            PathPrefixRoute('/_assets', [
                Route('/blob_uploaded/<asset_key>', name='blob-uploaded', handler='BlobstoreUploaded'),
                Route('/blob_uploaded/<asset_key>/<target_key>', name='blob-uploaded', handler='BlobstoreUploaded'),
                Route('/get/<asset_key>', name='get-asset', handler='MediaStorage'),
                Route('/blob/<action>/<asset_key>', name='serve-asset', handler='AssetServer'),
                Route('/blob/<action>/<asset_key>/<filename>', name='serve-asset-filename', handler='AssetServer'),
            ])
        ]),

        ## === Payment URLs === ##
        HandlerPrefixRoute('payment.', [
            PathPrefixRoute('/_payment', [
                Route('/handler', name='payment-handler', handler='PaymentHandler'),
                Route('/ipn', name='payment-ipn-handler', handler='WePayIPNHandler'),
            ])
        ]),

        ## == Tests == ##
        Route('/_test/multipart', name='multipart-test', handler='dev.TestMultipart'),
        Route('/_test/multipart/passthrough', name='multipart-test-passthrough', handler='dev.TestPassthrough'),

        ## Verification URLs
        Route('/mu-637494d5-6bf02344-9d641fe0-7c54acf6', name='custom_url', handler='main.VerifyURL'),

        Route('/<customurl>', name='custom_url', handler='main.CustomUrlHandler')
    ])
]
