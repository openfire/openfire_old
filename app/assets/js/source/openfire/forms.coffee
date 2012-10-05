# openfire form classes & controller
class FormObject extends OpenfireObject

    @export = 'public'

    constructor: (form) ->
        texts = form.find('textarea') or []
        @name = form.name or form.getAttribute('id')
        @action = form.action
        @method = form.method
        @fields = _.map(form.find('input').concat(texts), (it, i, arr) -> return arr[i] = (n = it.name or it.getAttribute('id')))

        console.log('[Forms]', 'Form registered:', @name)
        return @

class FormController extends OpenfireController

    @mount = 'forms'
    @events = [
        'FORM_VALIDATED',
        'FORM_SUBMITTED'
    ]
    @export = 'private'

    triml = /^\s*/g
    trimr = /\s*$/g
    patterns =
        email: /^([\w!#\$%&'\*\+-\/=\?^_`\{\|\}~\.]+)@{1}((?:[\w\-]+\.?)+[a-z]{2,4})$/i # (_, local, domain)
        tel: /^\(?([0-9]{3})\)?[\-\.\s]?([0-9]{3})[\-\.\s]?([0-9]{4})$/                 # (_, areacode, #{3}, #{4})
        url: /^(https?|s?ftp|wss?|git|ssh|rtmp|smb):\/\/((?:\w+\.?)+)(\w{2,4})$/i       # (_, protocol, inner, suffix)
        date: /^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})$/                               # (_, day, month, year)
        ssn: /^(\d{3})[\-\s](\d{2})[\-\s](\d{4})$/                                      # (_, #{3}, #{2}, #{4})
        alpha: /^[a-z]+$/i
        alphanum: /^\w+$/
        number: /^-?\d+$/
        text: /^[\w\W]*$/

    constructor: (openfire, window) ->

        @_state =
            data: []
            index: {}
            init: false

        @_init = () =>

            forms = document.forms

            for form in forms
                f = new FormObject(form)
                @_state.index[f.name] = @_state.data.push(f) - 1
                for input in form.find('input').concat(form.find('textarea'))
                    if input
                        type = input.type or 'text'
                        type = 'multi' if type is 'radio' or 'checkbox'

                        input.data('validation', type)
                        input.addEventListener('blur', @validate, false)

            @_state.init = true
            return @

        @validate = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()

                input = e.target
                input.removeClass('valid') if input.hasClass('valid')
                input.removeClass('invalid') if input.hasClass('invalid')

                vtype = input.data('validation') or 'text'
                name = input.name or input.getAttribute('id')

                console.log('validating input:', name)
                #input.disabled = true

                return @constructor::[vtype](input)

                ###

                valid = @constructor::[type](value, validre)
                if _.is_string(valid)
                    input.val(valid)
                    input.classList.add('valid')

                    console.log('input validated:', name)
                    return true

                else if _.is_raw_object(valid)
                    input.data('message', valid.error)

                else
                    input.data('message', 'An unknown error occurred. We\'re terribly embarrassed.')

                input.classList.add('invalid')
                console.log('unable to validate input:', name)

                ###
            return @

        return @

    multi: (input) ->
        name = input.name
        type = input.type

        return false if not name?
        checked = false
        val = if type is 'radio' then null else []

        multiset = _.to_array(input.parentNode[name])
        while m = multiset.shift()
            continue if not m.checked
            checked = true
            if type is 'radio'
                val = m.value
                break
            else
                val.push(m.value)
                continue

        return val

    email: (val, re) ->
        _val = val.replace re, (_, local, domain) ->
            return local.toLowerCase()+'@'+domain.toLowerCase()
    phone: (val, re) ->
        _val = val.replace re, (_, areacode, three, four) ->
            return '('+areacode+') '+three+'-'+four
    url: (val, re) ->
        _val = val.replace re, (_, protocol, inner, suffix) ->
            #parts = _.filter(inner.split('.'), (it) -> return it isnt '')
            return protocol+'://'+inner+'.'+suffix
    date: (val, re) ->
        _val = val.replace re, (_, day, month, year) ->
            return (if year.length < 3 then (if parseInt(year) < 13 then'20'+year else '19'+year) else year)+'-'+_.zero_fill(month, 2)+'-'+_.zero_fill(day, 2)
    ssn: (val, re) ->
        _val = val.replace re, (_, three, two, four) ->
            return '***-**-'+four
    alpha: (val, re) ->
        _val = re.test(val)
    alphanum: (val, re) ->
        _val = re.test(val)
    num: (val, re) ->
        _val = re.test(val)

@__openfire_preinit.abstract_base_objects.push FormObject
@__openfire_preinit.abstract_base_controllers.push FormController
