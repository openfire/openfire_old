# -*- coding: utf-8 -*-
from openfire.pipelines import AppPipeline


## RenderPipeline - parent to all render-related pipelines
class RenderPipeline(AppPipeline):

    ''' Abstract parent class for low-level render pipelines. '''

    def run(self):

        raise NotImplemented  # @TODO


## RawTemplate - return the source of a Jinja template
class RawTemplate(RenderPipeline):

    ''' Returns the source code of a Jinja template. '''

    def run(self):

        raise NotImplemented  # @TODO


## RenderTemplate - render a template and return the compiled source
class RenderTemplate(RenderPipeline):

    ''' Render a Jinja template using the given context, and yield the output. '''

    def run(self):

        raise NotImplemented  # @TODO
