from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\bbq_tabs\\users.html'

    def root(context, environment=environment):
        l_users = context.resolve('users')
        if 0: yield None
        yield u'<h2>openfire users</h2>\n<div class="content">\n    <table id="bbq-user-table" class="bbq-datatable">\n        <thead>\n            <tr>\n                <th>Username</th>\n                <th>Custom URL</th>\n                <th>First Name</th>\n                <th>Last Name</th>\n                <th>Email(s)</th>\n                <th>Activated</th>\n                <th>Public</th>\n            </tr>\n        </thead>\n        <tbody>\n            '
        l_user = missing
        for l_user in l_users:
            if 0: yield None
            yield u'\n            <tr>\n                <td>%s</td>\n                <td><a href="/%s">%s</a></td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>\n                    ' % (
                environment.getattr(l_user, 'username'), 
                context.call(environment.getattr(l_user, 'get_custom_url')), 
                context.call(environment.getattr(l_user, 'get_custom_url')), 
                environment.getattr(l_user, 'firstname'), 
                environment.getattr(l_user, 'lastname'), 
            )
            l_email_key = missing
            for l_email_key in environment.getattr(l_user, 'email'):
                if 0: yield None
                yield u'\n                        %s, &nbsp;\n                    ' % (
                    context.call(environment.getattr(l_email_key, 'id')), 
                )
            l_email_key = missing
            yield u'\n                </td>\n                <td>%s</td>\n                <td>%s</td>\n            </tr>\n            ' % (
                environment.getattr(l_user, 'activated'), 
                environment.getattr(l_user, 'public'), 
            )
        l_user = missing
        yield u'\n        </tbody>\n    </table>\n</div>'

    blocks = {}
    debug_info = '16=11&18=14&19=15&20=17&21=18&23=21&24=24&27=28&28=29'
    return locals()