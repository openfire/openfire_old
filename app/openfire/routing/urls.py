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

        ## === About URLs === ##
        HandlerPrefixRoute('about.', [
            Route('/about', name='about', handler='About'),
            Route('/terms', name='terms', handler='Terms'),
            Route('/privacy', name='privacy', handler='Privacy'),
            Route('/support', name='support', handler='Support'),
        ]),

        ## === User URLs === ##
        HandlerPrefixRoute('user.', [
            Route('/users', name='user/landing', handler='UserLanding'),
            Route('/user/<username>', name='user/profile', handler='UserProfile'),
            Route('/user/<username>/account', name='user/accout', handler='UserAccount'),
        ]),

        ## === Propose URLs === ##
        HandlerPrefixRoute('propose.', [
            Route('/propose', name='propose/landing', handler='ProposeLanding'),
            Route('/apply', name='apply', handler='Apply'),
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
        ]),

        ## === Internal URLs === ##
        HandlerPrefixRoute('internal.', [
            PathPrefixRoute('/_internal', [
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

        ## == Tests == ##
        Route('/_test/multipart', name='multipart-test', handler='dev.TestMultipart'),
        Route('/_test/multipart/passthrough', name='multipart-test-passthrough', handler='dev.TestPassthrough'),

        ## Verification URLs
        Route('/mu-637494d5-6bf02344-9d641fe0-7c54acf6', name='custom_url', handler='main.VerifyURL'),

        Route('/<customurl>', name='custom_url', handler='main.CustomUrlHandler')
    ])
]
