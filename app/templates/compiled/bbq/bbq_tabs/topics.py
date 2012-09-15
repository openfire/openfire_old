from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\bbq_tabs\\topics.html'

    def root(context, environment=environment):
        l_topics = context.resolve('topics')
        if 0: yield None
        yield u'<h2>openfire topics</h2>\n<a id="a-new-topic-dialog" href="#new-topic-dialog">+ Add New Topic</a>\n<div class="content">\n    <table id="bbq-topic-table" class="bbq-datatable">\n        <thead>\n            <tr>\n                <th>Name</th>\n                <th>Slug</th>\n                <th>User Count</th>\n                <th>Description</th>\n            </tr>\n        </thead>\n        <tbody>\n            '
        l_topic = missing
        for l_topic in l_topics:
            if 0: yield None
            yield u'\n            <tr>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n                <td>%s</td>\n            </tr>\n            ' % (
                environment.getattr(l_topic, 'name'), 
                environment.getattr(l_topic, 'slug'), 
                environment.getattr(l_topic, 'user_count'), 
                environment.getattr(l_topic, 'description'), 
            )
        l_topic = missing
        yield u'\n        </tbody>\n    </table>\n</div>'

    blocks = {}
    debug_info = '14=11&16=14&17=15&18=16&19=17'
    return locals()