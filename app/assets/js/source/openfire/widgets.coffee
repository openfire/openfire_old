## openfire widget classes

class WidgetController extends OpenfireController

    @mount: 'widgets'
    @export: 'private'
    constructor: (openfire, window) ->
        @state =
            init: false

        @register = (name, api) =>
            return (if api? and not @[name]? then @[name] = api else false)

        @setAPI = (name, api) =>
            return (if api? and @[name]? then @[name] = api else false)

        @_init = () =>
            @state.init = true
            return @

        return @


class Facepile extends CoreWidget

    @export: 'private'
    @template: null

class AutocompleteAPI extends CoreWidgetAPI

    @mount: 'widgets'
    @export: 'private'
    constructor: (openfire) ->

        @_state =
            store: []
            index: {}

        @get = (id) =>
            return (if (i = @_state.index[id])? then @_state.store[i] else false)

        @new = (element, options) =>
            if not options?
                options = element.getAttribute('data-options')
                options = JSON.parse(options) if options?
            autocomplete = new Autocomplete(element, options)

            @_state.index[autocomplete.element_id] = @_state.store.push(autocomplete) - 1
            autocomplete._init?()

            return autocomplete

        @_init = (openfire) =>
            openfire.widgets.register('autocomplete', @)

            autos = _.get('.autocomplete')
            @new(auto) for auto in autos if autos.length > 0

            @_state.init = true
            return @


class Autocomplete extends CoreWidget

    @export: 'public'
    @template: '<div id="{{=id}}" class="absolute autocomplete-results"></div>'

    constructor: (target, options) ->
        return false if not target.getAttribute('id')?

        @element_id = target.getAttribute('id')
        super(@element_id)

        @choice = null

        @_state =
            active: false
            init: false

            results: []
            cache: []

            config:
                item_template: null     # string template for result item
                length: 3               # characters needed to trigger
                api: 'autocomplete'     # AppTools search service method to call
                result_key: 'ids'       # key on result object to assign to results

        @_state.config = _.extend({}, @_state.config, options)

        @show = () =>
            _.bind(document.body, 'click', @hide)

            _.get(@id).classList.add('active')
            @_state.active = true
            return @

        @hide = () =>
            _.unbind(document.body, 'click', @hide)

            _.get(@id).classList.remove('active')
            @_state.active = false
            return @

        @render = () =>

            el = _.get(@element_id)
            h = el.offsetHeight or el.scrollHeight
            offset = _.get_offset(el)

            autoCSS =
                top:  offset.top + h + 'px'
                left: offset.left + 3 + 'px'

            df = _.create_doc_frag(@template.parse(@))
            df.firstChild.style[prop] = val for prop, val of autoCSS
            document.body.appendChild(df)

            _.bind(el, 'input', @complete)

            @template.t = @_state.config.item_template ||= [
                '{{>_state.results}}',
                    '<div id="autocomplete-result-{{=slug}}" class="autocomplete-result" data-name="{{=name}}">',
                        '{{avatar}}',
                            '<img class="preview-small" src="{{=avatar}}">',
                            '<h6>{{=firstname}} {{=lastname}} ({{=username}})</h6>',
                            '<span>{{=location}}</span>',
                        '{{:avatar}}',
                            '<h4{{none}} class="disabled"{{/none}}>{{=name}}</h4>',
                            '{{description}}<span>{{=description}}</span>{{/description}}',
                        '{{/avatar}}',
                    '</div>',
                '{{/_state.results}}'
            ].join('')

            return @render = () =>

                html = @template.parse(@)
                el = _.get('#'+@id)
                el.innerHTML = html
                result_els = _.filter(_.get('.autocomplete-result', el), (v)-> return (v.classList? and not v.classList.contains('disabled')))
                _.bind(result_els, 'click', @fill)

                @show() if not @_state.active

                return @

        @fill = (e) =>

            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()

                _.unbind(_.get('.autocomplete-result'), 'click', @fill)

                el = _.get('#'+@element_id)
                name = e.target.getAttribute('data-name')
                if not name?
                    node = e.target
                    while node = node.parentNode
                        continue if not node.classList.contains('autocomplete-result')
                        name = node.getAttribute('data-name')
                        break
                choices = @_state.results
                for c in choices
                    continue if c.name isnt name
                    @choice = c
                    break
                return false if not !!@choice

                if @finish?
                    el.value = ''
                    @finish(@)
                else el.value = name

                return @hide()

            else throw 'Autocomplete fill() requires bound event object as first parameter.'

        @complete = (e) =>

            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()

                el = e.target
                input = el.value or el.innerText
                input = input.toLowerCase()

                if input.length < @_state.config.length
                    @hide() if @_state.active
                    return false
                else
                    api = @_state.config.api
                    return $.apptools.api.search[api](query: input).fulfill
                        success: (res) =>
                            results = res[@_state.config.result_key]
                            @_state.cache = @_state.results
                            @_state.results = (if results? then results else [{
                                slug: 'none'
                                name: 'no results found'
                                none: true
                            }])
                            return @render()

                        failure: (err) =>
                            @_state.cache = @_state.results
                            @_state.results = []
                            console.log('Autocomplete API error:', err)
                            return @render()

            else throw 'Autocomplete complete() requires bound event object as first parameter.'


        @_init = () =>
            @render() if @element_id?
            @_state.init = true

            return @

        return @



@__openfire_preinit.abstract_base_classes.push Facepile, AutocompleteAPI, Autocomplete
@__openfire_preinit.abstract_base_controllers.push WidgetController