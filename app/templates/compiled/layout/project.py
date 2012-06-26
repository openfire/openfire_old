from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/layout/project.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('layout/layout_base.html', '/source/layout/project.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_right(context, environment=environment):
        l_project = context.resolve('project')
        if 0: yield None
        yield u'\n                        <b>project owners:</b>\n                        <ul>\n                            '
        l_owner = missing
        for l_owner in environment.getattr(l_project, 'owners'):
            if 0: yield None
            yield u'\n                                <li>%s</li>\n                            ' % (
                context.call(environment.getattr(l_owner, 'id')), 
            )
        l_owner = missing
        yield u'\n                        </ul>\n                        <br />\n                        <b>technology:</b>\n                        <p>%s\n                    ' % (
            environment.getattr(l_project, 'tech'), 
        )

    def block_description(context, environment=environment):
        l_project = context.resolve('project')
        if 0: yield None
        yield u'\n                      <p>%s</p>\n                    ' % (
            environment.getattr(l_project, 'summary'), 
        )

    def block_media(context, environment=environment):
        l_video = context.resolve('video')
        if 0: yield None
        yield u'\n                    '
        if l_video:
            if 0: yield None
            yield u'\n                        <iframe width="640" height="360" src="%s" frameborder="0" allowfullscreen></iframe>\n                    ' % (
                environment.getattr(l_video, 'url'), 
            )
        else:
            if 0: yield None
            yield u'\n                        <img src="http://placehold.it/640x360/222222&text=video" />\n                    '
        yield u'\n                '

    def block_postsouth(context, environment=environment):
        if 0: yield None
        yield u"\n<script type='text/javascript'>\n\n$(document).ready(function () {\n});\n\n</script>\n"

    def block_stylesheets(context, environment=environment):
        l_asset = context.resolve('asset')
        if 0: yield None
        yield u'\n    <link rel="stylesheet" href="%s">\n' % (
            context.call(environment.getattr(l_asset, 'style'), 'project', 'openfire'), 
        )

    def block_main(context, environment=environment):
        l_project = context.resolve('project')
        if 0: yield None
        yield u"\n\n    <!-- Main Masthead -->\n    <div id='masthead'>\n    </div><!-- #masthead -->\n\n    <div id='content'>\n        <div id='project'>\n\n            <div id='welcomebox'>\n                "
        for event in context.blocks['media'][0](context):
            yield event
        yield u'\n            </div>\n\n            <div id=\'sidebar\'>\n                <header>\n                    <div id=\'sidetitle\' class=\'fancy title\'><h1>%s</h1></div>\n                    <div id=\'sidebuttons\' class=\'buttons\'>\n                        <form class=\'rpctrigger\' action="#" method="POST">\n                            <button id=\'follow\'>Follow</button>\n                        </form>\n                    </div>\n                </header>\n                <section id=\'quickinfo\'>\n                    ' % (
            environment.getattr(l_project, 'name'), 
        )
        for event in context.blocks['right'][0](context):
            yield event
        yield u"\n                </section>\n            </div>\n\n            <article id='deets'>\n\n                <!-- project title -->\n                <h1>%s</h1>\n\n                <!-- intro/pitch -->\n                <section id='intro'>\n                    " % (
            environment.getattr(l_project, 'name'), 
        )
        for event in context.blocks['description'][0](context):
            yield event
        yield u'\n                </section><!-- end #intro -->\n\n            </article><!-- end #project -->\n\n        </div><!-- end #content -->\n    </div>\n\n'

    blocks = {'right': block_right, 'description': block_description, 'media': block_media, 'postsouth': block_postsouth, 'stylesheets': block_stylesheets, 'main': block_main}
    debug_info = '1=9&36=15&39=20&40=23&45=27&57=30&58=34&17=37&18=41&19=44&69=51&3=55&4=59&7=62&17=66&28=69&36=71&53=74&57=76'
    return locals()