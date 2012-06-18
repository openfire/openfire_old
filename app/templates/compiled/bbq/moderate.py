from __future__ import division
from jinja2.runtime import LoopContext, TemplateReference, Macro, Markup, TemplateRuntimeError, missing, concat, escape, markup_join, unicode_join, to_string, identity, TemplateNotFound
def run(environment):
    name = '/source\\bbq\\moderate.html'

    def root(context, environment=environment):
        parent_template = None
        if 0: yield None
        parent_template = environment.get_template('layout/bbq.html', '/source\\bbq\\moderate.html')
        for name, parent_block in parent_template.blocks.iteritems():
            context.blocks.setdefault(name, []).append(parent_block)
        for event in parent_template.root_render_func(context):
            yield event

    def block_moderate(context, environment=environment):
        if 0: yield None
        yield u'\n<div>\n    <h1>We decide all!</h1>\n    '
        template = environment.get_template('bbq/bbq_categories.html', '/source\\bbq\\moderate.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event
        yield u'\n\n    '
        template = environment.get_template('bbq/bbq_proposals.html', '/source\\bbq\\moderate.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event
        yield u'\n\n    '
        template = environment.get_template('bbq/bbq_projects.html', '/source\\bbq\\moderate.html')
        for event in template.root_render_func(template.new_context(context.parent, True, locals())):
            yield event
        yield u'\n</div>\n'

    def block_postsouth(context, environment=environment):
        if 0: yield None
        yield u'\n<script type="text/javascript">\n    /*\n     * TODO: Refactor and move all this code to assests.\n     */\n\n    $(document).ready(function() {\n\n        function lightGrill() {\n            $("#show-new-category-btn").click(function() {\n                $("#new-category-inline").show();\n                $("#show-new-category-btn").hide();\n            });\n\n            $("#cancel-new-category-btn").click(function() {\n                $("#new-category-inline").hide();\n                $("#show-new-category-btn").show();\n            });\n\n            $("#save-new-category-btn").click(function() {\n                var categoryDict = {\n                    name: $("#new-category-name-input").val(),\n                    slug: $("#new-category-url-input").val(),\n                    description: $("#new-category-description-input").val()\n                };\n                var request = $.apptools.api.category.put(categoryDict);\n                request.fulfill({\n                    success: function(obj, objType, rawResponse) {\n                        document.location.reload();\n                    },\n                    error: function(err) {\n                        alert("There was an error when you just tried to add the category just then.");\n                    }\n                });\n            });\n\n            $(".delete-category-btn").click(function() {\n                var categorySlug = this.id.match(/delete-category-(\\w+)/)[1],\n                    request = $.apptools.api.category.delete({slug: categorySlug});\n                request.fulfill({\n                    success: function(obj, objType, rawResponse) {\n                        document.location.reload();\n                    },\n                    error: function(err) {\n                        alert("There was an error when you tried to delete that category.");\n                    }\n                });\n            });\n\n            $(".start-edit-category-btn").click(function() {\n                var categorySlug = this.id.match(/start-edit-category-(\\w+)/)[1];\n                $("#start-edit-category-" + categorySlug).hide();\n                $("#save-edit-category-" + categorySlug).show();\n                $("#cancel-edit-category-" + categorySlug).show();\n                $("#category-display-" + categorySlug).hide();\n                $("#category-inputs-" + categorySlug).show();\n            });\n\n            $(".cancel-edit-category-btn").click(function() {\n                var categorySlug = this.id.match(/cancel-edit-category-(\\w+)/)[1];\n                $("#start-edit-category-" + categorySlug).show();\n                $("#save-edit-category-" + categorySlug).hide();\n                $("#cancel-edit-category-" + categorySlug).hide();\n                $("#category-display-" + categorySlug).show();\n                $("#category-inputs-" + categorySlug).hide();\n            });\n\n            $(".save-edit-category-btn").click(function() {\n                var categorySlug = this.id.match(/save-edit-category-(\\w+)/)[1],\n                    categoryDict = {\n                        key: $("#category-inputs-" + categorySlug + " .slug-input").val(),\n                        slug: $("#category-inputs-" + categorySlug + " .slug-input").val(),\n                        name: $("#category-inputs-" + categorySlug + " .name-input").val(),\n                        description: $("#category-inputs-" + categorySlug + " .description-input").val()\n                    },\n                    request = $.apptools.api.category.put(categoryDict);\n                request.fulfill({\n                    success: function(obj, objType, rawResponse) {\n                        document.location.reload();\n                    },\n                    error: function(err) {\n                        alert("There was an error when you tried to delete that category.");\n                    }\n                });\n            });\n\n        }\n\n        lightGrill();\n    });\n</script>\n'

    blocks = {'moderate': block_moderate, 'postsouth': block_postsouth}
    debug_info = '1=9&3=15&6=18&8=22&10=26&14=31'
    return locals()