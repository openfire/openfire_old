# -*- coding: utf-8 -*-
from openfire.core import CoreAPI
from google.appengine.ext import ndb


class CoreDataAPI(CoreAPI):

    ''' The Core Data API contains functions that give us information about our data. '''

    @classmethod
    def custom_url_taken(self, slug):

        ''' Check whether or not a custom url already exists. '''

        url_key = ndb.Key('CustomURL', slug)
        exists = url_key.get()
        return exists != None
