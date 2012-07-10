from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/core/__base.html'

    def root(context, environment=environment):
        if 0: yield None
        yield u'<!doctype html>'
        for event in context.blocks['_tpl_root'][0](context):
            yield event

    def block_og_image(context, environment=environment):
        l__opengraph = context.resolve('_opengraph')
        l_page = context.resolve('page')
        if 0: yield None
        if environment.getattr(l_page, 'image'):
            if 0: yield None
            yield to_string(environment.getattr(l_page, 'image'))
        else:
            if 0: yield None
            yield to_string(context.call(environment.getattr(l__opengraph, 'get'), 'image'))

    def block_meta_keywords(context, environment=environment):
        l__meta = context.resolve('_meta')
        if 0: yield None
        yield to_string(context.call(environment.getattr(',', 'join'), context.call(environment.getattr(l__meta, 'get'), 'keywords', [])))

    def block_og_determiner(context, environment=environment):
        l__opengraph = context.resolve('_opengraph')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__opengraph, 'get'), 'determiner'))

    def block_opengraph(context, environment=environment):
        if 0: yield None
        yield u'\n\t\t<!-- OpenGraph -->\n\t\t<meta property="og:title" content="'
        for event in context.blocks['og_title'][0](context):
            yield event
        yield u'" />\n\t\t<meta property="og:type" content="'
        for event in context.blocks['og_type'][0](context):
            yield event
        yield u'" />\n\t\t<meta property="og:determiner" content="'
        for event in context.blocks['og_determiner'][0](context):
            yield event
        yield u'" />\n\t\t<meta propert="og:locale" content="'
        for event in context.blocks['og_locale'][0](context):
            yield event
        yield u'" />\n\t\t<meta property="og:url" content="'
        for event in context.blocks['og_url'][0](context):
            yield event
        yield u'" />\n\t\t<meta property="og:description" content="'
        for event in context.blocks['og_description'][0](context):
            yield event
        yield u'" />\n\t\t<meta property="og:image" content="'
        for event in context.blocks['og_image'][0](context):
            yield event
        yield u'" />\n\t\t<meta property="og:image:width" content="298" />\n\t\t<meta property="og:image:height" content="298" />\n\t\t<meta property="og:site_name" content="'
        for event in context.blocks['og_sitename'][0](context):
            yield event
        yield u'" />\n\t\t<meta property="fb:app_id" content="'
        for event in context.blocks['og_fb_appid'][0](context):
            yield event
        yield u'" />\n\t\t<meta property="fb:admins" content="'
        for event in context.blocks['og_fb_admins'][0](context):
            yield event
        yield u'" />\n\n\t\t<!-- Location/Geo -->\n\t\t<meta property="og:latitude" content="'
        for event in context.blocks['og_latitude'][0](context):
            yield event
        yield u'">\n\t\t<meta property="og:longitude" content="'
        for event in context.blocks['og_longitude'][0](context):
            yield event
        yield u'">\n\t\t<meta property="og:street-address" content="'
        for event in context.blocks['og_address'][0](context):
            yield event
        yield u'">\n\t\t<meta property="og:locality" content="'
        for event in context.blocks['og_locality'][0](context):
            yield event
        yield u'">\n\t\t<meta property="og:region" content="'
        for event in context.blocks['og_region'][0](context):
            yield event
        yield u'">\n\t\t<meta property="og:postal-code" content="'
        for event in context.blocks['og_zipcode'][0](context):
            yield event
        yield u'">\n\t\t<meta property="og:country-name" content="'
        for event in context.blocks['og_country'][0](context):
            yield event
        yield u'">\n\t\t<meta property="og:email" content="'
        for event in context.blocks['og_email'][0](context):
            yield event
        yield u'">\n\t\t<meta property="og:phone_number" content="'
        for event in context.blocks['og_phone'][0](context):
            yield event
        yield u'">\n\t\t'

    def block_og_region(context, environment=environment):
        l__location = context.resolve('_location')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__location, 'get'), 'region'))

    def block_meta_copyright(context, environment=environment):
        l__meta = context.resolve('_meta')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__meta, 'get'), 'copyright'))

    def block__tpl_root(context, environment=environment):
        l_page = context.resolve('page')
        if 0: yield None
        if (not environment.getattr(l_page, 'manifest')):
            if 0: yield None
            yield u'\n<!--[if IEMobile 7]><html class="no-js iem7" lang="en" prefix="og: http://ogp.me/ns#"><![endif]-->\n<!--[if (gt IEMobile 7)|!(IEMobile)]><!--><html class="no-js" lang="en" prefix="og: http://ogp.me/ns#"><!--<![endif]-->\n<!--[if lt IE 7]> <html class="no-js ie6 oldie" lang="en" prefix="og: http://ogp.me/ns#"> <![endif]-->\n<!--[if IE 7]>    <html class="no-js ie7 oldie" lang="en" prefix="og: http://ogp.me/ns#"> <![endif]-->\n<!--[if IE 8]>    <html class="no-js ie8 oldie" lang="en" prefix="og: http://ogp.me/ns#"> <![endif]-->\n<!--[if gt IE 8]><!--> <html class="no-js" lang="en" prefix="og: http://ogp.me/ns#"> <!--<![endif]-->\n'
        else:
            if 0: yield None
            yield u'\n<!--[if IEMobile 7]><html class="no-js iem7" lang="en" prefix="og: http://ogp.me/ns#" manifest="%s"><![endif]-->\n<!--[if (gt IEMobile 7)|!(IEMobile)]><!--><html class="no-js" lang="en" prefix="og: http://ogp.me/ns#" manifest="%s"><!--<![endif]-->\n<!--[if lt IE 7]> <html class="no-js ie6 oldie" lang="en" prefix="og: http://ogp.me/ns#" manifest="%s"> <![endif]-->\n<!--[if (IE 7)&!(IEMobile)]>    <html class="no-js ie7 oldie" lang="en" prefix="og: http://ogp.me/ns#" manifest="%s"> <![endif]-->\n<!--[if (IE 8)&!(IEMobile)]>    <html class="no-js ie8 oldie" lang="en" prefix="og: http://ogp.me/ns#" manifest="%s"> <![endif]-->\n<!--[if gt IE 8]><!--> <html class="no-js" lang="en" prefix="og: http://ogp.me/ns#" manifest="%s"> <!--<![endif]-->\n' % (
                environment.getattr(environment.getattr(l_page, 'manifest'), 'location'), 
                environment.getattr(environment.getattr(l_page, 'manifest'), 'location'), 
                environment.getattr(environment.getattr(l_page, 'manifest'), 'location'), 
                environment.getattr(environment.getattr(l_page, 'manifest'), 'location'), 
                environment.getattr(environment.getattr(l_page, 'manifest'), 'location'), 
                environment.getattr(environment.getattr(l_page, 'manifest'), 'location'), 
            )
        yield u'\n\n<head>\n\t'
        for event in context.blocks['head'][0](context):
            yield event
        yield u'\n</head>\n\n<body role="application" lang="en" translate="yes" dir="ltr">\n\n<div id=\'templates\' class=\'hidden resource\'>\n\t<!-- JS Templates -->\n</div>\n\n'
        for event in context.blocks['body'][0](context):
            yield event
        yield u'\n\n'
        for event in context.blocks['presouth'][0](context):
            yield event
        yield u'\n'
        template = environment.get_template('core/__south.html', '/source/core/__base.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event
        yield u'\n'
        for event in context.blocks['postsouth'][0](context):
            yield event
        yield u'\n</body>\n</html>'

    def block_og_title(context, environment=environment):
        l__opengraph = context.resolve('_opengraph')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__opengraph, 'get'), 'title'))

    def block_meta_description(context, environment=environment):
        l__meta = context.resolve('_meta')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__meta, 'get'), 'description'))

    def block_presouth(context, environment=environment):
        if 0: yield None

    def block_title(context, environment=environment):
        if 0: yield None
        yield u'openfire!'

    def block_meta_author(context, environment=environment):
        l__meta = context.resolve('_meta')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__meta, 'get'), 'author'))

    def block_og_zipcode(context, environment=environment):
        l__location = context.resolve('_location')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__location, 'get'), 'zipcode'))

    def block_og_country(context, environment=environment):
        l__location = context.resolve('_location')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__location, 'get'), 'country'))

    def block_og_locality(context, environment=environment):
        l__location = context.resolve('_location')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__location, 'get'), 'locality'))

    def block_og_locale(context, environment=environment):
        l__opengraph = context.resolve('_opengraph')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__opengraph, 'get'), 'locale', 'en_US'))

    def block_body(context, environment=environment):
        if 0: yield None
        yield u'\n'

    def block_prenorth(context, environment=environment):
        if 0: yield None

    def block_head(context, environment=environment):
        l_util = context.resolve('util')
        l_asset = context.resolve('asset')
        if 0: yield None
        yield u'\n\t\t'
        for event in context.blocks['meta'][0](context):
            yield event
        for event in context.blocks['prenorth'][0](context):
            yield event
        for event in context.blocks['north'][0](context):
            yield event
        for event in context.blocks['stylesheets'][0](context):
            yield event
        yield u'\n\t\t'
        if context.call(environment.getattr(environment.getattr(environment.getattr(l_util, 'api'), 'users'), 'is_current_user_admin')):
            if 0: yield None
            yield u'\n\t\t\t<link rel="stylesheet" href="%s" />\n\t\t' % (
                context.call(environment.getattr(l_asset, 'style'), 'admin', 'compiled'), 
            )
        yield u'\n\t\t'
        for event in context.blocks['postnorth'][0](context):
            yield event
        yield u'\n\n\t\t<title>'
        for event in context.blocks['title'][0](context):
            yield event
        yield u'</title>\n\t'

    def block_og_description(context, environment=environment):
        l__meta = context.resolve('_meta')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__meta, 'get'), 'description'))

    def block_north(context, environment=environment):
        if 0: yield None
        template = environment.get_template('core/__north.html', '/source/core/__base.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event

    def block_og_phone(context, environment=environment):
        l__location = context.resolve('_location')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__location, 'get'), 'phone'))

    def block_stylesheets(context, environment=environment):
        if 0: yield None

    def block_og_sitename(context, environment=environment):
        l__opengraph = context.resolve('_opengraph')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__opengraph, 'get'), 'site_name'))

    def block_og_email(context, environment=environment):
        l__location = context.resolve('_location')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__location, 'get'), 'email'))

    def block_og_latitude(context, environment=environment):
        l__location = context.resolve('_location')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__location, 'get'), 'latitude'))

    def block_og_longitude(context, environment=environment):
        l__location = context.resolve('_location')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__location, 'get'), 'longitude'))

    def block_og_fb_appid(context, environment=environment):
        l__opengraph = context.resolve('_opengraph')
        if 0: yield None
        yield to_string(context.call(environment.getattr(context.call(environment.getattr(l__opengraph, 'get'), 'facebook', {}), 'get'), 'app_id'))

    def block_meta_publisher(context, environment=environment):
        l__meta = context.resolve('_meta')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__meta, 'get'), 'publisher'))

    def block_mobile(context, environment=environment):
        l_util = context.resolve('util')
        l_page = context.resolve('page')
        l_asset = context.resolve('asset')
        if 0: yield None
        if (environment.getattr(l_page, 'ios') or environment.getattr(environment.getattr(l_util, 'config'), 'debug')):
            if 0: yield None
            yield u'\n\t\t<!-- Mobile/Extras -->\n\t\t<meta name="MobileOptimized" content="320">\n\t\t<meta name="HandheldFriendly" content="True">\n\t\t<meta name="apple-mobile-web-app-capable" content="yes">\n\t\t<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />\n\n\t\t<link rel="apple-touch-icon" href="%s" />\n\t\t<link rel="apple-touch-startup-image" href="%s" />\n\t\t<link rel="apple-touch-icon-precomposed" href="%s">\n\t\t<link rel="apple-touch-icon-precomposed" sizes="114x114" href="%s">\n\t\t' % (
                context.call(environment.getattr(l_asset, 'image'), 'mobile/ios', 'touch-icon.png'), 
                context.call(environment.getattr(l_asset, 'image'), 'mobile/ios', 'iphone-splash.png'), 
                context.call(environment.getattr(l_asset, 'image'), 'mobile/ios', 'touch-icon-precomposed.png'), 
                context.call(environment.getattr(l_asset, 'image'), 'mobile/ios', 'apple-touch-icon.png'), 
            )

    def block_postsouth(context, environment=environment):
        if 0: yield None

    def block_og_type(context, environment=environment):
        l__opengraph = context.resolve('_opengraph')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__opengraph, 'get'), 'type'))

    def block_og_fb_admins(context, environment=environment):
        l__opengraph = context.resolve('_opengraph')
        if 0: yield None
        yield to_string(context.call(environment.getattr(',', 'join'), context.call(environment.getattr(context.call(environment.getattr(l__opengraph, 'get'), 'facebook', {}), 'get'), 'admins')))

    def block_og_address(context, environment=environment):
        l__location = context.resolve('_location')
        if 0: yield None
        yield to_string(context.call(environment.getattr(l__location, 'get'), 'address'))

    def block_meta(context, environment=environment):
        l_asset = context.resolve('asset')
        l_page = context.resolve('page')
        l__meta = context.resolve('_meta')
        if 0: yield None
        yield u'\n\n\t\t<!-- Meta -->\n\t\t<meta charset="utf-8">\n\t\t<meta http-equiv="Vary" content="encoding">\n\t\t<meta http-equiv="Content-Language" content="en">\n\t\t<meta http-equiv="Cache-Control" content="private">\n\t\t<meta http-equiv="Content-Type" content="text/html">\n\t\t<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n\t\t'
        if environment.getattr(l_page, 'cookies'):
            if 0: yield None
            yield u'\n\t\t<meta http-equiv="Set-Cookie" content="%s">\n\t\t' % (
                environment.getattr(l_page, 'cookies'), 
            )
        yield u'\n\n\t\t<!-- Info -->\n\t\t<meta name="author" content="'
        for event in context.blocks['meta_author'][0](context):
            yield event
        yield u'">\n\t\t<meta name="publisher" content="'
        for event in context.blocks['meta_publisher'][0](context):
            yield event
        yield u'">\n\t\t<meta name="keywords" content="'
        for event in context.blocks['meta_keywords'][0](context):
            yield event
        yield u'">\n\t\t<meta name="copyright" content="'
        for event in context.blocks['meta_copyright'][0](context):
            yield event
        yield u'">\n\t\t<meta name="description" content="'
        for event in context.blocks['meta_description'][0](context):
            yield event
        yield u'">\n\t\t<meta name="application-name" content="openfire">\n\t\t'
        if context.call(environment.getattr(context.call(environment.getattr(l__meta, 'get'), 'google', {}), 'get'), 'site_verification', False):
            if 0: yield None
            yield u'<meta name="google-site-verification" content="%s" />' % (
                context.call(environment.getattr(context.call(environment.getattr(l__meta, 'get'), 'google'), 'get'), 'site_verification'), 
            )
        yield u'\n\t\t<meta name="robots" content="%s">\n\t\t<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=yes,height=device-height">\n\t\t<meta name="revisit-after" content="%s">\n\t\t<!-- disruption,technology,crowdfunding -->\n\n\t\t' % (
            context.call(environment.getattr(l__meta, 'get'), 'robots', 'index,follow'), 
            context.call(environment.getattr(l__meta, 'get'), 'revisit', '7 days'), 
        )
        for event in context.blocks['opengraph'][0](context):
            yield event
        for event in context.blocks['mobile'][0](context):
            yield event
        yield u'<link rel="icon" href="/favicon.ico" type="image/x-icon">\n\t\t<link rel="logo" href="%s">\n\t\t<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">\n\n\t\t' % (
            context.call(environment.getattr(l_asset, 'image'), 'branding', 'logo.svg'), 
        )

    def block_postnorth(context, environment=environment):
        if 0: yield None

    def block_og_url(context, environment=environment):
        l__opengraph = context.resolve('_opengraph')
        l_page = context.resolve('page')
        if 0: yield None
        if environment.getattr(l_page, 'url'):
            if 0: yield None
            yield to_string(environment.getattr(l_page, 'url'))
        else:
            if 0: yield None
            yield to_string(context.call(environment.getattr(l__opengraph, 'get'), 'url'))

    blocks = {'og_image': block_og_image, 'meta_keywords': block_meta_keywords, 'og_determiner': block_og_determiner, 'opengraph': block_opengraph, 'og_region': block_og_region, 'meta_copyright': block_meta_copyright, '_tpl_root': block__tpl_root, 'og_title': block_og_title, 'meta_description': block_meta_description, 'presouth': block_presouth, 'title': block_title, 'meta_author': block_meta_author, 'og_zipcode': block_og_zipcode, 'og_country': block_og_country, 'og_locality': block_og_locality, 'og_locale': block_og_locale, 'body': block_body, 'prenorth': block_prenorth, 'head': block_head, 'og_description': block_og_description, 'north': block_north, 'og_phone': block_og_phone, 'stylesheets': block_stylesheets, 'og_sitename': block_og_sitename, 'og_email': block_og_email, 'og_latitude': block_og_latitude, 'og_longitude': block_og_longitude, 'og_fb_appid': block_og_fb_appid, 'meta_publisher': block_meta_publisher, 'mobile': block_mobile, 'postsouth': block_postsouth, 'og_type': block_og_type, 'og_fb_admins': block_og_fb_admins, 'og_address': block_og_address, 'meta': block_meta, 'postnorth': block_postnorth, 'og_url': block_og_url}
    debug_info = '2=9&55=12&37=23&51=28&47=33&49=36&50=39&51=42&52=45&53=48&54=51&55=54&58=57&59=60&60=63&63=66&64=69&65=72&66=75&67=78&68=81&69=84&70=87&71=90&67=94&38=99&2=104&3=107&11=113&12=114&13=115&14=116&15=117&16=118&20=121&115=124&118=127&119=130&120=134&49=138&39=143&118=148&105=151&35=155&68=160&69=165&66=170&52=175&115=180&95=184&20=187&21=192&95=194&96=196&99=198&100=201&101=204&103=207&105=210&54=214&96=219&97=221&71=225&99=230&58=233&70=238&63=243&64=248&59=253&36=258&74=263&75=268&82=271&83=272&84=273&85=274&120=277&50=280&60=285&65=290&21=295&30=301&31=304&35=307&36=310&37=313&38=316&39=319&41=322&42=328&44=329&47=331&74=333&90=336&103=339&53=342'
    return locals()