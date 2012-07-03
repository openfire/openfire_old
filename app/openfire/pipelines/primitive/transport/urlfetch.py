# -*- coding: utf-8 -*-
from openfire.pipelines.primitive import TransportPipeline


class URLFetchPipeline(TransportPipeline):

    ''' Abstract parent class for low-level URL fetch pipelines. '''

    pass


class FetchURL(URLFetchPipeline):

    ''' Retrieve a URL and yield a structure with the status code, result content, final URL and response headers directly. '''

    pass


class DownloadURL(URLFetchPipeline):

    ''' Retrieve a URL and yield a *reference* to a persisted structure with the status code, result content, final URL and response headers. '''

    pass


class PingURL(URLFetchPipeline):

    ''' Retrieve a URL and yield a structure with the status code and response headers only. Content is discarded. '''

    pass
