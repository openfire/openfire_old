## internal handlers
from openfire.handlers import WebHandler


class NoOp(WebHandler):

    ''' Will be implemented later. '''

    def get(self):

        return self.error(200)

    def post(self):

        return self.error(200)
