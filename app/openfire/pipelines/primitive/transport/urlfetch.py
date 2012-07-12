# -*- coding: utf-8 -*-
from google.appengine.api import urlfetch
from openfire.pipelines.primitive import TransportPipeline


## URLFetchPipeline - parent to all URLFetch-based pipelines
class URLFetchPipeline(TransportPipeline):

    ''' Abstract parent class for low-level URL fetch pipelines. '''

    api = urlfetch


## FetchURL - fetches a URL and yields the result directly
class FetchURL(URLFetchPipeline):

    ''' Retrieve a URL and yield a structure with the status code, result content, final URL and response headers directly. '''

    def run(self):

        raise NotImplemented  # @TODO


## DownloadURL - fetches a URL and yields a *reference* to the result
class DownloadURL(URLFetchPipeline):

    ''' Retrieve a URL and yield a *reference* to a persisted structure with the status code, result content, final URL and response headers. '''

    def run(self):

        raise NotImplemented  # @TODO


## PingURL - touch a URL and return only the status code and headers, discarding the content
class PingURL(URLFetchPipeline):

    ''' Retrieve a URL and yield a structure with the status code and response headers only. Content is discarded. '''

    def run(self):

        raise NotImplemented  # @TODO
