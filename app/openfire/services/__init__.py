# -*- coding: utf-8 -*-
## Project Services Init
import logging
from apptools import BaseService

from openfire.core.sessions import SessionsMixin


class RemoteService(BaseService, SessionsMixin):

    ''' Abstract parent for all openfire services. '''

    def initialize(self):

        ''' Initialize hook. '''

        logging.critical('!!!!!!!!!!  ====  INITIALIZE HOOK RAN  ====  !!!!!!!!!!')
        logging.critical('SELF: %s' % self)
        logging.critical('SELF DIR: %s' % dir(self))
        return
