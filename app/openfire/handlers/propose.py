# -*- coding: utf-8 -*-
from openfire.handlers import WebHandler


class ProposeLanding(WebHandler):

    ''' openfire proposal landing page. '''

    def get(self):

        ''' Render propose_landing.html. '''

        self.render('propose/proposal_landing.html')
        return


class Apply(WebHandler):

    ''' openfire apply page. '''

    def get(self):

        ''' Render apply.html. '''

        self.render('propose/apply.html')
        return


class ProposalHome(WebHandler):

    ''' openfire proposal home page. '''

    def get(self, key):

        ''' Render proposal_home.html. '''

        self.render('propose/proposal_home.html')
        return
