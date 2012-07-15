from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\snippets\\login_box.html'

    def root(context, environment=environment):
        l_federated_error = context.resolve('federated_error')
        l_link = context.resolve('link')
        l_error = context.resolve('error')
        l_security_config = context.resolve('security_config')
        t_1 = environment.filters['safe']
        t_2 = environment.filters['xmlattr']
        if 0: yield None
        yield u'<div class="loginbox" data-csrf="" data-providers="">\n\n\t<script>\n\t\t(function (w)\n\t\t{\n\t\t\tw._initExtAuth = function (p, m)\n\t\t\t{\n\t\t\t\t$(document).ready(function ()\n\t\t\t\t{\n\t\t\t\t\tw.location.href = $(\'.button[data-provider-name="\'+p+\'"]\').attr(\'data-action\');\n\t\t\t\t});\n\t\t\t};\n\t\t})(window);\n\n\t</script>\n\n\t<!-- left column: 3rd part logon -->\n\t<div class="federated">\n\t\t<div class="'
        if (not environment.getattr(environment.getattr(environment.getattr(l_security_config, 'authentication'), 'federation'), 'enabled')):
            if 0: yield None
            yield u'disabled'
        else:
            if 0: yield None
            yield u'thirdparty'
        yield u'">\n\t\t'
        if (not l_federated_error):
            if 0: yield None
            yield u'<h4>Sign in with an existing account</h4>'
        else:
            if 0: yield None
            yield u'<h4 class="woops">%s</h4>' % (
                t_1(l_federated_error), 
            )
        yield u'\n\t\t'
        l_disabled = l_provider = missing
        l_disabled = context.resolve('disabled')
        l_link = context.resolve('link')
        for l_provider in environment.getattr(environment.getattr(environment.getattr(l_security_config, 'authentication'), 'federation'), 'providers'):
            if 0: yield None
            yield u'\n\t\t\t'
            if environment.getattr(l_provider, 'enabled'):
                if 0: yield None
                if (not environment.getattr(environment.getattr(environment.getattr(l_security_config, 'authentication'), 'federation'), 'enabled')):
                    if 0: yield None
                    l_disabled = 'disabled'
                else:
                    if 0: yield None
                    l_disabled = 'thirdparty'
                yield u'<button %s>Login with %s</button>\n\t\t\t' % (
                    t_2(context.eval_ctx, {'class': context.call(environment.getattr(' ', 'join'), [l_disabled, 'zocial', environment.getattr(l_provider, 'name'), 'logon', 'button']), 'data-provider-name': environment.getattr(l_provider, 'name'), 'data-provider-label': environment.getattr(l_provider, 'label'), 'data-provider-mode': environment.getattr(l_provider, 'mode'), 'disabled': (None if (not l_disabled) else environment.undefined("the inline if-expression on line 30 in '/source\\\\snippets\\\\login_box.html' evaluated to false and no else section was defined.")), 'data-action': context.call(l_link, 'auth/login-with', provider=environment.getattr(l_provider, 'name')), 'onclick': t_1(("javascript:window._initExtAuth('%(name)s', '%(mode)s');" % l_provider))}), 
                    environment.getattr(l_provider, 'label'), 
                )
            yield u'\n\t\t'
        l_disabled = l_provider = missing
        yield u'\n\t\t</div>\n\t</div> <!-- end .federated -->\n\n\t<!-- right column: tour -->\n\t<div class="securelogon">\n\t\t'
        if (not l_error):
            if 0: yield None
            yield u'<h4>Or, sign in using your openfire account</h4>'
        else:
            if 0: yield None
            yield u'<h4 class="woops">%s</h4>' % (
                t_1(l_error), 
            )
        yield u'\n\t\t<form action="%s" method="POST" class="oflogon formcontainer">\n\t\t\t<input type="text" name="username" placeholder="Email" />\n\t\t\t<input type="password" name="password" placeholder="Password" />\n\t\t\t<a class="lockedout" href="#">Locked out?</a>\n\t\t\t<button class="login button">Log In</button>\n\t\t\t<button class="signup button">Sign Up</button>\n\t\t</form>\n\t</div> <!-- end .securelogon -->\n\n</div>' % (
            context.call(l_link, 'auth/login'), 
        )

    blocks = {}
    debug_info = '19=15&20=22&21=34&22=37&23=39&33=46&34=47&42=52&43=61'
    return locals()