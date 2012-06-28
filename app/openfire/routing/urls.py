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
            Route('/proposal/<token>', name='proposal/home', handler='ProposalHome'),
        ]),

        ## === Project URLs === ##
        HandlerPrefixRoute('project.', [
            Route('/projects', name='project/landing', handler='ProjectLanding'),
            Route('/project/<customurl>', name='project/home', handler='ProjectHome'),
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
        ])
    ])
]
