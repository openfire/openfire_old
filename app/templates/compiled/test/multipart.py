from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\test\\multipart.html'

    def root(context, environment=environment):
        l_endpoint = context.resolve('endpoint')
        if 0: yield None
        yield u'<html>\n<body>\n<form action="%s" method=\'POST\' enctype="multipart/form-data">\n\t<b>Upload a test file:</b>\n\t<input type="file" name="beans" />\n\t<input type="submit" />\n</form>\n</body>\n</html>' % (
            l_endpoint, 
        )

    blocks = {}
    debug_info = '3=10'
    return locals()