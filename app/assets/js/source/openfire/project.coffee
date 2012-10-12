## openfire project classes & controllers

# project media
class ProjectImage extends Asset

class ProjectVideo extends Asset

class ProjectAvatar extends Asset


# base project class
class Project extends Model

    @export: 'private'
    @events: ['PROJECT_ASSET_ATTACHED']

    model:
        key: String()
        name: String()
        status: String()
        category: String()
        summary: String()
        pitch: String()
        tech: String()
        keywords: Array()
        creator: String()
        owners: Array()
        public: Boolean()
        viewers: Array()
        backers: Number()
        followers: Number()
        money: Number()
        progress: Number()
        active_goal: String()
        completed_goals: Array()
        future_goal: String()

    constructor: () ->

        super

        @log = () => return console.log.apply(console, arguments)

        @stashes = {}
        @internal =

            new_stash: () =>
                return store: [], index: {}

            clean_stashes: _.debounce(() =>

                @log('Renewing stash indexes...')

                renew = (sn, s) =>
                    store = s.store
                    index = s.index
                    new_store = []
                    new_index = {}

                    (new_index[k] = new_store.push(store[i]) - 1) for k, i of index

                    @stashes[sn] =
                        store: new_store
                        index: new_index

                renew(stashname, stash) for stashname, stash of @stashes
                @log('Index update complete.')

            , 1000)

        @edit = () =>
            return @get (project) =>
                fields = [{
                    name: 'name'
                    attributes:
                        value: project['name']
                        type: 'alphanum'
                        id: 'project-edit-input-name'
                        'data-validation': 'alpha'
                    }]

                areas = []
                for k, v of @constructor::model
                    continue if k not in ['summary', 'pitch', 'tech', 'keywords']
                    area = {}
                    area.name = k
                    area.content = project[k] or ''
                    area.attributes =
                        'data-validation': 'text'
                        id: 'project-edit-input-'+k
                        value: k
                        style: 'width: 90%;margin: 10px auto'

                    areas.push(area)

                df = _.create_doc_frag(ProjectEditModal(fields: fields, areas: areas))
                adf = _.create_doc_frag(_.create_element_string('a',
                    id: 'a-project-editor'
                    style: 'display: none'
                , ''))
                document.body.appendChild(df)
                document.body.appendChild(adf)
                editor = _('#project-editor')
                trigger = _('#a-project-editor')

                return $.apptools.widgets.modal.create(editor, trigger, (m) =>
                    savebtn = _('#project-save')
                    savebtn.bind('click', (_save = (e) =>
                        e.preventDefault()
                        e.stopPropagation()

                        savebtn.unbind('click')
                        return notify('warn', 'saving project', 'Are your project details correct?', {
                                no: =>
                                    notify('notify', 'no changes made', 'keep working :)')
                                    savebtn.bind('click', _save)
                                    return

                                yes: =>
                                    pjct = {}
                                    editor = _('#project-editor-modal-dialog')
                                    inputs = _.to_array(editor.find('input')) or []
                                    texts = _.to_array(editor.find('textarea')) or []
                                    fields = _.join(inputs, texts)
                                    for field in fields
                                        continue if not field.hasAttribute('id')
                                        prop = field.getAttribute('id').split('-').pop()
                                        pjct[prop] = field.val()

                                    @from_message(pjct)

                                    return $.apptools.api.project.put(@to_message()).fulfill
                                        success: (response) =>
                                            notify('yay', 'project saved!', 'project saved successfully, click below to refresh & see updates :)', {ok: -> window.location.reload()})
                                            document.body.style.overflow = 'auto'
                                            return m.close()

                                        failure: (error) =>
                                            return notify('error','whoops', 'something went wrong :( refresh?', {ok: -> window.location.reload()})
                            })
                    ), false)

                    set_focus = (t_f) =>
                        t_f.addEventListener('click', (_focus = (e) =>
                            e.preventDefault()
                            e.stopPropagation()
                            field = e.target
                            return field.focus()
                            ), false)

                    set_focus(tier_field) for tier_field in _.get('.tier-field', editor)

                    if (editorform = _('#project-editor-form'))?
                        $.openfire.forms.register(editorform)

                    document.body.style.overflow = 'hidden'
                    return m.open()
                ,
                    ratio:
                        x: 0.7
                        y: 0.75
                )


        @attach = (obj, callback) =>

            if obj? and obj.key?

                stash_name = obj.constructor.name.toLowerCase()
                key = obj.key

                @stashes[stash_name] ?= @internal.new_stash()

                if @stashes[stash_name].index[key]

                    idx = @stashes[stash_name].index[key]

                    old_store = @stashes[stash_name].store
                    new_store = old_store.slice(0, idx)
                    (_ns = old_store.slice(idx+1)).unshift(obj)

                    new_store.push(item) for item in _ns

                    @stashes[stash_name].store = new_store

                else @stashes[stash_name].index[key] = @stashes[stash_name].store.push(obj) - 1

                $.apptools.events.trigger 'PROJECT_ASSET_ATTACHED', obj, @
                @internal.clean_stashes()

                return if callback? then callback?(obj) else obj

            else if obj?
                throw 'No key found on '+obj.constructor.name+' object.'

            else
                throw 'Too few arguments passed to attach(): function(object, callback=null){}'

        @get_attached = (name, key_or_index, index_only=false) =>

            if name? and key_or_index?

                name = name.toLowerCase()

                if not @stashes[name]?
                    return false
                else
                    if (i = parseInt(key_or_index, 10)) > 0 or i < 0 or i is 0    # if key parse doesn't return NaN, assume it's an index
                        index = i

                    else if key_or_index is true
                        # returns list
                        return @stashes[name].store

                    else if (_i = @stashes[name].index[key_or_index])?
                        index = _i

                    else return false

                    return if index_only then index else @stashes[name].store[index]

            else
                # eventually, calling this with no arguments should sync assets with server. for now you get error.
                throw 'Too few arguments passed to get_attached(): function(modelname, key_or_index, index_only=false)'


        @get = (callback) =>

            return $.apptools.api.project.get(key: @key).fulfill
                success: (response) =>
                    return if callback? then callback?(@from_message(response)) else @from_message(response)

                failure: (error) =>
                    return notify('error','whoops', 'something went wrong :( refresh?', {ok: -> window.location.reload()})


        @put = (callback) =>

            return $.apptools.api.project.put(@to_message()).fulfill
                success: (response) =>
                    return if callback? then callback?(@from_message(response)) else @from_message(response)

                failure: (error) =>
                    return notify('error','whoops', 'something went wrong :( refresh?', {ok: -> window.location.reload()})




# project controller
class ProjectController extends OpenfireController

    @mount = 'project'
    @events = [
        'PROJECT_CONTROLLER_READY',
        'PROJECT_CONTROLLER_INIT',
        'PROJECT_AVATAR_ADDED',
        'PROJECT_IMAGE_ADDED',
        'PROJECT_VIDEO_ADDED',
        'PROJECT_BACKED',
        'PROJECT_EDITED',
        'PROJECT_FOLLOWED',
        'PROJECT_READY',                # @get()
        'PROJECT_SHARED',
        'PROJECT_UPDATED',
    ]

    method_proxies: ['attach', 'get_attached', 'from_message', 'to_message']

    constructor: (openfire) ->

        @_state = _.extend(true, {}, window._cp)

        if @_state.ke and not /proposal/.test(window.location.href)
            @project = new Project(@_state.ke)
            @project.get()

        @log = () => return console.log.apply(console, arguments)

        @internal =

            cleanup: (rootID) =>

                _list = [
                    rootID,
                    rootID+'-modal-dialog',
                    'a-'+rootID,
                    'a-'+rootID+'-modal-dialog'
                ]

                remove = (nodeID) =>
                    node = document.getElementById(nodeID)
                    if node?
                        node.parentNode.removeChild(node)

                remove(_l) while _l = _list.shift()
                return _list

            process_goal: (goal) =>

                ctx = _.extend({type: 'goal'}, goal)
                ctx.index = if goal.key? then @get_attached('goal', goal.key, true) else (ctx.new = true; 'new')

                btnctx =
                    attributes:
                        'data-index': ctx.index

                if !!ctx.new
                    axn = 'add'
                else
                    axn = 'save'

                ctx.buttons = [_.extend(true, {}, btnctx,
                    attributes:
                        'data-action': axn
                        class: 'goal-button '+axn
                    content: axn + ' goal'
                )]

                return ctx

            process_tier: (tier) =>

                ctx = _.extend({type: 'tier'}, tier)
                ctx.index = if tier.key? then @get_attached('tier', tier.key, true) else (ctx.new = true; 'new')

                btnctx =
                    attributes:
                        'data-index': ctx.index

                if !!ctx.new
                    axns = ['add']
                else
                    axns = ['save', 'reset', 'delete']

                ctx.buttons = (_.extend(true, {}, btnctx,
                    attributes:
                        'data-action': axn
                        class: 'tier-button '+axn
                    content: axn + ' tier'
                ) for axn in axns)

                return ctx

            prep_dropped_modal_html: (name, ext) =>
                # takes filename, returns [premodal_element, trigger_element]
                base = 'project-image-drop-'

                @internal.cleanup(base + 'choice')

                preview = _.create_element_string('img',
                    id: base + 'preview'
                    style: 'max-width: 140px;'
                    class: 'dropshadow'
                )

                filename_edit = _.create_element_string('span',
                    id: base + 'filename'
                    class: 'modal-editable alone'
                    'data-ext': '.'+ext
                    contenteditable: true
                , name)

                greeting = _.create_element_string('span',
                    style: 'font-weight: 700; font-size: 14px;'
                , 'Would you like to attach' + filename_edit + 'to your project?')

                attach_avatar = _.create_element_string('button',
                    id: base + 'avatar'
                    class: 'rounded modal-button'
                    value: 'avatar'
                , 'yes!<br>(as an avatar)')

                attach_image = _.create_element_string('button',
                    id: base + 'image'
                    class: 'rounded modal-button'
                    value: 'image'
                , 'yes!<br>(as an image)')

                oops = _.create_element_string('button',
                    id: base + 'no'
                    class: 'rounded modal-button'
                    value: 'oops'
                , 'oops!<br>(no thanks)')

                buttons = [attach_avatar, attach_image, oops].join('')
                content = ['',preview,'','',greeting,'','',buttons].join('<br>')

                pre_modal = _.create_element_string('div',
                    id: base + 'choice'
                    style: 'width: 100%;margin: 0 auto;opacity: 0;text-align: center;background-color: #eee;font-size: 9pt;'
                    class: 'pre-modal'
                    'data-title': 'Hey! You dropped your photo!'
                , content)

                trigger = _.create_element_string('a',
                    id: 'a-' + base + 'choice'
                    href: '#project-image-drop-choice'
                    style: 'display: none;'
                )

                return [pre_modal, trigger]

            prep_goals_modal_html: (goals) =>

                @internal.cleanup('project-goal-editor')

                _goals = []

                blank_goal = new Goal
                    amount: 0
                    description: 'Fill this out to add a goal!'

                _goals.push(@internal.process_goal(blank_goal))
                _goals.push(@internal.process_goal(g)) for g in goals

                pre_modal = window.TierEditModal(false,
                    tiers: _goals
                    type: 'goal'
                )

                trigger = _.create_element_string('a',
                    id: 'a-project-goal-editor'
                    style: 'display: none;')

                return [pre_modal, trigger]

            prep_tiers_modal_html: (tiers) =>

                @internal.cleanup('project-tier-editor')

                _tiers = []

                blank_tier = new Tier
                    name: 'New Tier'
                    amount: 0
                    description: 'Fill this out to add a tier!'

                _tiers.push(@internal.process_tier(blank_tier))
                _tiers.push(@internal.process_tier(t)) for t in tiers

                pre_modal = window.TierEditModal(false, 
                    tiers: _tiers
                    type: 'tier'
                )

                trigger = _.create_element_string('a',
                    id: 'a-project-tier-editor',
                    style: 'display: none;')

                return [pre_modal, trigger]


        @add_media = (file_or_url) =>

            ## attach a media item to a project
            if @_state.o

                if file_or_url.preventDefault
                    # it's an event, grab the files & try again
                    file_or_url.preventDefault()
                    file_or_url.stopPropagation()

                    e = file_or_url
                    files = e.dataTransfer.files

                    return @add_media(fi) for fi in files if files?

                if file_or_url.size and file_or_url.type
                    # it's a file!
                    file = file_or_url
                    filetype = file.type
                    filesize = file.size
                    file_ext = (fn = file.name.split('.')).pop()

                    @log('Received dropped file: '+filetype, file.name)

                    # prep modal
                    modal_parts = @internal.prep_dropped_modal_html(fn.join('.'), file_ext)

                    choice_modal = $.apptools.widgets.modal.create (() =>
                        # pre-modal
                        docfrag = _.create_doc_frag(modal_parts[0])
                        document.body.appendChild(docfrag)
                        return document.getElementById('project-image-drop-choice')
                    )(), (() =>
                        # trigger (not used here but required for create())
                        docfrag = _.create_doc_frag(modal_parts[1])
                        document.body.appendChild(docfrag)
                        return document.getElementById('a-project-image-drop-choice')
                    )(), (m) =>
                        # create() callback
                        return m.open()
                    ,
                        # config for modal
                        initial:
                            width: '0px'
                            height: '0px'
                            bottom: '60px'
                            right: '60px'

                        ratio:
                            x: 0.3
                            y: 0.7

                        calc: () ->
                            css = {}
                            r = @ratio
                            wW = window.innerWidth
                            wH = window.innerHeight
                            mW = Math.floor r.x*wW
                            mH = Math.floor r.y*wH

                            css.width = mW + 'px'
                            css.height = mH + 'px'
                            css.bottom = @initial.bottom
                            css.right = @initial.right

                            return css

                    # construct reader for img preview
                    reader = new FileReader()
                    reader.file = file
                    reader.onloadend = (e) =>
                        e.preventDefault()
                        e.stopPropagation()
                        return _.get('#project-image-drop-preview').setAttribute('src', e.target.result)

                    # simple check for allowed filetypes
                    if /^image\/(png|jpeg|gif)$/gi.test(filetype)

                        # kick off preview
                        reader.readAsDataURL(file)

                        # upload as image
                        _.get('#project-image-drop-image').addEventListener('click', (e) =>

                            if e.preventDefault
                                e.preventDefault()
                                e.stopPropagation()

                            (btn = e.target).innerHTML = 'Great!<br>Uploading...'
                            fn_el = document.getElementById('project-image-drop-filename')
                            filename = fn_el.innerText

                            @log('Uploading dropped file as: ', [filename, file_ext].join('.'))

                            callback = (res) =>
                                # post-upload callback
                                @log('Image upload successful! Attaching image to project...')
                                @attach new ProjectImage(res[0]), () =>
                                    $.apptools.events.trigger 'PROJECT_IMAGE_ADDED', @
                                    btn.style.backgroundColor = '#bada55'
                                    btn.innerHTML = 'Awesome!<br>Good to go.'

                                    return @project

                            $.apptools.api.media.attach_image(
                                target: @project.key
                                size: filesize
                                name: filename
                            ).fulfill
                                success: (response) =>
                                    if not @uploader?
                                        # create uploader if one hasn't been made
                                        uploader = $.apptools.widgets.uploader.create 'array',
                                            id: 'body'
                                            endpoints: [response.endpoint]
                                            finish: callback

                                        @uploader = uploader

                                    else
                                        # update current uploader
                                        uploader = @uploader.set_endpoint(response.endpoint)
                                        uploader = uploader.add_callback(callback)

                                    uploader.upload(file)

                                failure: (error) =>
                                    # apologize and try again
                                    btn.style.backgroundColor = '#ee9099'
                                    btn.innerHTML = 'Sorry!<br>:('
                                    timer = setTimeout(() =>
                                        btn.style.backgroundColor = 'transparent'
                                        btn.innerHTML = 'Try again?<br>:)'
                                    , 600)

                        , false)

                        # upload as avatar
                        _.get('#project-image-drop-avatar').addEventListener('click', (e) =>

                            if e.preventDefault
                                e.preventDefault()
                                e.stopPropagation()

                            (btn = e.target).innerHTML = 'Great!<br>Uploading...'
                            fn_el = document.getElementById('project-image-drop-filename')
                            filename = fn_el.innerText

                            callback = (res) =>
                                @log('Avatar upload successful! Attaching avatar to project...')
                                @attach new ProjectAvatar(res[0]), () =>
                                    $.apptools.events.trigger 'PROJECT_AVATAR_ADDED', @
                                    btn.style.backgroundColor = '#bada55'
                                    btn.innerHTML = 'Awesome!<br>Good to go.'

                                    return @project

                            $.apptools.api.media.attach_avatar(
                                target: @project.key
                                size: filesize
                                name: filename
                            ).fulfill
                                success: (response) =>
                                    if not @uploader?
                                        uploader = $.apptools.widgets.uploader.create 'array',
                                            id: 'body'
                                            endpoints: [response.endpoint]
                                            finish: callback

                                        @uploader = uploader

                                    else
                                        uploader = @uploader.set_endpoint(response.endpoint)
                                        uploader = uploader.add_callback(callback)

                                    uploader.upload(file)

                                failure: (error) =>
                                    btn.style.backgroundColor = '#ee9099'
                                    btn.innerHTML = 'Sorry!<br>:('
                                    timer = setTimeout(() =>
                                        btn.style.backgroundColor = 'transparent'
                                        btn.innerHTML = 'Try again?<br>:)'
                                    , 600)

                        , false)

                        # no thx
                        _.get('#project-image-drop-no').addEventListener('click', (e) =>

                            if e.preventDefault
                                e.preventDefault()
                                e.stopPropagation()

                            return $.apptools.widgets.modal.get('project-image-drop-choice').close()

                        , false)

                        return

                    else throw new MediaError(@constructor.name, 'Tried to upload unsupported filetype. Images must be .jpg, .png, or .gif.')

                else if file_or_url.length and file_or_url.charAt
                    # it's a URL - for now we support video
                    url = file_or_url
                    @log('Received video URL: '+url)

                    $.apptools.api.media.attach_video(
                        reference: url
                        target: @project.key
                    ).fulfill
                        success: (response) =>
                            @attach(new Video(response))
                            $.apptools.events.trigger 'PROJECT_VIDEO_ADDED', @

                        failure: (error) =>
                            notify('error', 'whoops', 'couldn\'t attach your video :(')

                else throw new MediaError(@constructor.name, 'Unrecognized media kind linked.')

            else throw new UserPermissionsError(@constructor.name, 'Current user is not a project owner.')


        @edit = () =>

            ## edit an existing project
            # content api?
            @log('editing functionality currently stubbed.')
            alert('You tried to edit a project! We\'re working on it :)')

        @update = () =>

            ## post an update to a project
            @log('updating functionality currently stubbed.')
            alert('You tried to update a project! We\'re working on it :)')

            ###
            if @_state.o
                $.apptools.api.project.post(target: @project.key).fulfill
                    success: () =>
                        # no response i think?
                        alert 'update() success'

                    failure: (error) =>
                        alert 'update() failure'

            else throw new UserPermissionsError(@constructor.name, 'Current user is not a project owner.')
            ###

        @close_back_dialog = () =>
            $.apptools.widgets.modal.get("back-project-dialog").close()

        @change_backing_tier = () ->
            rads = document.getElementsByName("tier")
            value = ""
            for rad in rads
                if rad.checked
                    value = rad.value
                    # TODO: Use this value to populate number of votes and amount.
                    break

        @vote_plus_clicked = () ->
            # TODO: Increase input here.

        @vote_minus_clicked = () ->
            # TODO: Decread input here.

        @detect_cc_type = () ->
            val = @.value
            type = ""
            if /^4/.test(val)
                type = "Visa"
            if /^(34|37)/.test(val)
                type = "American Express"
            if /^5[1-5]/.test(val)
                type = "MasterCard"
            if /^6011/.test(val)
                type = "Discover"
            document.getElementById("back-project-cc-type-display")?.innerHTML = type
            return false

        @choose_donation_tier = () ->
            # Set the number of next step votes.
            document.getElementById('back-project-remaining-votes').value = this.parentNode.find('num-votes').innerHTML
            document.getElementById('back-project-amount-input').value = parseInt(this.parentNode.find('dollar-amount').innerHTML)

        @next_step_vote_plus = () ->
            # Increment the nearest votes input and decrement the overall votes count.
            increment = this.parentNode.find('back-project-next-step-input')
            decrement = document.getElementById('back-project-remaining-votes')

            remaining = parseInt(decrement.value)
            if remaining > 0
                increment.value = parseInt(increment.value) + 1
                decrement.value = remaining - 1

        @next_step_vote_minus = () ->
            # Decrement the nearest votes input and increment the overall votes count.
            decrement = this.parentNode.find('back-project-next-step-input')
            increment = document.getElementById('back-project-remaining-votes')

            remaining = parseInt(decrement.value)
            if remaining > 0
                increment.value = parseInt(increment.value) + 1
                decrement.value = remaining - 1

        @select_money_source = () ->
            # If a previous money source was selected, clear and disable the new cc form.
            for el in document.getElementById('use-new-cc').find('input')
                if this.value
                    el.value = ''
                    el.disabled = true
                else
                    el.disabled = false

        @submit_payment = () =>
            # Simple way to submit a back project request with a new credit card for now.
            votes = []
            for el in document.getElementsByClassName("back-project-next-step-input")
                votes.push
                    key: el.id
                    num_votes: parseInt(el.value)

            tier = ""
            rads = document.getElementsByName("tier")
            for rad in rads
                if rad.checked
                    tier = rad.value
                    break

            params =
                user: null # TODO: Get user so that we can double check with the session? Should we do that?
                project: @project.key
                tier: tier
                amount: document.getElementById("back-project-amount-input").value
                next_step_votes: votes
                money_source: document.getElementById("back-project-money-source-input").value
                new_cc:
                    cc_num: document.getElementById("back-project-cc-num-input").value
                    ccv: document.getElementById("back-project-cc-ccv-input").value
                    expire_month: document.getElementById("back-project-cc-month-input").value
                    expire_year: document.getElementById("back-project-cc-year-input").value
                    user_name: document.getElementById("back-project-cc-name-input").value
                    email: document.getElementById("back-project-cc-email-input").value
                    address1: document.getElementById("back-project-cc-address-1-input").value
                    address2: document.getElementById("back-project-cc-address-2-input").value
                    city: document.getElementById("back-project-cc-city-input").value
                    state: document.getElementById("back-project-cc-state-input").value
                    country: document.getElementById("back-project-cc-country-input").value
                    zipcode: document.getElementById("back-project-cc-zipcode-input").value
                    save_for_reuse: document.getElementById("back-project-cc-save-input").checked

            # Submit the back request via the payment.back_project service.
            $.apptools.api.payment.back_project(params).fulfill
                success: (response) =>
                    notify('yay', "Success!", response.message)
                    $.apptools.widgets.modal.get("back-project-dialog").close()
                    document.getElementById('back-text').innerHTML = 'you rock.'
                    document.getElementById('back').classList.add('backed')
                failure: (error, status, xhr) =>
                    msg = error.error_message
                    $("#donate-wizard").smartWizard("showMessage", msg)


        @back = () =>

            # Get any existing money sources for this user and populate them in the dialog, then open it.
            $.apptools.api.payment.money_sources().fulfill
                success: (response) =>
                    selector = document.getElementById("back-project-money-source-input")
                    options = selector.innerHTML
                    if response.sources and response.sources.length
                        for source in response.sources
                            options += "<option value='" + source.key + "'>" + source.description + "</option>"
                    else
                        options = "<option value=''>No saved payment accounts</option>"
                    selector.innerHTML = options
                    $.apptools.widgets.modal.get("back-project-dialog").open()
                failure: (error) =>
                    notify('error', 'whoops', 'couldn\'t back project. are you logged in?')
            return

        @propose_goal = () =>
            params =
                project: @project.key
                amount: parseFloat(document.getElementById("propose-goal-amount").value)
                description: document.getElementById("propose-goal-description").value
                funding_day_limit: parseInt(document.getElementById("propose-goal-funding_day_limit").value)
                deliverable_description: document.getElementById("propose-goal-deliverable_description").value
                deliverable_date: new Date(document.getElementById("propose-goal-deliverable_date").value).toISOString()

            $.apptools.api.project.propose_goal(params).fulfill
                success: (response) ->
                    notify('yay', 'goal saved!', 'refreshing page....')
                    setTimeout(window.location.reload, 2000)
                    return

                failure: (error) ->
                    notify('error', 'whoops', 'we couldn\'t save your goal:'+response.responseText)

        @close_propose_goal = () =>
            $.apptools.widgets.modal.get("propose-project-goal").close()

        @follow = () =>

            ## follow a project
            $.apptools.dev.log('OF:Follow', "User clicked 'Follow'...")

            follow_r =
                subject:
                    key: @project.key
                    kind: 'PROJECT'

            return $.apptools.api.project.follow(follow_r).fulfill({

                success: (response) =>
                    $.apptools.dev.log('OF:Follow', "Follow request successful.", response)
                    f_button = document.getElementById('follow')
                    f_button.classList.add('following')

                    $.apptools.analytics.track.social("Project", "Follow", @project.name)

                failure: (response) =>
                    $.apptools.dev.error('OF:Follow', "Follow request failed.", response)
                    f_button = document.getElementById('follow')
                    f_button.classList.add('error')

            })

        @share = (sm_service) =>

            ## share a project via social media
            # what do?

            @log('sharing functionality currently stubbed.')
            notify('warn', 'that tickled!', 'you tried to share a project! we\'re working on it :)')


        @get = (refresh, callback) =>

            ## get the associated project

            if not refresh?         # refresh=true syncs with server
                refresh = false

            else if typeof refresh isnt 'boolean'
                callback ?= refresh
                refresh = false

            if typeof callback isnt 'function'
                callback = null

            return if refresh then @project.get(callback) else if callback? then callback.call(@, @project) else @project

        @get_backers = () =>

            ## get project backers
            $.apptools.api.project.backers(target: @project.key).fulfill

                success: (response) =>
                    # response.users = []
                    alert 'get_backers() success'

                failure: (error) =>
                    alert 'get_backers() failure'


        @get_followers = () =>

            ## get project followers
            $.apptools.api.project.followers(target: @project.key).fulfill

                success: (response) =>
                    alert 'get_followers() success'

                failure: (error) =>
                    notify('error', 'whoops', error.error)


        @get_updates = () =>

            ## get recent updates
            $.apptools.api.project.posts(target: @project.key).fulfill

                success: (response) =>
                    # response.posts = []
                    alert 'get_updates() success'

                failure: (error) =>
                    notify('error', 'whoops', error.error)

        @edit_goal = () => return @tiers.edit.apply(@, arguments)
        @edit_tier = () => return @tiers.edit.apply(@, arguments)

        @goals =

            get: (goal_key, callback, sync) =>

                ## get goal by key

                if not sync?
                    if callback? and typeof callback is 'boolean'
                        sync = callback
                        callback = null
                    else sync = false

                if not sync
                    goal = @get_attached('goal', goal_key)
                    return if callback? then callback.call(@, goal) else goal

                else
                    # get from the server
                    $.apptools.api.project.get_goal(
                        key: goal_key
                        project: @project.key
                    ).fulfill
                        success: (response) =>
                            goal = @attach(new Goal(target: @project.key).from_message(response.goal))

                            return if callback? then callback.call(@, goal) else goal

                        failure: (error) =>
                            alert 'goals.get() failure'


            list: (callback, sync) =>

                ## list goals by project key
                if not sync?
                    if callback? and typeof callback is 'boolean'
                        sync = callback
                        callback = null
                    else sync = false

                if not sync
                    goals = @get_attached('goal', true)
                    return if callback? then callback.call(@, goals) else goals

                else
                    # get from the server
                    $.apptools.api.project.list_goals(project: @project.key).fulfill

                        success: (response) =>
                            goals = []
                            goals.push(@attach(new Goal(target: @project.key).from_message(goal))) for goal in response.goals

                            return if callback? then callback.call(@, goals) else goals

                        failure: (error) =>
                            alert 'goals.list() failure'
                            @log('Error listing goals: ' + error)

            put: (goal, callback) =>

                ## put goal by key
                $.apptools.api.project.put_goal(goal.to_message()).fulfill

                    success: (response) =>
                        alert 'goals.put() success'
                        return if callback? then callback.call(@, response) else response.key

                    failure: (error) =>
                        alert 'goals.put() failure'

            delete: (goal_key, callback) =>

                ## delete goal by key
                $.apptools.api.project.delete_goal({key: goal_key}).fulfill

                    success: (response) =>
                        alert 'goals.delete() success'
                        return if callback? then callback.call(@, response) else response.key

                    failure: (error) =>
                        alert 'goals.delete() failure'

            edit_current: (e) =>

                if (trigger = e.target)?
                    trigger.classList.add('init') if (sync = not trigger.classList.contains('init'))

                else if typeof e is 'boolean'
                    sync = e

                else sync = false

                current = @project.active_goal
                return @goals.get(current, (goal) =>
                    goal_modal_parts = @internal.prep_goals_modal_html(goal, '')

                    return @goals.return $.apptools.widgets.modal.create (() =>
                        docfrag = _.create_doc_frag(goal_modal_parts[0])
                        document.body.appendChild(docfrag)
                        return document.getElementById('project-goal-editor')
                    )(), (() =>
                        docfrag = _.create_doc_frag(goal_modal_parts[1])
                        document.body.appendChild(docfrag)
                        return document.getElementById('a-project-goal-editor')
                    )(), ((m) =>
                        editor = document.getElementById(m._state.element_id)

                        save_button.addEventListener('click', (_save = (e) =>
                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            idx = btn.getAttribute('data-index')

                            return notify('warn', 'saving goal', 'ready to save?', {

                                no: =>

                                    notify('notify', 'goal not saved', 'keep on working :)')
                                    btn.addEventListener('click', _save, false)
                                    return

                                yes: =>

                                    amount_el = _('#goal-amount-'+idx)
                                    description_el = _('#goal-description-'+idx)
                                    name_el = _('#goal-name-'+idx)

                                    return $.apptools.api.project.put_goal(_.extend((if idx isnt 'new' then @get_attached('goal', idx) else new Goal()),

                                        target: @project.key
                                        amount: parseInt(amount_el.val())
                                        description: _('#goal-description-'+idx).val()
                                        name: _('#goal-name-'+idx).val()

                                    ).to_message()).fulfill

                                        success: (response) =>

                                            notify('yay', 'goal saved', 'updating info...')

                                            return @attach new Goal().from_message(response), (goal) =>

                                                k = goal.key

                                                _('#a-'+k).innerHTML = goal.name + ' - ' + _.currency(goal.amount)
                                                _('#'+k).innerHTML = '<p>'+goal.description+'</p>'

                                                amount_el.val goal.amount
                                                name_el.val goal.name
                                                description_el.val goal.description

                                                btn.innerHTML = 'save goal'
                                                btn.bind('click', _save)

                                                return goal

                                        failure: (error) =>
                                            notify('error', 'whoops', 'couldn\'t save goal, sorry :(. try again, or hit OK to refresh', {ok: -> window.location.reload()})

                                            btn.bind('click', _save)
                                            return false

                            })

                            ), false) for save_button in _.get('.save', editor)

                        set_focus = (g_f) =>
                            g_f.addEventListener('click', (_focus = (e) =>
                                e.preventDefault()
                                e.stopPropagation()
                                field = e.target
                                field.innerHTML = ''
                                return field.focus()
                            ), false)

                        set_focus(goal_field) for goal_field in _.get('.goal-field', editor)

                        return m.open()

                    ),
                        initial:
                            width: '0px'
                            height: '0px'
                            bottom: '60px'
                            right: '60px'

                        ratio:
                            x: 0.3
                            y: 0.85

                        calc: () ->

                            css = {}
                            r = @ratio
                            wW = window.innerWidth
                            wH = window.innerHeight
                            mW = Math.floor r.x*wW
                            mH = Math.floor r.y*wH

                            css.width = mW + 'px'
                            css.height = mH + 'px'
                            css.bottom = @initial.bottom
                            css.right = @initial.right

                            return css

                , true)


        @tiers =

            ## get single tier by key
            get: (t_key, callback, sync) =>

                if not sync?
                    if callback? and typeof callback is 'boolean'
                        sync = callback
                        callback = null
                    else sync is false

                if not sync
                    tier = @get_attached('tier', t_key)
                    return if callback? then callback.call(@, tier) else tier

                else
                    # get from the server
                    return $.apptools.api.project.get_tier(key: t_key).fulfill
                        success: (response) =>
                            tier = @attach(new Tier().from_message(response))
                            return if callback? then callback.call(@, tier) else tier

                        failure: (error) =>
                            notify('error', 'whoops', 'couldn\'t get project tiers from server. refresh page?', {ok: -> window.location.reload()})

            ## get all project tiers
            list: (callback, sync) =>

                if not sync?
                    if callback? and typeof callback is 'boolean'
                        sync = callback
                        callback = null
                    else sync is false

                if not sync
                    # return cached
                    tiers = @get_attached('tier', true)
                    return if callback? then callback.call(@, tiers) else tiers

                else
                    # pull from the server
                    return $.apptools.api.project.list_tiers(goal: @project.active_goal).fulfill
                        success: (response) =>
                            tiers = []
                            tiers.push(@attach(new Tier().from_message(tier))) for tier in response.tiers

                            return if callback? then callback.call(@, tiers) else tiers

                        failure: (error) =>
                            notify('error', 'whoops', 'couldn\'t get project tiers from server. refresh page?', {ok: -> window.location.reload()})

            ## put tier by key
            put: (tier, callback) =>

                return $.apptools.api.project.put_tier(tier.to_message()).fulfill
                    success: (response) =>
                        notify('yay', 'tier saved', ':)')
                        return if callback? then callback.call(@, response) else response.key

                    failure: (error) =>
                        notify('error', 'whoops', 'couldn\'t save tier. refresh page?', {ok: -> window.location.reload()})

            ## delete tier by key
            delete: (tier_key, callback) =>

                return $.apptools.api.project.delete_tier({key: tier_key}).fulfill
                    success: (response) =>
                        notify('notify', 'tier deleted', 'bye bye')
                        return if callback? then callback.call(@, response) else response.key

                    failure: (error) =>
                        notify('error', 'whoops', 'couldn\'t delete tier. refresh page?', {ok: -> window.location.reload()})

            ## edit
            edit: (e) =>

                ## coordinates editing tier properties

                if (trigger = e.target)?
                    trigger.classList.add('init') if (sync = not _.has_class(trigger, 'init'))

                else if typeof e is 'boolean'
                    sync = e

                else sync = false

                return @tiers.list (tiers) =>

                    _t.target = @project.key for _t in tiers

                    tier_modal_parts = @internal.prep_tiers_modal_html(tiers)

                    return $.apptools.widgets.modal.create (() =>
                        docfrag = _.create_doc_frag(tier_modal_parts[0])
                        document.body.appendChild(docfrag)
                        return document.getElementById('project-tier-editor')
                    )(), (() =>
                        docfrag = _.create_doc_frag(tier_modal_parts[1])
                        document.body.appendChild(docfrag)
                        return document.getElementById('a-project-tier-editor')
                    )(), (m) =>
                        editor = _('#'+m.id)

                        save_button.addEventListener('click', (_save = (e) =>
                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            idx = btn.getAttribute('data-index')

                            return notify('warn', 'saving tier', 'ready to save?', {

                                no: =>

                                    notify('notify', 'tier not saved', 'keep on working :)')
                                    btn.addEventListener('click', _save, false)
                                    return

                                yes: =>

                                    amount_el = _('#tier-amount-'+idx)
                                    description_el = _('#tier-description-'+idx)
                                    name_el = _('#tier-name-'+idx)

                                    return $.apptools.api.project.put_tier(_.extend((if idx isnt 'new' then @get_attached('tier', idx) else new Tier()),

                                        target: @project.key
                                        amount: parseInt(amount_el.val())
                                        description: _('#tier-description-'+idx).val()
                                        name: _('#tier-name-'+idx).val()

                                    ).to_message()).fulfill

                                        success: (response) =>

                                            notify('yay', 'tier saved', 'updating info...')

                                            return @attach new Tier().from_message(response), (tier) =>

                                                k = tier.key

                                                _('#a-'+k).innerHTML = tier.name + ' - ' + _.currency(tier.amount)
                                                _('#'+k).innerHTML = '<p>'+tier.description+'</p>'

                                                amount_el.val tier.amount
                                                name_el.val tier.name
                                                description_el.val tier.description

                                                btn.innerHTML = 'save tier'
                                                btn.bind('click', _save)

                                                return tier

                                        failure: (error) =>
                                            notify('error', 'whoops', 'couldn\'t save tier, sorry :(. try again, or hit OK to refresh', {ok: -> window.location.reload()})

                                            btn.bind('click', _save)
                                            return false

                            })

                        ), false) for save_button in _.get('.save', editor)

                        delete_button.addEventListener('click', (_delete = (e) =>
                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            idx = btn.getAttribute('data-index')

                            tier = @get_attached('tier', idx)

                            return notify('warn', 'deleting tier', 'are you sure you want to delete "'+tier.name+'"?', {

                                no: =>

                                    notify('notify', 'tier not deleted', '')
                                    btn.addEventListener('click', _delete)
                                    return

                                yes: =>

                                    tier_edit_el = _('#tier-editing-'+idx)
                                    tier_trigger = _('#a-'+tier.key)
                                    tier_el = _('#'+tier.key)

                                    return $.apptools.api.project.delete_tier(key: tier.key).fulfill
                                        success: (response) =>
                                            notify('yay', 'tier deleted', 'tier successfully deleted. updating page...')
                                            tier_edit_el.fadeOut(
                                                complete: ->
                                                    tier_edit_el.remove()
                                                    tier_trigger.remove()
                                                    tier_el.remove()
                                            )
                                            return true

                                        failure: (error) =>
                                            notify('error', 'whoops', 'couldn\'t delete tier, sorry :(. try again, or hit OK to refresh', {ok: -> window.location.reload()})

                                            btn.bind('click', _delete)
                                            return false

                            })

                        ), false) for delete_button in _.get('.delete', editor)

                        reset_button.addEventListener('click', (_reset = (e) =>
                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            idx = btn.getAttribute('data-index')

                            tier = @get_attached('tier', idx)

                            return notify('warn', 'resetting tier', 'Really discard your changes and reset tier to saved version?', {

                                no: =>

                                    notify('notify', 'tier not reset', 'keep on working :)')
                                    btn.addEventListener('click', _reset)
                                    return

                                yes: =>

                                    return $.apptools.api.project.get_tier(key: tier.key).fulfill

                                        success: (response) =>

                                            notify('yay', 'tier reset!', 'reset tier info. applying changes...')

                                            return @attach new Tier().from_message(response), (_tier) =>

                                                _('#tier-name-'+idx).val _tier.name
                                                _('#tier-amount-'+idx).val _tier.amount
                                                _('#tier-description-'+idx).val _tier.description

                                                btn.addEventListener('click', _reset)

                                                return _tier

                                        failure: (error) =>

                                            notify('error', 'whoops', 'couldn\'t reset tier, sorry :(. try again, or hit OK to refresh', {ok: -> window.location.reload()})

                                            btn.bind('click', _reset)
                                            return false

                            })

                        ), false) for reset_button in _.get('.reset', editor)

                        add_button.addEventListener('click', (_add = (e) =>
                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            idx = 'new'

                            amount_el = _('#tier-amount-'+idx)
                            description_el = _('#tier-description-'+idx)
                            name_el = _('#tier-name-'+idx)

                            new_edit_el = amount_el.parentNode.parentNode

                            return notify('warn', 'add tier', 'ready to add tier to project?', {

                                no: =>

                                    notify('notify', 'tier not added', 'keep on working :)')
                                    btn.addEventListener('click', _add)
                                    return

                                yes: =>

                                    return $.apptools.api.project.put_tier(new Tier(

                                        target: @project.key
                                        amount: parseInt(amount_el.val())
                                        description: description_el.val()
                                        name: name_el.val()

                                    ).to_message()).fulfill
                                        success: (response) =>
                                            notify('yay', 'tier added', 'hooray :)')

                                            return @attach new Tier(target: @project.key).from_message(response), (_tier) =>
                                                k = _tier.key
                                                index = @get_attached('tier', k, true)

                                                df = _.create_doc_frag(TierEditModalItem(@internal.process_tier(_tier)))
                                                new_edit_el.parentNode.insertBefore(df, new_edit_el.nextSibling)

                                                name_el.val 'New Tier'
                                                amount_el.val 0
                                                description_el.val 'Fill this out to add a tier!'

                                                btn.addEventListener('click', _add, false)

                                                added = document.getElementById('tier-editing-'+index)

                                                sv_btn.addEventListener('click', _save, false) for sv_btn in _.get('.save', added)
                                                rst_btn.addEventListener('click', _reset, false) for rst_btn in _.get('.reset', added)
                                                del_btn.addEventListener('click', _delete, false) for del_btn in _.get('.delete', added)

                                                return @project.put()


                                        failure: (error) =>
                                            notify('error', 'whoops', 'couldn\'t add tier, sorry :(. try again, or hit OK to refresh', {ok: -> window.location.reload()})

                                            btn.innerHTML = 'add tier'
                                            btn.bind('click', _add)
                                            return false

                            })

                        ), false) for add_button in _.get('.add', editor)

                        set_focus = (t_f) =>
                            t_f.addEventListener('click', (_focus = (e) =>
                                e.preventDefault()
                                e.stopPropagation()
                                field = e.target
                                return field.focus()
                                ), false)

                        set_focus(tier_field) for tier_field in _.get('.tier-field', editor)

                        if (editorform = editor.find('form'))?
                            $.openfire.forms.register(editorform)

                        return m.open()

                    ,
                        initial:
                            width: '0px'
                            height: '0px'
                            bottom: '60px'
                            right: '60px'

                        ratio:
                            x: 0.3
                            y: 0.5

                        calc: () ->

                            css = {}
                            r = @ratio
                            wW = window.innerWidth
                            wH = window.innerHeight
                            mW = Math.floor r.x*wW
                            mH = Math.floor r.y*wH

                            css.width = mW + 'px'
                            css.height = mH + 'px'
                            css.bottom = @initial.bottom
                            css.right = @initial.right

                            return css

                , sync

        @go_live = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.project.go_live(key: @project.key).fulfill
                success: () ->
                    notify('yay', 'your project is live!', 'refresh page?', {ok: -> window.location.reload()})
                failure: (response) ->
                    notify('error', 'whoops', response.error)

        @suspend = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.project.suspend(key: @project.key).fulfill
                success: () ->
                    notify('notify', 'project suspended', 'refresh page?', {ok: -> window.location.reload()})
                failure: (response) ->
                    notify('error', 'whoops', response.error)

        @shutdown = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.project.shutdown(key: @project.key).fulfill
                success: () ->
                    notify('notify', 'project closed', 'refresh page?', {ok: -> window.location.reload()})
                failure: (response) ->
                    notify('error', 'whoops', response.error)

        @cancel = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.project.cancel(key: @project.key).fulfill
                success: () ->
                    notify('error', 'project canceled', 'all payments will be refunded. refreshing page?', {ok: -> window.location.reload()})
                failure: (response) ->
                    notify('error', 'whoops', response.error)


        @approve_goal = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            key = document.getElementById("proposed-goal-key").value
            $.apptools.api.project.approve_goal(key: key).fulfill
                success: () ->
                    notify('yay', 'goal approved', 'refresh page?', {ok: -> window.location.reload()})
                failure: (response) ->
                    notify('error', 'whoops', response.error)

        @reject_goal = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            key = document.getElementById("proposed-goal-key").value
            $.apptools.api.project.reject_goal(key: key).fulfill
                success: () ->
                    notify('notify', 'goal rejected', 'refresh page?', {ok: -> window.location.reload()})
                failure: (response) ->
                    notify('error', 'whoops', response.error)

        @review_goal = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            key = document.getElementById("proposed-goal-key").value
            $.apptools.api.project.review_goal(key: key).fulfill
                success: () ->
                    notify('notify', 'goal returned', 'goal returned for review. refresh page?', {ok: -> window.location.reload()})
                failure: (response) ->
                    notify('error', 'whoops', response.error)

        @submit_proposed_goal = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            key = document.getElementById("proposed-goal-key").value
            $.apptools.api.project.submit_proposed_goal(key: key).fulfill
                success: () ->
                    notify('yay', 'goal submitted', 'goal submitted for approval. refresh page?', {ok: -> window.location.reload()})
                failure: (response) ->
                    notify('error', 'whoops', response.error)

        @reopen_proposed_goal = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            key = document.getElementById("proposed-goal-key").value
            $.apptools.api.project.reopen_proposed_goal(key: key).fulfill
                success: () ->
                    notify('yay', 'goal re-opened', 'refresh page?', {ok: -> window.location.reload()})
                failure: (response) ->
                    notify('error', 'whoops', response.error)

        @open_goal= (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.project.open_goal(key: @project.active_goal).fulfill
                success: () ->
                    notify('yay', 'goal opened', 'refresh page?', {ok: -> window.location.reload()})
                failure: (response) ->
                    notify('error', 'whoops', response.error)

        @close_goal = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.project.close_goal(key: @project.active_goal).fulfill
                success: () ->
                    notify('notify', 'goal closed', 'refresh page?', {ok: -> window.location.reload()})
                failure: (response) ->
                    notify('error', 'whoops', response.error)

        @_init = () =>

            if window._cp and _.get('#project')?

                # setup project method proxies
                ((m) =>
                    @[m] = () => return @project[m].apply(@project, arguments)
                )(method) for method in @constructor::method_proxies

                # event listeners
                document.getElementById('follow').addEventListener('click', @follow, false)
                document.getElementById('share').addEventListener('click', @share, false)
                document.getElementById('back')?.addEventListener('click', @back, false)

                # Event listeners in the back project dialog.
                for el in document.getElementsByClassName('vote-plus')
                    el.addEventListener('click', @next_step_vote_plus, false)
                for el in document.getElementsByClassName('vote-minus')
                    el.addEventListener('click', @next_step_vote_minus, false)
                for el in document.getElementById('donate-step-1')?.find('input')?
                    el.addEventListener('click', @choose_donation_tier, false)
                document.getElementById('back-project-money-source-input')?.addEventListener('change', @select_money_source)
                _.ready () =>
                    $("#donate-wizard").smartWizard
                        onFinish: @submit_payment

                if @_state.o and not /proposal/.test(window.location.href)
                    document.body.addEventListener('drop', @add_media, false)

                    # BBQ Actions
                    document.getElementById('bbq-live')?.addEventListener('click', @go_live, false)
                    document.getElementById('bbq-suspend')?.addEventListener('click', @suspend, false)
                    document.getElementById('bbq-shutdown')?.addEventListener('click', @shutdown, false)
                    document.getElementById('bbq-cancel')?.addEventListener('click', @cancel, false)

                    # Project Owner Actions
                    document.getElementById('promote-project')?.addEventListener('click', @project.edit, false)
                    document.getElementById('promote-tiers')?.addEventListener('click', @tiers.edit, false)
                    document.getElementById('promote-goals')?.addEventListener('click', @goals.edit, false)
                    document.getElementById('promote-live')?.addEventListener('click', @go_live, false)
                    document.getElementById('promote-suspend')?.addEventListener('click', @suspend, false)
                    document.getElementById('promote-shutdown')?.addEventListener('click', @shutdown, false)
                    document.getElementById('promote-cancel')?.addEventListener('click', @cancel, false)

                    # Propose a new goal
                    document.getElementById('submit-proposed-goal')?.addEventListener('click', @propose_goal, false)
                    document.getElementById('cancel-submit-proposed-goal')?.addEventListener('click', @close_propose_goal, false)
                    if document.getElementById('propose-goal-deliverable_date')
                        dpicker = new datepickr('propose-goal-deliverable_date', { dateFormat: 'm-d-Y' })

                    # Owner goal actions
                    document.getElementById('owner-open-goal')?.addEventListener('click', @open_goal, false)
                    document.getElementById('owner-close-goal')?.addEventListener('click', @close_goal, false)
                    document.getElementById('owner-submit-proposed-goal')?.addEventListener('click', @submit_proposed_goal, false)
                    document.getElementById('owner-reopen-proposed-goal')?.addEventListener('click', @reopen_proposed_goal, false)
                    document.getElementById('owner-edit-proposed-goal')?.addEventListener('click', @edit_goal, false)

                    # BBQ goal actions
                    document.getElementById('bbq-open-goal')?.addEventListener('click', @open_goal, false)
                    document.getElementById('bbq-close-goal')?.addEventListener('click', @close_goal, false)
                    document.getElementById('bbq-approve-proposed-goal')?.addEventListener('click', @approve_goal, false)
                    document.getElementById('bbq-reject-proposed-goal')?.addEventListener('click', @reject_goal, false)
                    document.getElementById('bbq-review-proposed-goal')?.addEventListener('click', @review_goal, false)

                    document.getElementById('promote-dropzone')?.addEventListener('dragenter', d_on = (ev) ->
                        if ev?.preventDefault
                            ev.preventDefault()
                            ev.stopPropagation()

                        ev.target.classList.add('hover')
                    , false)
                    document.getElementById('promote-dropzone')?.addEventListener('dragover', d_on, false)
                    document.getElementById('promote-dropzone')?.addEventListener('dragleave', d_off = (ev) ->
                        if ev?.preventDefault
                            ev.preventDefault()
                            ev.stopPropagation()

                        ev.target.className = 'dropzone'
                    , false)
                    document.getElementById('promote-dropzone')?.addEventListener('dragexit', d_off, false)
                    document.getElementById('promote-dropzone')?.addEventListener('drop', ((ev) =>
                        d_off(ev)
                        return @add_media(ev)
                    ), false)

            window.__pr = new Project('my-test-project-key')
            return @get()


if @__openfire_preinit?
    @__openfire_preinit.abstract_base_objects.push Asset, ProjectImage, ProjectVideo, ProjectAvatar
    @__openfire_preinit.abstract_base_classes.push Project, Proposal
    @__openfire_preinit.abstract_base_controllers.push ProjectController, ProposalController
