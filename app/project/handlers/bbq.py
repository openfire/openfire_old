# -*- coding: utf-8 -*-
from project.handlers import WebHandler


class Moderate(WebHandler):

    ''' openfire bbq (moderation) page. '''

    def get(self):

        ''' Render moderate.html. '''

        self.render('bbq/moderate.html')
        return
