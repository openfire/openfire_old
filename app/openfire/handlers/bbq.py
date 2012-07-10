# -*- coding: utf-8 -*-
from openfire.handlers import WebHandler
from openfire.models.project import Category, Proposal, Project
from openfire.models.user import User
from openfire.models.assets import CustomURL


class Moderate(WebHandler):

    ''' openfire bbq (moderation) page. '''

    def get(self):

        ''' Render moderate.html. '''

        context = {
            'categories': Category.query().fetch(),
            'proposals': Proposal.query().fetch(),
            'projects': Project.query().fetch(),
            'users': User.query().fetch(),
            'custom_urls': CustomURL.query().fetch(),
        }
        return self.render('bbq/moderate.html', **context)
