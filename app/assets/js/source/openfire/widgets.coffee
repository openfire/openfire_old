## openfire widget classes

class WidgetController extends OpenfireController

    @mount: 'widgets'
    @export: 'private'
    constructor: (openfire, window) ->
        @state =
            widgets: []
        @widget = null
        @_init = () =>
            return @

        return @


class Facepile extends CoreWidget

    @export: 'private'
    @template: null

class Autocomplete extends CoreWidget

    @export: 'public'
    @template: '<div id="{{=id}}" class="absolute autocomplete"></div>'

    constructor: (openfire, element_id, options) ->
        super(element_id)

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
            _.get(@id).classList.add('active')
            @_state.active = true
            return @

        @hide = () =>
            _.get(@id).classList.remove('active')
            @_state.active = false
            return @

        @render = () =>

            el = _.get(@element_id)
            w = el.scrollWidth
            h = el.scrollHeight
            offset = _.get_offset(el)

            autoCSS =
                width: w + 'px'
                top:  offset.top + h + 'px'
                left: offset.left + 'px'

            df = _.create_doc_frag(@template.render(@))
            df.firstChild.style[prop] = val for prop, val of autoCSS
            document.body.appendChild(df)

            _.bind(el, 'input', @complete)

            @template.t = @_state.config.item_template ||= [
                '{{>_state.results}}',
                    '<div id="autocomplete-result-{{=slug}}" class="autocomplete-result" data-name="{{<name}}">',
                        '{{avatar}}',
                            '<img class="preview-small" src="{{=avatar}}">',
                            '<h6>{{=firstname}} {{=lastname}} ({{=username}})</h6>',
                            '<span>{{=location}}</span>',
                        '{{:avatar}}',
                            '<h6>{{&1}}</h6>',
                            '<span>{{=description}}</span>',
                        '{{/avatar}}',
                    '</div>',
                '{{/_state.results}}'
            ].join('')

            return @render = () =>
                @hide()
                setTimeout(@show, 350)

                html = @template.render(@)
                el = _.get(@id)
                el.innerHTML = html
                _.bind(_.get('.autocomplete-result', el), 'click', @fill, true)

                return @

        @fill = (e) =>

            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()

                el = _.get('#'+@element_id)
                name = e.target.getAttribute('data-name')
                choices = @_state.results
                for c in choices
                    continue if c.name isnt name
                    @choice = c
                    break
                return false if not !!@choice
                el.value = name

                return @

            else throw 'Autocomplete fill() requires bound event object as first parameter.'

        @complete = (e) =>

            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()

                el = e.target
                input = el.value or el.innerText
                if input.length < @_state.config.length
                    return false
                else
                    api = @_state.config.api
                    return $.apptools.api.search[api](query: input).fulfill
                        success: (res) =>
                            @_state.cache = @_state.results
                            @_state.results = res[@_state.config.result_key]
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



@__openfire_preinit.abstract_base_classes.push Facepile, Autocomplete
@__openfire_preinit.abstract_base_controllers.push WidgetController