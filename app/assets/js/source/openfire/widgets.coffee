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
        '<div class="{{class}}">',
            '{{#users}}',
                '<a href="https://www.openfi.re/{{username}}" data-firstname="{{firstname}}">',
                    '<img class="avatar" src="http://placehold.it/32x32">'
                '</a>',
            '{{/users}}',
            '{{^users}}no users here :({{/users}}'
        '</div>'
    ].join('')

    'new': (id, users) =>
        ct = @constructor
        return new ct(id, users)

    render: () =>

        renderer = Milk or null
        return false if not renderer?

        template = @constructor::template
        id = @id
        element = _.get(id)

        console.log('Preparing to render', @constructor.name, 'into element at ID', id, 'with template', template)
        element.outerHTML = renderer.render(template, @)

        return @

    constructor: (@id, @users) ->
        @class = @constructor.name.toLowerCase()
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