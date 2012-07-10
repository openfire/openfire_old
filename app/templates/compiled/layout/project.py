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

    def block_presouth(context, environment=environment):
        l_project = context.resolve('project')
        l_util = context.resolve('util')
        l_encrypt = context.resolve('encrypt')
        l_security = context.resolve('security')
        if 0: yield None
        yield u"\n<script>\n\n  // openfire project init\n  window._cp = {\n    ke: '%s'," % (
            context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_project, 'key'), 'urlsafe'))), 
        )
        if environment.getattr(environment.getattr(l_util, 'config'), 'debug'):
            if 0: yield None
            yield u"kd: '%s'," % (
                context.call(environment.getattr(environment.getattr(l_project, 'key'), 'urlsafe')), 
            )
        yield u'i: %s,' % (
            context.call(environment.getattr(environment.getattr(l_project, 'key'), 'id')), 
        )
        if environment.getattr(l_project, 'current_user_following'):
            if 0: yield None
            yield u'f: true,'
        else:
            if 0: yield None
            yield u'f: false,'
        if environment.getattr(l_project, 'current_user_backed'):
            if 0: yield None
            yield u'b: true,'
        else:
            if 0: yield None
            yield u'b: false,'
        if environment.getattr(environment.getattr(l_security, 'current_user'), 'key') in environment.getattr(l_project, 'owners'):
            if 0: yield None
            yield u'o: true,'
        else:
            if 0: yield None
            yield u'o: false,'
        if environment.getattr(environment.getattr(l_security, 'current_user'), 'key') in environment.getattr(l_project, 'viewers'):
            if 0: yield None
            yield u'v: true'
        else:
            if 0: yield None
            yield u'v: false'
        yield u'};\n\n</script>\n'

    def block_right(context, environment=environment):
        l_project = context.resolve('project')
        l_tiers = context.resolve('tiers')
        l_goals = context.resolve('goals')
        if 0: yield None
        yield u'\n\n\t\t\t\t\t\t<div id=\'global_progress\'>\n\t\t\t\t\t\t\t<!-- project progress -->\n\t\t\t\t\t\t\t<div id=\'progress\' data-value="%s" data-max="100">\n\t\t\t\t\t\t\t\t<div id=\'progress-inner\' style=\'width: %s%%;\'>%s%%</div>\n\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t</div><!-- end #global_progress -->\n\n\t\t\t\t\t\t<div id=\'project_goals\'>\n\t\t\t\t\t\t\t' % (
            environment.getattr(l_project, 'progress'), 
            environment.getattr(l_project, 'progress'), 
            environment.getattr(l_project, 'progress'), 
        )
        if environment.getattr(l_project, 'goals'):
            if 0: yield None
            yield u"\n\t                        <ul class='naked'>\n\t\t\t\t\t\t\t\t"
            l_goal = missing
            l_currency = context.resolve('currency')
            for l_goal in l_goals:
                if 0: yield None
                yield u'\n\t\t\t\t\t\t\t\t\t<li>\n\t\t\t\t\t\t\t\t\t\t<b>%s</b>\n\t\t\t\t\t\t\t\t\t</li>\n\t\t\t\t\t\t\t\t' % (
                    context.call(l_currency, environment.getattr(l_goal, 'amount')), 
                )
            l_goal = missing
            yield u'\n\t                        </ul>\n\t\t\t\t\t\t\t'
        else:
            if 0: yield None
            yield u'\n\t\t\t\t\t\t\t\t<b>no project goals yet! :(</b>\n\t\t\t\t\t\t\t'
        yield u"\n\t\t\t\t\t\t</div> <!-- end #project_goals -->\n\n\t\t\t\t\t\t<div id='project_tiers'>\n\t\t\t\t\t\t\t"
        if environment.getattr(l_project, 'tiers'):
            if 0: yield None
            yield u"\n\t\t\t\t\t\t\t<ul class='naked'>\n\t\t\t\t\t\t\t\t"
            l_tier = missing
            l_currency = context.resolve('currency')
            for l_tier in l_tiers:
                if 0: yield None
                yield u'\n\t\t\t\t\t\t\t\t\t<li>\n\t\t\t\t\t\t\t\t\t\t<b>%s - %s</b>\n\t\t\t\t\t\t\t\t\t</li>\n\t\t\t\t\t\t\t    ' % (
                    environment.getattr(l_tier, 'name'), 
                    context.call(l_currency, environment.getattr(l_tier, 'amount')), 
                )
            l_tier = missing
            yield u'\n\t\t\t\t\t\t\t </ul>\n\n\t\t\t\t\t\t\t'
        else:
            if 0: yield None
            yield u'\n\t\t\t\t\t\t\t\t<b>no project tiers yet! :(</b>\n\t\t\t\t\t\t\t'
        yield u'\n\t\t\t\t\t\t</div>\n\n                    '

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
            yield u'\n                        '
            if environment.getattr(l_video, 'provider') == 'vimeo':
                if 0: yield None
                yield u'\n                            '
                if environment.getattr(l_video, 'ext_id'):
                    if 0: yield None
                    yield u'\n                                <iframe src="http://player.vimeo.com/video/%s?title=0&amp;byline=0&amp;portrait=0&amp;color=BADA55&amp;api=1&amp;player_id=prj" width="640" height="360" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>\n                            ' % (
                        environment.getattr(l_video, 'ext_id'), 
                    )
                else:
                    if 0: yield None
                    yield u'\n                                <iframe src="%s" width="640" height="360" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>\n                            ' % (
                        environment.getattr(l_video, 'url'), 
                    )
                yield u'\n                        '
            else:
                if 0: yield None
                yield u'\n                            '
                if environment.getattr(l_video, 'provider') == 'youtube':
                    if 0: yield None
                    yield u'\n                                <iframe width="640" height="360" src="%s" frameborder="0" allowfullscreen></iframe>\n                            ' % (
                        environment.getattr(l_video, 'url'), 
                    )
                else:
                    if 0: yield None
                    yield u'\n                                <img src="http://placehold.it/640x360/222222&text=video" />\n                            '
                yield u'\n                        '
            yield u'\n                    '
        else:
            if 0: yield None
            yield u'\n                        <img src="http://placehold.it/640x360/222222&text=video" />\n                    '
        yield u'\n                '

    def block_stylesheets(context, environment=environment):
        l_asset = context.resolve('asset')
        if 0: yield None
        yield u'\n    <link rel="stylesheet" href="%s">\n' % (
            context.call(environment.getattr(l_asset, 'style'), 'project', 'openfire'), 
        )

    def block_main(context, environment=environment):
        l_project = context.resolve('project')
        l_owners = context.resolve('owners')
        if 0: yield None
        yield u'\n\n    <!-- Main Masthead -->\n    <div id=\'masthead\'>\n    </div><!-- #masthead -->\n\n    <div id=\'content\'>\n        <div id="fb-root"></div>\n        <div id=\'project\'>\n\n            <div id=\'welcomebox\'>\n                <div id=\'promote\'>\n                </div>\n                '
        for event in context.blocks['media'][0](context):
            yield event
        yield u"\n            </div>\n\n            <div id='sidebar'>\n                <header>\n                    <div id='sidetitle' class='fancy title'><h1>%s</h1></div>\n                    <div id='sidebuttons' class='buttons'>\n                        <button id='follow' class='momentron" % (
            environment.getattr(l_project, 'name'), 
        )
        if environment.getattr(l_project, 'current_user_following'):
            if 0: yield None
            yield u'following'
        yield u"'>&#xf007f;</button>\n                        <button id='share' class='momentron'>&#xf0085;</button>\n                    </div>\n                </header> <!-- end header -->\n                <section id='quickinfo'>\n                    "
        for event in context.blocks['right'][0](context):
            yield event
        yield u"\n                </section> <!-- end #quickinfo -->\n                <section id='backers'>\n                    <div id='backproject'>\n                        <button id='back'>Back</button>\n                    </div> <!-- end #backproject -->\n                    <div id='backer_summary'>\n                        backerz\n                    </div> <!-- end #backer_summary -->\n                </section> <!-- end #backers -->\n\n                <div id='owners'>\n\t\t            <b>project owners:</b>\n\t\t            <ul class='naked'>\n\t\t                "
        l_owner = missing
        l_gravatarify = context.resolve('gravatarify')
        l_link = context.resolve('link')
        for l_owner in l_owners:
            if 0: yield None
            yield u'\n\t\t                    <li>\n\t\t\t\t\t\t\t\t<div class=\'ownercard\'>\n\t\t\t\t\t\t\t\t\t<img src="%s" width=\'32\' height=\'32\' alt=\'%s\' />\n\n\t\t\t\t\t\t\t\t\t<div class=\'nametag\' data-owner-key="%s" data-owner-firstname="%s" data-owner-lastname="%s">' % (
                context.call(l_gravatarify, context.call(environment.getattr(environment.getattr(l_owner, 'key'), 'id')), 'jpg', '32'), 
                context.call(environment.getattr(environment.getattr(l_owner, 'key'), 'id')), 
                context.call(environment.getattr(environment.getattr(l_owner, 'key'), 'urlsafe')), 
                environment.getattr(l_owner, 'firstname'), 
                environment.getattr(l_owner, 'lastname'), 
            )
            if environment.getattr(l_owner, 'customurl'):
                if 0: yield None
                yield u'<a href="%s">%s %s</a>' % (
                    context.call(l_link, 'custom_url', customurl=context.call(environment.getattr(environment.getattr(l_owner, 'customurl'), 'id'))), 
                    environment.getattr(l_owner, 'firstname'), 
                    environment.getattr(l_owner, 'lastname'), 
                )
            else:
                if 0: yield None
                yield u'<a href="%s">%s %s</a>' % (
                    context.call(l_link, 'user/profile', username=context.call(environment.getattr(environment.getattr(l_owner, 'key'), 'id'))), 
                    environment.getattr(l_owner, 'firstname'), 
                    environment.getattr(l_owner, 'lastname'), 
                )
            if environment.getattr(l_owner, 'location'):
                if 0: yield None
                yield u"<span class='location byline'>%s</span>" % (
                    environment.getattr(l_owner, 'location'), 
                )
            yield u'</div>\n\t\t\t\t\t\t\t\t</div>\n\t\t\t\t\t\t\t</li>\n\t\t                '
        l_owner = missing
        yield u"\n\t\t            </ul>\n\t\t        </div> <!-- end #owners -->\n            </div> <!-- end #sidebar -->\n\n            <article id='deets'>\n\n                <!-- project title -->\n                <div id='projecttitle'>\n                    <h1>%s</h1>\n                    <div id='deetactions'>\n                        <div class='buttongroup'>\n                            <h6>Share This</h6>\n                            <button id='fbshare' class='zocial facebook sharebutton icon'></button>\n                            <button id='twshare' class='zocial twitter sharebutton icon'></button>\n                            <button id='g+share' class='zocial googleplus sharebutton icon'></button>\n                        </div> <!-- end .buttongroup -->\n                    </div> <!-- end #deetactions -->\n                </div> <!-- end #projecttitle -->\n\n                <!-- intro/pitch -->\n                <section id='intro' class='prsection'>\n                    <h2>Project Intro</h2>\n                    " % (
            environment.getattr(l_project, 'name'), 
        )
        for event in context.blocks['description'][0](context):
            yield event
        yield u"\n                </section><!-- end #intro -->\n\n                <!-- technologies -->\n                <section id='technologies' class='prsection'>\n                    <h2>Technologies</h2>\n                    <p>%s</p>\n                </section><!-- end #technologies -->\n\n                <!-- team -->\n                <section id='team' class='prsection'>\n                    <h2>Team</h2>\n                    <p>TEAM</p>\n                </section><!-- end #team -->\n\n            </article><!-- end #project -->\n        </div><!-- end #content -->\n    </div>\n\n" % (
            environment.getattr(l_project, 'tech'), 
        )

    blocks = {'presouth': block_presouth, 'right': block_right, 'description': block_description, 'media': block_media, 'stylesheets': block_stylesheets, 'main': block_main}
    debug_info = '1=9&163=15&168=22&169=24&170=27&172=30&173=32&178=38&183=44&188=50&50=58&54=64&55=65&60=68&62=73&64=76&74=84&76=89&78=92&140=102&141=106&20=109&21=113&22=116&23=119&24=122&26=127&29=133&30=136&3=148&4=152&7=155&20=160&43=163&45=165&50=169&102=175&105=178&107=180&108=184&109=194&111=198&112=201&126=206&140=208&148=211'
    return locals()