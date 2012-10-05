from config import config


def webapp_add_wsgi_middleware(app):

    ''' Add appstats profiling middleware. '''

    if config.get('apptools.system', {}).get('hooks', {}).get('appstats', {}).get('enabled', False) == True:
        from google.appengine.ext.appstats import recording
        app = recording.appstats_wsgi_middleware(app)
    return app
