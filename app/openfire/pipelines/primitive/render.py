# -*- coding: utf-8 -*-
from openfire.pipelines import AppPipeline


## RenderPipeline - parent to all render-related pipelines
class RenderPipeline(AppPipeline):

    ''' Abstract parent class for low-level render pipelines. '''

    pass


## RawTemplate - return the source of a Jinja template
class RawTemplate(RenderPipeline):

    ''' Returns the source code of a Jinja template. '''

    pass


## RenderTemplate - render a template and return the compiled source
class RenderTemplate(RenderPipeline):

    ''' Render a Jinja template using the given context, and yield the output. '''

    pass
