## openfire proposal classes & controllers

# proposal media
class ProposalImage extends Asset

class ProposalVideo extends Asset

class ProposalAvatar extends Asset


# base proposal class
class Proposal extends Model

    @export: 'private'
    @events: ['PROPOSAL_ASSET_ATTACHED']

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
        goals: Array()
        tiers: Array()

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

            return @get (proposal) =>
                fields = [{
                    name: 'name'
                    attributes:
                        value: proposal['name']
                        type: 'text'
                        id: 'proposal-edit-input-name'
                        'data-validation': 'alpha'
                    }]

                areas = []
                for k, v of @constructor::model
                    continue if k not in ['summary', 'pitch', 'tech', 'keywords']
                    area = {}
                    area.name = k
                    area.content = proposal[k] or ''
                    area.attributes =
                        'data-validation': 'text'
                        id: 'proposal-edit-input-'+k
                        value: k
                        style: 'width: 90%;margin: 10px auto'

                    areas.push(area)

                df = _.create_doc_frag(ProjectEditModal(fields: fields, areas: areas, kind: 'proposal'))
                adf = _.create_doc_frag(_.create_element_string('a',
                    id: 'a-proposal-editor'
                    style: 'display: none'
                , ''))
                document.body.appendChild(df)
                document.body.appendChild(adf)
                editor = _('#proposal-editor')
                trigger = _('#a-proposal-editor')

                return $.apptools.widgets.modal.create(editor, trigger, (m) =>
                    savebtn = _('#proposal-save')
                    savebtn.bind('click', (_save = (e) =>
                        e.preventDefault()
                        e.stopPropagation()

                        savebtn.unbind('click')
                        return notify('warn', 'saving proposal', 'Are your proposal details correct?', {
                                no: =>
                                    notify('notify', 'no changes made', 'keep working :)')
                                    savebtn.bind('click', _save)
                                    return

                                yes: =>
                                    pjct = {}
                                    editor = _('#proposal-editor-modal-dialog')
                                    inputs = _.to_array(editor.find('input')) or []
                                    texts = _.to_array(editor.find('textarea')) or []
                                    fields = _.join(inputs, texts)
                                    for field in fields
                                        continue if not field.hasAttribute('id')
                                        prop = field.getAttribute('id').split('-').pop()
                                        pjct[prop] = field.val()

                                    @from_message(pjct)

                                    return $.apptools.api.proposal.put(@to_message()).fulfill
                                        success: (response) =>
                                            notify('yay', 'proposal saved!', 'proposal saved successfully, click below to refresh & see updates :)', {ok: -> window.location.reload()})
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

                    if (editorform = _('#proposal-editor-form'))?
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

                $.apptools.events.trigger 'PROPOSAL_ASSET_ATTACHED', obj, @
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

            $.apptools.api.proposal.get(key: @key).fulfill
                success: (response) =>
                    return if callback? then callback?(@from_message(response)) else @from_message(response)

                failure: (error) =>
                    return notify('error','whoops', 'something went wrong :( refresh?', {ok: -> window.location.reload()})

        @put = (callback) =>

            return $.apptools.api.proposal.put(@to_message()).fulfill
                success: (response) =>
                    return if callback? then callback?(@from_message(response)) else @from_message(response)

                failure: (error) =>
                    return notify('error','whoops', 'something went wrong :( refresh?', {ok: -> window.location.reload()})


# proposal controller
class ProposalController extends OpenfireController

    @mount = 'proposal'
    @events = [
        'PROPOSAL_CONTROLLER_READY',
        'PROPOSAL_CONTROLLER_INIT',
        'PROPOSAL_AVATAR_ADDED',
        'PROPOSAL_IMAGE_ADDED',
        'PROPOSAL_VIDEO_ADDED',
        'PROPOSAL_BACKED',
        'PROPOSAL_EDITED',
        'PROPOSAL_FOLLOWED',
        'PROPOSAL_READY',                # @get()
        'PROPOSAL_SHARED',
        'PROPOSAL_UPDATED',
    ]

    method_proxies: ['attach', 'get_attached', 'from_message', 'to_message']

    constructor: (openfire) ->

        @_state = _.extend(true, {}, window._cp)

        if /proposal/.test(window.location.href)
            @proposal = new Proposal(@_state.ke)
            @proposal.get()

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

            process_goal: (goal, w) =>

                ctx = _.extend({type: 'goal', kind: 'proposal', which: w}, goal)
                ctx.index = if goal.key? then @get_attached('goal', goal.key, true) else (ctx.new = true; 'new')

                btnctx =
                    attributes:
                        'data-index': ctx.index

                if !!ctx.new
                    axn = 'propose'
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

                ctx = _.extend({type: 'tier', kind: 'proposal'}, tier)
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
                base = 'proposal-image-drop-'

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
                , 'Would you like to attach' + filename_edit + 'to your proposal?')

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
                    href: '#proposal-image-drop-choice'
                    style: 'display: none;'
                )

                return [pre_modal, trigger]

            prep_goals_modal_html: (goals, which) =>

                @internal.cleanup('proposal-goal-editor')

                _goals = []

                blank_goal = new Goal
                    which: which
                    proposal: @proposal.key
                    amount: 0
                    description: 'Fill this out to propose a new goal!'
                    funding_day_limit: 30
                    deliverable_description: 'Describe your proposed goal\'s deliberable'
                    deliverable_date: '12/31/2013'

                _goals.push(@internal.process_goal(blank_goal))
                _goals.push(@internal.process_goal(g, which)) for g in goals

                pre_modal = window.TierEditModal(false,
                    tiers: _goals
                    type: 'goal'
                )

                trigger = _.create_element_string('a',
                    id: 'a-proposal-goal-editor'
                    style: 'display: none;')

                return [pre_modal, trigger]

            prep_tiers_modal_html: (tiers) =>

                @internal.cleanup('proposal-tier-editor')

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
                    id: 'a-proposal-tier-editor',
                    style: 'display: none;')

                return [pre_modal, trigger]


        @add_media = (file_or_url) =>

            ## attach a media item to a proposal
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
                        return document.getElementById('proposal-image-drop-choice')
                    )(), (() =>
                        # trigger (not used here but required for create())
                        docfrag = _.create_doc_frag(modal_parts[1])
                        document.body.appendChild(docfrag)
                        return document.getElementById('a-proposal-image-drop-choice')
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
                        return _.get('proposal-image-drop-preview').setAttribute('src', e.target.result)

                    # simple check for allowed filetypes
                    if /^image\/(png|jpeg|gif)$/gi.test(filetype)

                        # kick off preview
                        reader.readAsDataURL(file)

                        # upload as image
                        _.get('proposal-image-drop-image').addEventListener('click', (e) =>

                            if e.preventDefault
                                e.preventDefault()
                                e.stopPropagation()

                            (btn = e.target).innerHTML = 'Great!<br>Uploading...'
                            fn_el = document.getElementById('proposal-image-drop-filename')
                            filename = fn_el.innerText

                            @log('Uploading dropped file as: ', [filename, file_ext].join('.'))

                            callback = (res) =>
                                # post-upload callback
                                @log('Image upload successful! Attaching image to proposal...')
                                @attach new ProposalImage(res[0]), () =>
                                    $.apptools.events.trigger 'PROPOSAL_IMAGE_ADDED', @
                                    btn.style.backgroundColor = '#bada55'
                                    btn.innerHTML = 'Awesome!<br>Good to go.'

                                    return @proposal

                            $.apptools.api.media.attach_image(
                                target: @proposal.key
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
                        _.get('proposal-image-drop-avatar').addEventListener('click', (e) =>

                            if e.preventDefault
                                e.preventDefault()
                                e.stopPropagation()

                            (btn = e.target).innerHTML = 'Great!<br>Uploading...'
                            fn_el = document.getElementById('proposal-image-drop-filename')
                            filename = fn_el.innerText

                            callback = (res) =>
                                @log('Avatar upload successful! Attaching avatar to proposal...')
                                @attach new ProposalAvatar(res[0]), () =>
                                    $.apptools.events.trigger 'PROPOSAL_AVATAR_ADDED', @
                                    btn.style.backgroundColor = '#bada55'
                                    btn.innerHTML = 'Awesome!<br>Good to go.'

                                    return @proposal

                            $.apptools.api.media.attach_avatar(
                                target: @proposal.key
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
                        _.get('proposal-image-drop-no').addEventListener('click', (e) =>

                            if e.preventDefault
                                e.preventDefault()
                                e.stopPropagation()

                            return $.apptools.widgets.modal.get('proposal-image-drop-choice').close()

                        , false)

                        return

                    else throw new MediaError(@constructor.name, 'Tried to upload unsupported filetype. Images must be .jpg, .png, or .gif.')

                else if file_or_url.length and file_or_url.charAt
                    # it's a URL - for now we support video
                    url = file_or_url
                    @log('Received video URL: '+url)

                    $.apptools.api.media.attach_video(
                        reference: url
                        target: @proposal.key
                    ).fulfill
                        success: (response) =>
                            @attach(new Video(response))
                            $.apptools.events.trigger 'PROPOSAL_VIDEO_ADDED', @

                        failure: (error) =>
                            alert 'attach_video() failure'

                else throw new MediaError(@constructor.name, 'Unrecognized media kind linked.')

            else throw new UserPermissionsError(@constructor.name, 'Current user is not a proposal owner.')


        @edit = () =>

            ## edit an existing proposal
            # content api?
            @log('editing functionality currently stubbed.')
            alert('You tried to edit a proposal! We\'re working on it :)')

        @update = () =>

            ## post an update to a proposal
            @log('updating functionality currently stubbed.')
            alert('You tried to update a proposal! We\'re working on it :)')

            ###
            if @_state.o
                $.apptools.api.proposal.post(target: @proposal.key).fulfill
                    success: () =>
                        # no response i think?
                        alert 'update() success'

                    failure: (error) =>
                        alert 'update() failure'

            else throw new UserPermissionsError(@constructor.name, 'Current user is not a proposal owner.')
            ###

        @back = () =>

            ## back a proposal
            # to do - figure out how to get the user, create UI for backing
            $.apptools.api.proposal.back(
                proposal: @proposal.key
                user: null
                contribution: null
            ).fulfill
                success: (response) =>
                    @log('backing functionality currently stubbed.')
                    $('#back-text').animate opacity: 0,
                        duration: 250
                        complete: () =>
                            document.getElementById('back-text')?.innerHTML = 'you rock.'
                            document.getElementById('back')?.classList.add('backed')
                            $('#back-text').animate opacity: 1,
                                duration: 250
                                complete: () =>
                                    alert 'back() success'


                failure: (error) =>
                    alert 'back() failure'

        @follow = () =>

            ## follow a proposal
            @log('following functionality currently stubbed.')
            alert('You tried to follow a proposal! We\'re working on it :)')

            ###
            $.apptools.api.proposal.follow(target: @proposal.key).fulfill

                success: (response) =>
                    document.getElementById('follow')?.classList.add('following')
                    alert 'follow() success'

                failure: (error) =>
                    alert 'follow() failure'
            ###


        @share = (sm_service) =>

            ## share a proposal via social media
            # what do?

            @log('sharing functionality currently stubbed.')
            alert('You tried to share a proposal! We\'re working on it :)')


        @get = (refresh, callback) =>

            ## get the associated proposal

            if not refresh?         # refresh=true syncs with server
                refresh = false

            else if typeof refresh isnt 'boolean'
                callback ?= refresh
                refresh = false

            if typeof callback isnt 'function'
                callback = null

            return if refresh then @proposal.get(callback) else if callback? then callback.call(@, @proposal) else @proposal

        @get_backers = () =>

            ## get proposal backers
            $.apptools.api.proposal.backers(target: @proposal.key).fulfill

                success: (response) =>
                    # response.users = []
                    alert 'get_backers() success'

                failure: (error) =>
                    alert 'get_backers() failure'


        @get_followers = () =>

            ## get proposal followers
            $.apptools.api.proposal.followers(target: @proposal.key).fulfill

                success: (response) =>
                    # response.profiles = []
                    alert 'get_followers() success'

                failure: (error) =>
                    alert 'get_followers() failure'


        @get_updates = () =>

            ## get recent updates
            $.apptools.api.proposal.posts(target: @proposal.key).fulfill

                success: (response) =>
                    # response.posts = []
                    alert 'get_updates() success'

                failure: (error) =>
                    alert 'get_updates() failure'

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
                    $.apptools.api.proposal.get_goal(
                        key: goal_key
                        proposal: @proposal.key
                    ).fulfill
                        success: (response) =>
                            goal = @attach(new Goal(target: @proposal.key).from_message(response.goal))

                            return if callback? then callback.call(@, goal) else goal

                        failure: (error) =>
                            alert 'goals.get() failure'


            list: (callback, sync) =>

                ## list goals by proposal key
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
                    $.apptools.api.proposal.get(key: @proposal.key).fulfill

                        success: (response) =>
                            goals = []
                            goals.push(@attach(new Goal(target: @proposal.key).from_message(goal))) for goal in response.goals

                            return if callback? then callback.call(@, goals) else goals

                        failure: (error) =>
                            alert 'goals.list() failure'
                            @log('Error listing goals: ' + error)

            put: (goal, callback) =>

                ## put goal by key
                $.apptools.api.proposal.put_goal(goal.to_message()).fulfill

                    success: (response) =>
                        alert 'goals.put() success'
                        return if callback? then callback.call(@, response) else response.key

                    failure: (error) =>
                        alert 'goals.put() failure'

            delete: (goal_key, callback) =>

                ## delete goal by key
                $.apptools.api.proposal.delete_goal({key: goal_key}).fulfill

                    success: (response) =>
                        alert 'goals.delete() success'
                        return if callback? then callback.call(@, response) else response.key

                    failure: (error) =>
                        alert 'goals.delete() failure'

            edit: (e) =>

                sync = true
                target = e.target
                which = target.getAttribute('id').split('-').pop()+'_goal'

                return @goals.get(which, (goal) =>
                    goal_modal_parts = @internal.prep_goals_modal_html([goal])

                    return $.apptools.widgets.modal.create (() =>
                        docfrag = _.create_doc_frag(goal_modal_parts[0])
                        document.body.appendChild(docfrag)
                        return document.getElementById('proposal-goal-editor')
                    )(), (() =>
                        docfrag = _.create_doc_frag(goal_modal_parts[1])
                        document.body.appendChild(docfrag)
                        return document.getElementById('a-proposal-goal-editor')
                    )(), ((m) =>
                        editor = _('#'+m._state.element_id+'-modal-dialog')
                        _('#'+m._state.element_id+'-modal-title').innerHTML = 'Editing '+which.split('_').shift()+' goal...'

                        propose_button.addEventListener('click', (_propose = (e) =>
                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            idx = btn.getAttribute('data-index')

                            return notify('warn', 'proposing goal', 'ready to submit?', {

                                no: =>

                                    notify('notify', 'goal not submitted', 'take your time :)')
                                    btn.addEventListener('click', _propose, false)
                                    return

                                yes: =>

                                    description_el = _('#goal-description-'+idx)
                                    name_el = _('#goal-name-'+idx)
                                    amount_el = _('#goal-amount-'+idx) or document.createElement('input')

                                    return $.apptools.api.proposal.propose_goal(new Goal(
                                        proposal: @proposal.key
                                        description: description_el.val()
                                        amount: amount_el.val()
                                        name: name_el.val()
                                        deliverable_date: +Date()
                                        deliverable_description: 'your deliverable from this goal'
                                    ).to_message).fulfill
                                        success: (response) =>
                                            notify('yay', 'goal proposed', 'we got your submission. you\'ll hear back soon!', {ok: -> m.close})
                                            btn.addEventListener('click', _propose, false)
                                            return

                                        failure: (error) =>
                                            notify('error', 'whoops', 'couldn\'t propose goal, sorry :(. try again, or hit OK to refresh', {ok: -> window.location.reload()})

                                            btn.bind('click', _propose)
                                            return false
                                })

                        ), false) for propose_button in editor.find('.propose')

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

                                    return $.apptools.api.proposal.put_goal(_.extend((if idx isnt 'new' then @get_attached('goal', idx) else new Goal()),

                                        target: @proposal.key
                                        amount: parseInt(amount_el.val())
                                        description: _('#goal-description-'+idx).val()
                                        name: _('#goal-name-'+idx).val()

                                    ).to_message()).fulfill

                                        success: (response) =>

                                            notify('yay', 'goal saved', 'updating info...')

                                            return @attach(new Goal().from_message(response), (goal) =>

                                                k = goal.key

                                                _('#a-'+k).innerHTML = goal.name + ' - ' + _.currency(goal.amount)
                                                _('#'+k).innerHTML = '<p>'+goal.description+'</p>'

                                                amount_el.val goal.amount
                                                name_el.val goal.name
                                                description_el.val goal.description

                                                btn.innerHTML = 'save goal'
                                                btn.bind('click', _save)

                                                return goal

                                            )

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
                    return $.apptools.api.proposal.get_tier(key: t_key).fulfill
                        success: (response) =>
                            tier = @attach(new Tier().from_message(response))
                            return if callback? then callback.call(@, tier) else tier

                        failure: (error) =>
                            notify('error', 'whoops', 'couldn\'t get proposal tiers from server. refresh page?', {ok: -> window.location.reload()})

            ## get all proposal tiers
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
                    return $.apptools.api.proposal.get(key: @proposal.key).fulfill
                        success: (response) =>
                            tiers = []
                            tiers.push(@attach(new Tier().from_message(tier))) for tier in response.tiers

                            return if callback? then callback.call(@, tiers) else tiers

                        failure: (error) =>
                            notify('error', 'whoops', 'couldn\'t get proposal tiers from server. refresh page?', {ok: -> window.location.reload()})

            ## put tier by key
            put: (tier, callback) =>

                return $.apptools.api.proposal.put_tier(tier.to_message()).fulfill
                    success: (response) =>
                        notify('yay', 'tier saved', ':)')
                        return if callback? then callback.call(@, response) else response.key

                    failure: (error) =>
                        notify('error', 'whoops', 'couldn\'t save tier. refresh page?', {ok: -> window.location.reload()})

            ## delete tier by key
            delete: (tier_key, callback) =>

                return $.apptools.api.proposal.delete_tier({key: tier_key}).fulfill
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

                    _t.target = @proposal.key for _t in tiers

                    tier_modal_parts = @internal.prep_tiers_modal_html(tiers)

                    return $.apptools.widgets.modal.create (() =>
                        docfrag = _.create_doc_frag(tier_modal_parts[0])
                        document.body.appendChild(docfrag)
                        return document.getElementById('proposal-tier-editor')
                    )(), (() =>
                        docfrag = _.create_doc_frag(tier_modal_parts[1])
                        document.body.appendChild(docfrag)
                        return document.getElementById('a-proposal-tier-editor')
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

                                    return $.apptools.api.proposal.put_tier(_.extend((if idx isnt 'new' then @get_attached('tier', idx) else new Tier()),

                                        target: @proposal.key
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

                                    return $.apptools.api.proposal.delete_tier(key: tier.key).fulfill
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

                                    return $.apptools.api.proposal.get_tier(key: tier.key).fulfill

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

                            return notify('warn', 'add tier', 'ready to add tier to proposal?', {

                                no: =>

                                    notify('notify', 'tier not added', 'keep on working :)')
                                    btn.addEventListener('click', _add)
                                    return

                                yes: =>

                                    return $.apptools.api.proposal.put_tier(new Tier(

                                        target: @proposal.key
                                        amount: parseInt(amount_el.val())
                                        description: description_el.val()
                                        name: name_el.val()

                                    ).to_message()).fulfill
                                        success: (response) =>
                                            notify('yay', 'tier added', 'hooray :)')

                                            return @attach new Tier(target: @proposal.key).from_message(response), (_tier) =>
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

                                                return @proposal.put()


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

        @bbq_promote = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.proposal.promote(key: @proposal.key).fulfill
                success: () ->
                    return notify("yay", "Proposal Promoted", "This proposal has been promoted to a proposal. Click to refresh", {ok: -> window.location.reload()})
                failure: (response) ->
                    return notify('error', 'an error occurred', response.error+". Click to refresh", {ok: -> window.location.reload()})

        @bbq_reject = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.proposal.reject(key: @proposal.key).fulfill
                success: () ->
                    return notify("error", "Proposal rejected", "This proposal has been rejected. Click to refresh", {ok: -> window.location.reload()})
                failure: (response) ->
                    return notify('error', 'an error occurred', response.error+". Click to refresh", {ok: -> window.location.reload()})

        @submit = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.proposal.submit(key: @proposal.key).fulfill
                success: () ->
                    return notify("yay", "Proposal Submitted", "This proposal has been submitted for approval. Click to refresh", {ok: -> window.location.reload()})
                failure: (response) ->
                    return notify('error', 'an error occurred', response.error+". Click to refresh", {ok: -> window.location.reload()})

        @reopen = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.proposal.reopen(key: @proposal.key).fulfill
                success: () ->
                    return notify("notify", "Proposal Reopened", "This proposal has been reopened for editing and is not longer waiting for approval. Click to refresh", {ok: -> window.location.reload()})
                failure: (response) ->
                    return notify('error', 'an error occurred', response.error+". Click to refresh", {ok: -> window.location.reload()})

        @suspend = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.proposal.suspend(key: @proposal.key).fulfill
                success: () ->
                    return notify("yay", "Proposal suspended", "This proposal has been suspended. It may only be re-opened by an admin. Click to refresh", {ok: -> window.location.reload()})
                failure: (response) ->
                    return notify('error', 'an error occurred', response.error+". Click to refresh", {ok: -> window.location.reload()})

        @review= (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            $.apptools.api.proposal.review(key: @proposal.key).fulfill
                success: () ->
                    return notify("yay", "Proposal returned", "This proposal has been returned for further review. Click to refresh", {ok: -> window.location.reload()})
                failure: (response) ->
                    return notify('error', 'an error occurred', response.error+". Click to refresh", {ok: -> window.location.reload()})

        @add_viewers = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            return notify('notify', "Coming soon.", ':)')

        @add_team_member = (e) =>
            if e.preventDefault
                e.preventDefault()
                e.stopPropagation()
            return notify('notify', "Coming soon.", ':)')

        @_init = () =>

            if window._cp

                # setup proposal method proxies
                ((m) =>
                    @[m] = () => return @proposal[m].apply(@proposal, arguments)
                )(method) for method in @constructor::method_proxies

                # event listeners
                #document.getElementById('share').addEventListener('click', @share, false)

                if @_state.o and /proposal/.test(window.location.href)
                    document.body.addEventListener('drop', @add_media, false)

                    # BBQ Actions
                    document.getElementById('bbq-promote')?.addEventListener('click', @bbq_promote, false)
                    document.getElementById('bbq-reject')?.addEventListener('click', @bbq_reject, false)
                    document.getElementById('bbq-suspend')?.addEventListener('click', @suspend, false)
                    document.getElementById('bbq-review')?.addEventListener('click', @review, false)

                    # Proposal Owner Actions
                    #document.getElementById('promote-goal').addEventListener('click', @active_goal.edit, false)
                    document.getElementById('promote-proposal-deets')?.addEventListener('click', @proposal.edit, false)
                    document.getElementById('promote-tiers')?.addEventListener('click', @tiers.edit, false)
                    document.getElementById('promote-submit')?.addEventListener('click', @submit, false)
                    document.getElementById('promote-reopen')?.addEventListener('click', @reopen, false)
                    document.getElementById('promote-add-viewers')?.addEventListener('click', @add_viewers, false)
                    document.getElementById('promote-add-team-member')?.addEventListener('click', @add_team_member, false)

                    # Proposal Owner Actions

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

            window.__pr = new Proposal('my-test-proposal-key')
            return @get()




if @__openfire_preinit?
    @__openfire_preinit.abstract_base_objects.push(Asset)
    @__openfire_preinit.abstract_base_objects.push(ProposalImage)
    @__openfire_preinit.abstract_base_objects.push(ProposalVideo)
    @__openfire_preinit.abstract_base_objects.push(ProposalAvatar)
    @__openfire_preinit.abstract_base_classes.push(Proposal)
    @__openfire_preinit.abstract_base_controllers.push(ProposalController)
