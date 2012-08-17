## openfire widget classes

class WidgetController extends OpenfireController

    @mount: 'widgets'
    @export: 'private'
    constructor: () ->
        @facepile = Facepile.prototype
        @followers = Followers.prototype
        @backers = Backers.prototype
        @owners = Owners.prototype


# base Facepile class: generates a facepile
class Facepile extends CoreWidget
    @mount: 'facepile'

    template: [
        '<div class="{{=class}}">\n',
            '{{@users}}',
                '<a href="https://www.openfi.re/{{=username}}" data-firstname="{{=firstname}}">',
                    '<img class="avatar" src="http://placehold.it/32x32">',
                '</a>\n',
                '<p class="bio">\n',
                    '{{@bio}}',
                        'age: {{age}}{{=age}}{{:age}}SO OLD{{/age}}\n',
                        'height: {{height}}{{=height}}{{:height}}SO TALL{{/height}}\n',
                        '{{!greeting}}nothing to say{{/greeting}}\n',
                    '{{/bio}}',
                '</p>',
            '{{/users}}',
        '</div>'
    ].join('')

    'new': (id) =>
        ct = @constructor
        return new ct(id)

    render: (obj) =>
        _.extend(@, obj) if obj?

        template = @template or new t(@constructor::template)
        return false if not template?

        id = @id
        element = _.get(id)

        console.log('Preparing to render', @constructor.name, 'into element at ID', id, 'with template', template)
        element.outerHTML = template.render(@)
        element.classList.add('rendered') if not element.classList.contains('rendered')

        @class = element.className
        return @

    constructor: (@id) ->

        @class = @constructor.name.toLowerCase()
        @template = new t(@template)
        return @

class Followers extends Facepile
class Backers extends Facepile
    constructor: (@id, @users) ->
        super
        @supered = true
class Owners extends Facepile
    constructor: (@id, @users) ->
        @supered = false

if @__openfire_preinit?
    @__openfire_preinit.abstract_base_classes.push Facepile
    @__openfire_preinit.abstract_base_classes.push Followers
    @__openfire_preinit.abstract_base_classes.push Backers
    @__openfire_preinit.abstract_base_classes.push Owners
    @__openfire_preinit.abstract_base_controllers.push WidgetController