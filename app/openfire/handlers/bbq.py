# -*- coding: utf-8 -*-
from openfire.handlers import WebHandler
from openfire.models.project import Category, Proposal, Project


class Moderate(WebHandler):

    ''' openfire bbq (moderation) page. '''

    def get(self):

        ''' Render moderate.html. '''

        categories = Category.query().fetch()
        proposals = Proposal.query().fetch()
        projects = Project.query().fetch()
        self.render('bbq/moderate.html', categories=categories, proposals=proposals, projects=projects)
        return
