from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/layout/landing.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('layout/layout_base.html', '/source/layout/landing.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_stylesheets(context, environment=environment):
        l_asset = context.resolve('asset')
        if 0: yield None
        yield u'\n    <link rel="stylesheet" href="%s">\n' % (
            context.call(environment.getattr(l_asset, 'style'), 'landing', 'openfire'), 
        )

    def block_main(context, environment=environment):
        l_projects = context.resolve('projects')
        if 0: yield None
        yield u'\n\n<!-- Main Masthead -->\n    <div id=\'masthead\'>\n        <div class="left">\n            <img id=\'oflogo\' src=\'https://d2ipw8y1masjpy.cloudfront.net/static/branding/openfire_transparent_optimized.png\' alt=\'openfire!\' width=\'600\' height=\'173\' />\n            <h1 id="title"><span class=\'lightorange\'>momentum for</span> <span class=\'darkorange\'>positive disruption</span></h1>\n        </div>\n        <div id="how-it-works-button" class="right">\n            <a href id="a-how-it-works">How it works&nbsp;&nbsp;&gt;</a>\n        </div>\n\n    </div><!-- #masthead -->\n\n    <div id=\'content\'>\n\n        <section id=\'projects\' class=\'cardstack\' role=\'region\'>\n\n            <h2>Projects</h2>\n            <div class=\'section-wrap\'>\n            '
        if l_projects:
            if 0: yield None
            yield u'\n                '
            l_project = missing
            l_util = context.resolve('util')
            l_link = context.resolve('link')
            l_asset = context.resolve('asset')
            for l_project in l_projects:
                if 0: yield None
                yield u'\n                    <!-- project card for %s -->\n                    <div class=\'project-card\' data-project=\'%s\'>\n                        <a href="%s">\n                            <div class=\'project-icon\' data-name=\'%s\' data-description=\'%s\'>\n                                ' % (
                    environment.getattr(l_project, 'slug'), 
                    environment.getattr(l_project, 'slug'), 
                    context.call(l_link, 'project/home', customurl=context.call(environment.getattr(environment.getattr(l_project, 'key'), 'id'))), 
                    environment.getattr(l_project, 'name'), 
                    environment.getattr(l_project, 'summary'), 
                )
                if environment.getattr(l_project, 'avatar'):
                    if 0: yield None
                    yield u'\n                                    <img src="%s" title="%s - %s" />\n                                ' % (
                        context.call(environment.getattr(l_asset, 'image'), 'projects/cardstock', environment.getattr(l_project, 'avatar')), 
                        environment.getattr(l_project, 'name'), 
                        environment.getattr(l_project, 'summary'), 
                    )
                else:
                    if 0: yield None
                    yield u'\n                                    <img src="http://placehold.it/140x120" />\n                                '
                yield u"\n                            </div>\n                        </a>\n                        <div class='project-progress' style='width: %s%%'>\n                        </div>\n                    </div> <!-- end project card for %s -->\n                " % (
                    context.call(environment.getattr(environment.getattr(l_util, 'random'), 'randint'), 1, 100), 
                    environment.getattr(l_project, 'slug'), 
                )
            l_project = missing
            yield u'\n            '
        else:
            if 0: yield None
            yield u"\n                <div class='ohnoes'>\n                    Oh noez, no projects!\n                </div>\n            "
        yield u'\n            </div>\n\n        </section><!-- #projects -->\n\n        <section id=\'activity\' class=\'newsfeed\' role=\'region\'>\n\n            <h2>Activity</h2>\n            <div class="section-wrap">\n                <!--<ul class=\'feed\'>\n                    <li class=\'feed-item\'>\n                        <span class="datetime">\n                            &nbsp;\n                        </span>\n                    </li>\n                </ul>-->\n\n                <div id=\'pre-scroller\' class="scroller-frame">\n                    <div class="scroller-pane" id="pane1">\n                        <p>\n                            test pane 1\n                        </p>\n                    </div>\n                    <div class="scroller-pane" id="pane2">\n                        <p>\n                            test pane 2\n                        </p>\n                    </div>\n                </div>\n                <div>\n                    <a id="a-pane1">pane 1</a>\n                    <a id="a-pane2">pane 2</a>\n                </div>\n            </div>\n\n        </section><!-- #activity -->\n\n     </div><!-- #content -->\n\n<div class="pre-modal" id="how-it-works" data-title="How it works!" data-options=\'{"ratio":{"x":0.7,"y":0.7}}\'>\n    <h1>How it works!</h1>\n    <p>I will eventually be content that explains what the heck this awesome-looking site is about!</p>\n</div>\n'

    def block_tinylogo(context, environment=environment):
        if 0: yield None

    def block_leftnav(context, environment=environment):
        if 0: yield None

    blocks = {'stylesheets': block_stylesheets, 'main': block_main, 'tinylogo': block_tinylogo, 'leftnav': block_leftnav}
    debug_info = '1=9&3=15&4=19&11=22&31=26&32=33&33=36&34=37&35=38&36=39&37=42&38=45&44=53&46=54&9=63&8=66'
    return locals()