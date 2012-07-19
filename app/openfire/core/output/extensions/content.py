# -*- coding: utf-8 -*-
from openfire.core.output.extensions import OutputExtension


## DynamicContentExtension
class DynamicContentExtension(OutputExtension):

    ''' Extends Jinja2 to support custom openfire dynamic content tags. '''

    tags = set(['content', 'snippet', 'summary'])
