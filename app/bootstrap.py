import sys
import logging

if 'lib' not in sys.path:
    # Add lib as primary libraries directory, with fallback to lib/dist
    # and optionally to lib/dist.zip, loaded using zipimport.
    sys.path[0:0] = ['lib', 'lib/dist', 'lib/dist.zip']


class AppBootstrapper(object):

    @classmethod
    def prepareImports(cls):
        if 'lib' not in sys.path:
            sys.path[0:0] = ['lib', 'lib/dist', 'lib/dist.zip']

        try:
            from webapp2 import RequestHandler
            from webapp2 import WSGIApplication
            from google.appengine.ext import webapp
        except:
            pass
        else:
            webapp.RequestHandler = RequestHandler
            webapp.WSGIApplication = WSGIApplication
        finally:
            return cls

    @classmethod
    def prepareExtern(cls):
        if 'lib' not in sys.path:
            sys.path[0:0] = ['lib', 'lib/dist', 'lib/dist.zip']

        return cls
