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

    errors =
        email: 'youruser@email.com'
        tel: '(XXX) XXX-XXXX'
        url: 'http://www.mysite.com'
        date: 'MM/DD/YYYY'
        ssn: 'XXX-XX-XXXX'
        alpha: 'Allowed: [a-zA-Z]'
        alphanum: 'Allowed: [a-zA-Z0-9]'
        number: 'Allowed: [0-9]'
        text: 'Text only please!'

    replaces =
        email: (_, local, domain) -> return local.toLowerCase()+'@'+domain.toLowerCase()
        tel: (_, areacode, three, four) -> return '('+areacode+') '+three+'-'+four
        url: (_, protocol, inner, suffix) -> return protocol+'://'+inner+'.'+suffix
        date: (_, day, month, year) -> return (if year.length < 3 then (if parseInt(year) < 13 then'20'+year else '19'+year) else year)+'-'+_.zero_fill(month, 2)+'-'+_.zero_fill(day, 2)
        ssn: (_, three, two, four) -> return '***-**-'+four
        alpha: (x) -> return x
        alphanum: (x) -> return x
        number: (x) -> return x
        text: (x) -> return x

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
                        type = 'text' if type is 'textarea'
                        type = 'multi' if type is 'radio' or type is 'checkbox'

                        if not input.data('validation')?
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

                type = input.data('validation') or 'text'
                name = input.name or input.getAttribute('id')
                val = input.val()

                return if val is ''

                console.log('validating input:', name)
                #input.disabled = true

                if type isnt 'multi'
                    re = patterns[type]
                    if re.test(val)
                        input.disabled = false
                        _val = val.replace(re, replaces[type])
                        input.val(_val)
                        @constructor::valid(input)
                    else
                        input.disabled = false
                        input.val('')
                        input.setAttribute('placeholder', errors[type])
                        @constructor::invalid(input)

                    return input

            return @

        return @

    valid: (input) ->
        input.classList.remove('invalid') if input.hasClass('invalid')
        input.classList.add('valid')
        return input

    invalid: (input) ->
        input.classList.remove('valid') if input.hasClass('valid')
        input.classList.add('invalid')
        return input


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


@__openfire_preinit.abstract_base_objects.push FormObject
@__openfire_preinit.abstract_base_controllers.push FormController
