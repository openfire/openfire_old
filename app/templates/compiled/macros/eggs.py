from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source/macros/eggs.html'

    def root(context, environment=environment):
        if 0: yield None
        def macro(l_user, l_session):
            t_1 = []
            l_util = context.resolve('util')
            pass
            l__greeting_template = context.call(environment.getattr(environment.getattr(l_util, 'random'), 'choice'), ['Hey %s!', 'Bonjour, %s!', 'Welcome back, %s!', 'We missed you, %s!'])
            if environment.getattr(l_user, 'firstname'):
                pass
                t_1.append(
                    to_string((l__greeting_template % environment.getattr(l_user, 'firstname'))), 
                )
            else:
                pass
                if environment.getattr(l_session, 'nickname'):
                    pass
                    t_1.append(
                        to_string((l__greeting_template % environment.getattr(l_session, 'nickname'))), 
                    )
            return concat(t_1)
        context.exported_vars.add('random_greeting')
        context.vars['random_greeting'] = l_random_greeting = Macro(environment, macro, 'random_greeting', ('user', 'session'), (), False, False, False)

    blocks = {}
    debug_info = '1=8&2=12&11=13&12=20'
    return locals()