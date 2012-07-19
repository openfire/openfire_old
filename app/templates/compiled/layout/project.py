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
        l_current_goal = context.resolve('current_goal')
        l_current_tier = context.resolve('current_tier')
        t_1 = environment.filters['safe']
        if 0: yield None
        yield u'\n\n                        <div id=\'global_progress\'>\n                            <!-- project progress -->\n                            <div id=\'progress\' data-value="%s" data-max="100"' % (
            environment.getattr(l_project, 'progress'), 
        )
        if environment.getattr(l_project, 'progress') == 100:
            if 0: yield None
            yield u' class="done"'
        yield u'>\n                                <div id=\'progress-inner\' style=\'width: %s%%;\'>%s%%</div>\n                            </div>\n                        </div><!-- end #global_progress -->\n\n                        <div id=\'project_goals\' data-section-title="goals">\n                            ' % (
            environment.getattr(l_project, 'progress'), 
            environment.getattr(l_project, 'progress'), 
        )
        if environment.getattr(l_project, 'goals'):
            if 0: yield None
            yield u'\n                            <div id="project-goals-accordion" class=\'pre-accordion\' data-options=\'{"axis":"vertical"}\'>\n                                '
            l_current_goal = False
            yield u'\n                                '
            t_2 = l_current_goal
            l_goal = missing
            l_currency = context.resolve('currency')
            l_encrypt = context.resolve('encrypt')
            for l_goal in l_goals:
                if 0: yield None
                yield u'\n                                    <a href="#%s"' % (
                    context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_goal, 'key'), 'urlsafe'))), 
                )
                if environment.getattr(l_goal, 'amount') < environment.getattr(l_project, 'money'):
                    if 0: yield None
                    yield u' class="reached"'
                else:
                    if 0: yield None
                    if l_current_goal == False:
                        if 0: yield None
                        yield u' class="current"'
                yield u'>%s</a>\n                                    <div id="%s"' % (
                    context.call(l_currency, environment.getattr(l_goal, 'amount')), 
                    context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_goal, 'key'), 'urlsafe'))), 
                )
                if environment.getattr(l_goal, 'amount') < environment.getattr(l_project, 'money'):
                    if 0: yield None
                    yield u' class="reached none"'
                else:
                    if 0: yield None
                    if l_current_goal == False:
                        if 0: yield None
                        l_current_goal = True
                        yield u' class="current none"'
                    else:
                        if 0: yield None
                        yield u' class="none"'
                yield u'>\n                                        <p>'
                if environment.getattr(l_goal, 'description') != None:
                    if 0: yield None
                    yield to_string(environment.getattr(l_goal, 'description'))
                else:
                    if 0: yield None
                    yield u'  '
                yield u'</p>\n                                    </div>\n                                '
            l_current_goal = t_2
            l_goal = missing
            yield u'\n                            </div>\n                            '
        else:
            if 0: yield None
            yield u'\n                                <b>no project goals yet! :(</b>\n                            '
        yield u'\n                        </div> <!-- end #project_goals -->\n\n                        <div id=\'project_tiers\'  data-section-title="tiers">\n                            '
        if environment.getattr(l_project, 'tiers'):
            if 0: yield None
            yield u'\n                            <div id="project-tiers-accordion" class=\'pre-accordion\' data-options=\'{"axis":"vertical"}\'>\n                                '
            l_current_tier = False
            yield u'\n                                '
            t_3 = l_current_tier
            l_tier = missing
            l_currency = context.resolve('currency')
            l_encrypt = context.resolve('encrypt')
            for l_tier in l_tiers:
                if 0: yield None
                yield u'\n                                    <a href="#%s"' % (
                    context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_tier, 'key'), 'urlsafe'))), 
                )
                if l_current_tier == False:
                    if 0: yield None
                    yield u' class="current"'
                yield u'>%s - %s</a>\n                                    <div id="%s"' % (
                    environment.getattr(l_tier, 'name'), 
                    context.call(l_currency, environment.getattr(l_tier, 'amount')), 
                    context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_tier, 'key'), 'urlsafe'))), 
                )
                if l_current_tier == False:
                    if 0: yield None
                    l_current_tier = True
                    yield u' class="current none"'
                else:
                    if 0: yield None
                    yield u' class="none"'
                yield u'>\n                                        <p>%s</p>\n                                    </div>\n                                ' % (
                    t_1(environment.getattr(l_tier, 'description')), 
                )
            l_current_tier = t_3
            l_tier = missing
            yield u'\n                             </div>\n\n                            '
        else:
            if 0: yield None
            yield u'\n                                <b>no project tiers yet! :(</b>\n                            '
        yield u'\n                        </div>\n\n                    '

    def block_description(context, environment=environment):
        l_project = context.resolve('project')
        if 0: yield None
        yield u"\n                            <h3>Summary</h3>\n                            <p>%s</p>\n                            <h3>Pitch</h3>\n                            <p>%s</p>\n                            <h3>Specifics</h3>\n                            <ul class='naked'>\n                                <li>Category: %s</li>\n                                <li>Technology: %s</li>\n                                <li>Keywords: %s</li>\n                            </ul>\n                        " % (
            environment.getattr(l_project, 'summary'), 
            environment.getattr(l_project, 'pitch'), 
            environment.getattr(l_project, 'category'), 
            environment.getattr(l_project, 'tech'), 
            environment.getattr(l_project, 'keywords'), 
        )

    def block_media(context, environment=environment):
        l_encrypt = context.resolve('encrypt')
        l_video = context.resolve('video')
        if 0: yield None
        yield u'\n                    '
        if l_video:
            if 0: yield None
            yield u'\n                        '
            if environment.getattr(l_video, 'provider') == 'vimeo':
                if 0: yield None
                yield u"\n                        <div id='mainvideo' data-provider='vimeo' data-media-key='%s'>\n                            " % (
                    context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_video, 'key'), 'urlsafe'))), 
                )
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
                yield u'\n                        </div>\n                        '
            else:
                if 0: yield None
                yield u'\n                            '
                if environment.getattr(l_video, 'provider') == 'youtube':
                    if 0: yield None
                    yield u'\n                            <div id=\'mainvideo\' data-provider=\'youtube\' data-media-key=\'%s\'>\n                                <iframe width="640" height="360" src="%s" frameborder="0" allowfullscreen></iframe>\n                            </div>\n                            ' % (
                        context.call(l_encrypt, context.call(environment.getattr(environment.getattr(l_video, 'key'), 'urlsafe'))), 
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
        l_currency = context.resolve('currency')
        l_security = context.resolve('security')
        l_owners = context.resolve('owners')
        if 0: yield None
        yield u'\n\n    <!-- Main Masthead -->\n    <div id=\'masthead\'>\n    </div><!-- #masthead -->\n\n    <div id=\'content\'>\n        <div id="fb-root"></div>\n        <div id=\'project\'>\n\n            <div id=\'welcomebox\'>\n\t\t\t\t'
        if environment.getattr(environment.getattr(l_security, 'current_user'), 'key') in environment.getattr(l_project, 'owners'):
            if 0: yield None
            yield u'\n                <div id=\'promote\' data-section-title="admin">\n                    <div id=\'promote-dropzone\' class=\'dropzone\'>drop images here</div>\n                    <button id=\'promote-goals\' value="goals">edit goals</button>\n                    <button id=\'promote-tiers\' value="tiers">edit tiers</button>\n                </div>\n                '
        yield u'\n                '
        for event in context.blocks['media'][0](context):
            yield event
        yield u"\n            </div>\n\n            <div id='sidebar' class='pre-sticky'>\n                <header>\n                    <div id='sidetitle' class='fancy title'><h1>%s</h1></div>\n                    <div id='sidebuttons' class='buttons'>\n                        <button id='follow' class='momentron" % (
            environment.getattr(l_project, 'name'), 
        )
        if environment.getattr(l_project, 'current_user_following'):
            if 0: yield None
            yield u'following'
        yield u'\'>&#xf007f;</button>\n                        <button id=\'share\' class=\'momentron\'>&#xf0085;</button>\n                    </div>\n                </header> <!-- end header -->\n\n                <hr class="hr-inset most">\n\n                <section id=\'quickinfo\'>\n                    '
        for event in context.blocks['right'][0](context):
            yield event
        yield u'\n                </section> <!-- end #quickinfo -->\n\n                <hr class="hr-inset most"></span>\n\n                <section id=\'backers\'>\n                    <div id=\'backproject\'>\n                        <button id=\'back\'><span id="back-text">Back this project</span></button>\n                    </div> <!-- end #backproject -->\n                    <div id=\'backer_summary\'>\n                        backerz\n                    </div> <!-- end #backer_summary -->\n                </section> <!-- end #backers -->\n\n                <div id=\'owners\' >\n                    <b>project owners:</b>\n                    <ul class=\'naked\'>\n                        '
        l_owner = missing
        l_gravatarify = context.resolve('gravatarify')
        l_link = context.resolve('link')
        for l_owner in l_owners:
            if 0: yield None
            yield u'\n                            <li>\n                                <div class=\'ownercard\'>\n                                    <img src="%s" width=\'32\' height=\'32\' alt=\'%s\' />\n\n                                    <div class=\'nametag\' data-owner-key="%s" data-owner-firstname="%s" data-owner-lastname="%s">' % (
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
            yield u'</div>\n                                </div>\n                            </li>\n                        '
        l_owner = missing
        yield u'\n                    </ul>\n                </div> <!-- end #owners -->\n            </div> <!-- end #sidebar -->\n\n            <article id=\'deets\'>\n\n                <!-- project title -->\n                <div id=\'projecttitle\'>\n                    <h1 class="mini-editable" id="project-title-header">%s</h1>\n                    <div id=\'deetactions\'>\n                        <div class=\'buttongroup\' data-action="Share This">\n                            <button id=\'fbshare\' class=\'zocial facebook sharebutton icon\'></button>\n                            <button id=\'twshare\' class=\'zocial twitter sharebutton icon\'></button>\n                            <button id=\'g+share\' class=\'zocial googleplus sharebutton icon\'></button>\n                        </div> <!-- end .buttongroup -->\n                    </div> <!-- end #deetactions -->\n                </div> <!-- end #projecttitle -->\n\n                <!-- project info tabset -->\n                <div id=\'project-tabset\' class=\'pre-tabs relative tabset\' data-options=\'{"div_string":"section","width":"640px"}\'>\n                    <a href=\'#details-tab\' class=\'tab-rounded\'>project details</a>\n                    <a href=\'#members-tab\' class=\'tab-rounded\'>project members</a>\n                    <a href=\'#openfire-tab\' class=\'tab-rounded\'>social reach</a>\n\n                    <!-- details-tab -->\n                    <section id=\'details-tab\' class=\'prsection absolute tab\' style="opacity: 0">\n                        <h2>Project Details</h2>\n                        ' % (
            environment.getattr(l_project, 'name'), 
        )
        for event in context.blocks['description'][0](context):
            yield event
        yield u'\n                    </section><!-- end #details-tab -->\n\n                    <!-- members-tab-->\n                    <section id=\'members-tab\' class=\'prsection absolute tab\' style="opacity: 0">\n                        <h2>Project Members</h2>\n                        <p>This project has team members and an owner.</p>\n                        <p>It was made possible by %s generous backers, who have donated %s to date, placing this project %s%% of the way to its next support goal!</p>\n                    </section><!-- end #members-tab-->\n\n                    <!-- team -->\n                    <section id=\'openfire-tab\' class=\'prsection absolute tab\' style="opacity: 0">\n                        <h2>Social Reach</h2>\n                        <p>TEAM</p>\n                    </section><!-- end #team -->\n\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n                <p></p>\n\n            </article><!-- end #project -->\n        </div><!-- end #content -->\n    </div>\n\n' % (
            environment.getattr(l_project, 'backers'), 
            context.call(l_currency, environment.getattr(l_project, 'money')), 
            environment.getattr(l_project, 'progress'), 
        )

    blocks = {'presouth': block_presouth, 'right': block_right, 'description': block_description, 'media': block_media, 'stylesheets': block_stylesheets, 'main': block_main}
    debug_info = '1=9&216=15&221=22&222=24&223=27&225=30&226=32&231=38&236=44&241=50&62=58&66=67&67=73&72=76&74=79&75=85&76=88&77=100&78=115&88=129&90=132&91=138&92=141&93=149&94=159&164=169&166=173&168=174&171=175&172=176&173=177&25=180&26=185&27=188&28=191&29=193&30=196&32=201&36=207&37=210&38=211&3=223&4=227&7=230&18=237&25=241&52=244&54=246&62=250&121=256&124=259&126=261&127=265&128=275&130=279&131=282&145=287&164=289&182=292'
    return locals()