from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/bbq/moderate.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('layout/bbq.html', '/source/bbq/moderate.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_moderate(context, environment=environment):
        if 0: yield None
        yield u'\n<div style="padding-bottom: 75px;">\n    <h1>We decide all!</h1>\n\n    <div id="drop-image-here" class="pre-uploader editable" style="width:200px; height:200px; border: 1px solid;">\n        DROP AVATAR HERE\n    </div>\n\n\n\n    <div id="bbq-tabs-container" class="pre-tabs" data-options=\'{"width":"800px"}\'>\n\n        <a href="#bbq-tab-1">Categories</a>\n        <a href="#bbq-tab-2">Proposals</a>\n        <a href="#bbq-tab-3">Projects</a>\n        <a href="#bbq-tab-4">Custom URLs</a>\n\n        <div id="bbq-tab-1" style="opacity: 0;">\n            '
        template = environment.get_template('bbq/bbq_categories.html', '/source/bbq/moderate.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event
        yield u'\n        </div>\n        <div id="bbq-tab-2" style="opacity: 0;">\n            '
        template = environment.get_template('bbq/bbq_proposals.html', '/source/bbq/moderate.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event
        yield u'\n        </div>\n        <div id="bbq-tab-3" style="opacity: 0;">\n            '
        template = environment.get_template('bbq/bbq_projects.html', '/source/bbq/moderate.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event
        yield u'\n        </div>\n        <div id="bbq-tab-4" style="opacity: 0;">\n            '
        template = environment.get_template('bbq/bbq_custom_urls.html', '/source/bbq/moderate.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event
        yield u'\n        </div>\n\n    </div>\n\n</div>\n'

    def block_postsouth(context, environment=environment):
        if 0: yield None
        yield u'\n    <script type="text/javascript">\n        $(document).ready(function() {\n            $.apptools.widgets.tabs._init();\n        });\n    </script>\n'

    blocks = {'moderate': block_moderate, 'postsouth': block_postsouth}
    debug_info = '1=9&3=15&26=18&29=22&32=26&35=30&43=35'
    return locals()