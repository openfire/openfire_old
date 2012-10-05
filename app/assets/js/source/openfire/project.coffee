## openfire project classes & controllers

# project media
class ProjectImage extends Asset

class ProjectVideo extends Asset

class ProjectAvatar extends Asset


# project object classes

class Goal extends Model

    model:
        key: String()
        target: String()
        contribution_type: String()
        amount: Number()
        description: String()
        backer_count: Number()
        progress: Number()
        met: Boolean()


class Tier extends Model

    model:
        key: String()
        target: String()
        name: String()
        contribution_type: String()
        amount: Number()
        description: String()
        delivery: String()
        backer_count: Number()
        backer_limit: Number()


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
        goals: Array()
        tiers: Array()

    constructor: () ->

        super

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

            @log('Pulling most updated project version from server...')
            $.apptools.api.project.get(key: @key).fulfill
                success: (response) =>
                    @log('Project successfully synced.')
                    return if callback? then callback?(@from_message(response)) else @from_message(response)

                failure: (error) =>
                    @log('Error syncing project: '+error)
                    alert 'project get() failure'



# base proposal object
class Proposal extends Model

    model: null

    constructor: (@key) ->
        return @


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

        @project = new Project(@_state.ke)
        @project_key = @project.key

        @log = (message) => return @constructor::log(@constructor.name, message)

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

                template = window.GoalEditor ||= new Template('{{+TierEditModal}}', true, 'GoalEditor')
                ctx = _.extend({type: 'goal'}, goal)
                ctx.index = if goal.key? then @get_attached('goal', goal.key, true) else (ctx.new = true; 'new')

                btnctx =
                    attributes:
                        'data-index': '{{=index}}'

                if !!ctx.new
                    axns = ['add']
                else
                    axns = ['save', 'reset', 'delete']

                ctx.buttons = [(_.extend(true, btnctx,
                    attributes:
                        'data-action': axn
                        class: '{{=type}}-button '+axn
                    content: axn + ' {{=type]}}'
                )) for axn in axns]

                return template(ctx)

            process_tier: (tier) =>

                template = window.TierEditor ||= new Template('{{+TierEditModal}}', true, 'TierEditor')
                ctx = _.extend({type: 'tier'}, tier)
                ctx.index = if tier.key? then @get_attached('tier', tier.key, true) else (ctx.new = true; 'new')

                btnctx =
                    attributes:
                        'data-index': '{{=index}}'

                if !!ctx.new
                    axns = ['add']
                else
                    axns = ['save', 'reset', 'delete']

                ctx.buttons = [(_.extend(true, btnctx,
                    attributes:
                        'data-action': axn
                        class: '{{=type}}-button '+axn
                    content: axn + ' {{=type]}}'
                )) for axn in axns]

                return template(ctx)

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

                pre_modal = _.create_element_string('div',
                    id: 'project-goal-editor'
                    class: 'pre-modal'
                    style: 'opacity: 0;'
                    'data-title': 'editing project goals...'
                , _goals.join(''))

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

                pre_modal = _.create_element_string('div',
                    id: 'project-tier-editor'
                    class: 'pre-modal'
                    style: 'opacity: 0;'
                    'data-title': 'editing project tiers...'
                , _tiers.join(''))

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
                        return _.get('project-image-drop-preview').setAttribute('src', e.target.result)

                    # simple check for allowed filetypes
                    if /^image\/(png|jpeg|gif)$/gi.test(filetype)

                        # kick off preview
                        reader.readAsDataURL(file)

                        # upload as image
                        _.get('project-image-drop-image').addEventListener('click', (e) =>

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
                                target: @project_key
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
                        _.get('project-image-drop-avatar').addEventListener('click', (e) =>

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
                                target: @project_key
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
                        _.get('project-image-drop-no').addEventListener('click', (e) =>

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
                        target: @project_key
                    ).fulfill
                        success: (response) =>
                            @attach(new Video(response))
                            $.apptools.events.trigger 'PROJECT_VIDEO_ADDED', @

                        failure: (error) =>
                            alert 'attach_video() failure'

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
                $.apptools.api.project.post(target: @project_key).fulfill
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
            document.getElementById("back-project-cc-type-display").innerHTML = type
            return false

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
                project: @project_key
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
                    alert("Success! " + response.message)
                    document.getElementById('back-text').innerHTML = 'you rock.'
                    document.getElementById('back').classList.add('backed')
                failure: (error, status, xhr) =>
                    msg = JSON.parse(xhr.responseText)?.response?.content?.error_message
                    alert("Failure! " + msg)


        @back = () =>

            # Get any existing money sources for this user and populate them in the dialog, then open it.
            $.apptools.api.payment.money_sources().fulfill
                success: (response) =>
                    selector = document.getElementById("back-project-money-source-input")
                    options = selector.innerHTML
                    if response.sources and response.sources.length
                        for source in response.sources
                            options += "<option value='" + source.key + "'>" + source.description + "</option>"
                    selector.innerHTML = options
                    $.apptools.widgets.modal.get("back-project-dialog").open()
                failure: (error) =>
                    alert("Failed to start donation. Are you logged in?")
            return


        @follow = () =>

            ## follow a project
            @log('following functionality currently stubbed.')
            alert('You tried to follow a project! We\'re working on it :)')

            ###
            $.apptools.api.project.follow(target: @project_key).fulfill

                success: (response) =>
                    document.getElementById('follow').classList.add('following')
                    alert 'follow() success'

                failure: (error) =>
                    alert 'follow() failure'
            ###


        @share = (sm_service) =>

            ## share a project via social media
            # what do?

            @log('sharing functionality currently stubbed.')
            alert('You tried to share a project! We\'re working on it :)')


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
            $.apptools.api.project.backers(target: @project_key).fulfill

                success: (response) =>
                    # response.users = []
                    alert 'get_backers() success'

                failure: (error) =>
                    alert 'get_backers() failure'


        @get_followers = () =>

            ## get project followers
            $.apptools.api.project.followers(target: @project_key).fulfill

                success: (response) =>
                    # response.profiles = []
                    alert 'get_followers() success'

                failure: (error) =>
                    alert 'get_followers() failure'


        @get_updates = () =>

            ## get recent updates
            $.apptools.api.project.posts(target: @project_key).fulfill

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
                    $.apptools.api.project.get_goal(
                        key: goal_key
                        project: @project_key
                    ).fulfill
                        success: (response) =>
                            goal = @attach(new Goal(target: @project_key).from_message(response.goal))

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
                    $.apptools.api.project.list_goals(project: @project_key).fulfill

                        success: (response) =>
                            goals = []
                            goals.push(@attach(new Goal(target: @project_key).from_message(goal))) for goal in response.goals

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

            edit: (e) =>

                if (trigger = e.target)?
                    trigger.classList.add('init') if (sync = not _.has_class(trigger, 'init'))

                else if typeof e is 'boolean'
                    sync = e

                else sync = false

                ## coordinates editing goal properties
                return @goals.list (goals) =>

                    _g.target = @project_key for _g in goals

                    goal_modal_parts = @internal.prep_goals_modal_html(goals)

                    return $.apptools.widgets.modal.create (() =>
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
                            @log('Goal save() click handler triggered. Saving...')

                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            btn.innerHTML = 'Saving...'
                            idx = btn.getAttribute('data-index')

                            goal = if idx isnt 'new' then @get_attached('goal', idx) else new Goal(target: @project_key)

                            amt_edit_el = document.getElementById('goal-amount-'+idx)
                            desc_edit_el = document.getElementById('goal-description-'+idx)

                            goal.amount = parseInt(amt_edit_el.innerHTML, 10)
                            goal.description = desc_edit_el.innerHTML

                            return $.apptools.api.project.put_goal(goal.to_message()).fulfill
                                success: (response) =>
                                    @log('Goal saved! Applying changes...')

                                    return @attach goal.from_message(response), (_goal) =>
                                        k = _goal.key

                                        amt_el = document.getElementById('a-'+k)
                                        desc_el = document.getElementById(k)
                                        amt_edit_el.innerHTML = _goal.amount
                                        amt_el.innerHTML = _.currency(_goal.amount)
                                        desc_edit_el.innerHTML = _goal.description
                                        desc_el.innerHTML = '<p>'+_goal.description+'</p>'

                                        btn.style.backgroundColor = '#bada55'
                                        btn.innerHTML = 'Goal saved!'

                                        setTimeout(() =>
                                            btn.style.backgroundColor = 'transparent'
                                            btn.innerHTML = 'Save goal'
                                            btn.addEventListener('click', _save, false)
                                        , 500)

                                        return _goal


                                failure: (error) =>
                                    @log('Sorry, something went wrong :( Try again?')
                                    @log(error)

                                    btn.style.backgroundColor = '#ff9e9e'
                                    btn.innerHTML = ':( Try again?'
                                    return btn.addEventListener('click', _save, false)

                        ), false) for save_button in _.get('save', editor)

                        delete_button.addEventListener('click', (_delete = (e) =>
                            @log('Goal delete() click handler triggered. Confirming goal delete...')

                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            btn.innerHTML = 'Really?'
                            idx = btn.getAttribute('data-index')

                            goal = @get_attached('goal', idx)
                            goal_editing_el = document.getElementById('goal-editing-'+idx)
                            goal_el = document.getElementById(goal.key)
                            goal_trigger = document.getElementById('a-'+goal.key)

                            if confirm('Really delete '+goal.amount+' goal?')
                                @log('Goal delete() confirmed. Deleting goal...')

                                return $.apptools.api.project.delete_goal(key: goal.key).fulfill
                                    success: (response) =>
                                        @log('Goal deleted! Applying changes...')

                                        btn.style.backgroundColor = '#bada55'
                                        btn.innerHTML = 'Goal deleted!'

                                        setTimeout(() =>
                                            goal_editing_el.style.opacity = 0
                                            setTimeout(() =>
                                                goal_editing_el.parentNode.removeChild(goal_editing_el)
                                                goal_el.parentNode.removeChild(goal_el)
                                                goal_trigger.parentNode.removeChild(goal_trigger)
                                            , 500)
                                        , 1000)

                                        return

                                    failure: (error) =>
                                        @log('Sorry, something went wrong :( Try again?')
                                        @log(error)

                                        btn.style.backgroundColor = '#ff9e9e'
                                        btn.innerHTML = ':( Try again?'

                                        return btn.addEventListener('click', _delete, false)

                            else
                                @log('Goal delete() canceled by user.')

                                btn.innerHTML = 'Delete goal'
                                return btn.addEventListener('click', _delete, false)

                        ), false) for delete_button in _.get('delete', editor)

                        reset_button.addEventListener('click', (_reset = (e) =>
                            @log('Goal reset() click handler triggered. Confirming goal reset...')

                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            btn.innerHTML = 'Really?'
                            idx = btn.getAttribute('data-index')

                            goal = @get_attached('goal', idx)

                            if confirm('Really discard your changes and reset goal to saved version?')
                                @log('Goal reset() confirmed. Resetting goal to saved values...')

                                return $.apptools.api.project.get_goal(key: goal.key).fulfill
                                    success: (response) =>
                                        @log('Goal reset! Applying changes')

                                        btn.style.backgroundColor = '#bada55'
                                        btn.innerHTML = 'Goal reset!'

                                        return @attach goal.from_message(response), (_goal) =>
                                            document.getElementById('goal-amount-'+idx).innerHTML = _goal.amount
                                            document.getElementById('goal-description-'+idx).innerHTML = _goal.description

                                            setTimeout(() =>
                                                btn.style.backgroundColor = 'transparent'
                                                btn.innerHTML = 'Reset goal'
                                                return btn.addEventListener('click', _reset, false)
                                            , 500)

                                            return _goal


                                    failure: (error) =>
                                        @log('Sorry, something went wrong :( Try again?')
                                        @log(error)

                                        btn.style.backgroundColor = '#ff9e9e'
                                        btn.innerHTML = ':( Try again?'
                                        return btn.addEventListener('click', _reset, false)

                            else
                                @log('Goal reset() canceled by user.')

                                btn.innerHTML = 'Reset goal'
                                return btn.addEventListener('click', _reset, false)

                        ), false) for reset_button in _.get('reset', editor)

                        add_button.addEventListener('click', (_add = (e) =>
                            @log('Goal add() click handler triggered. Saving...')

                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            btn.innerHTML = 'Adding...'
                            idx = 'new'

                            goal = new Goal(target: @project_key)

                            amt_edit_el = document.getElementById('goal-amount-'+idx)
                            desc_edit_el = document.getElementById('goal-description-'+idx)
                            new_edit_el = amt_edit_el.parentNode

                            goal.amount = parseInt(amt_edit_el.innerHTML, 10)
                            goal.description = desc_edit_el.innerText

                            return $.apptools.api.project.put_goal(goal.to_message()).fulfill
                                success: (response) =>
                                    @log('Goal added! Applying changes...')

                                    return @attach goal.from_message(response), (_goal) =>
                                        k = _goal.key
                                        index = @get_attached('goal', k, true)

                                        df = _.create_doc_frag(@internal.process_goal(_goal))
                                        new_edit_el.parentNode.insertBefore(df, new_edit_el.nextSibling)

                                        amt_edit_el.innerHTML = 0
                                        desc_edit_el.innerHTML = 'Fill this out to add a goal!'

                                        btn.innerHTML = 'Add goal'
                                        btn.addEventListener('click', _add, false)

                                        added = document.getElementById('goal-editing-'+index)

                                        sv_btn.addEventListener('click', _save, false) for sv_btn in _.get('save', added)
                                        rst_btn.addEventListener('click', _reset, false) for rst_btn in _.get('reset', added)
                                        del_btn.addEventListener('click', _delete, false) for del_btn in _.get('delete', added)

                                        btn.style.backgroundColor = '#bada55'
                                        btn.innerHTML = 'Goal added!'
                                        return () =>
                                            btn.addEventListener('click', _add, false)

                                failure: (error) =>
                                    @log('Sorry, something went wrong :( Try again?')
                                    @log(error)

                                    btn.style.backgroundColor = '#ff9e9e'
                                    btn.innerHTML = ':( Try again?'
                                    return btn.addEventListener('click', _add, false)

                        ), false) for add_button in _.get('add', editor)

                        set_focus = (g_f) =>
                            g_f.addEventListener('click', (_focus = (e) =>
                                e.preventDefault()
                                e.stopPropagation()
                                field = e.target
                                field.innerHTML = ''
                                return field.focus()
                            ), false)

                        set_focus(goal_field) for goal_field in _.get('goal-field', editor)

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

                , sync


        @tiers =

            get: (tier_key, callback, sync) =>

                ## get tier by key

                if not sync?
                    if callback? and typeof callback is 'boolean'
                        sync = callback
                        callback = null
                    else sync is false

                if not sync
                    tier = @get_attached('tier', tier_key)
                    return if callback? then callback.call(@, tier) else tier

                else
                    # get from the server
                    $.apptools.api.project.get_tier(
                        key: tier_key
                        project: @project_key
                    ).fulfill
                        success: (response) =>
                            tier = @attach(new Tier(target: @project_key).from_message(response.tier))
                            return if callback? then callback.call(@, tier) else tier

                        failure: (error) =>
                            alert 'tiers.get() failure'

            list: (callback, sync) =>

                ## list tiers by project key

                if not sync?
                    if callback? and typeof callback is 'boolean'
                        sync = callback
                        callback = null
                    else sync is false

                if not sync
                    tiers = @get_attached('tier', true)
                    return if callback? then callback.call(@, tiers) else tiers

                else
                    # get from the server
                    $.apptools.api.project.list_tiers(project: @project_key).fulfill
                        success: (response) =>
                            tiers = []
                            tiers.push(@attach(new Goal(target: @project_key).from_message(tier))) for tier in response.tiers

                            return if callback? then callback.call(@, tiers) else tiers

                        failure: (error) =>
                            alert 'tiers.list() failure'
                            @log('Error listing tiers: ' + error)

            put: (tier, callback) =>

                ## put tier by key

                $.apptools.api.project.put_tier(tier.to_message()).fulfill
                    success: (response) =>
                        alert 'tiers.put() success'
                        return if callback? then callback.call(@, response) else response.key

                    failure: (error) =>
                        alert 'tiers.put() failure'

            delete: (tier_key, callback) =>

                ## delete tier by key

                $.apptools.api.project.delete_tier({key: tier_key}).fulfill
                    success: (response) =>
                        alert 'tiers.delete() success'
                        return if callback? then callback.call(@, response) else response.key

                    failure: (error) =>
                        alert 'tiers.delete() failure'

            edit: (e) =>

                ## coordinates editing tier properties

                if (trigger = e.target)?
                    trigger.classList.add('init') if (sync = not _.has_class(trigger, 'init'))

                else if typeof e is 'boolean'
                    sync = e

                else sync = false

                return @tiers.list (tiers) =>

                    _t.target = @project_key for _t in tiers

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
                        editor = document.getElementById(m._state.element_id)

                        save_button.addEventListener('click', (_save = (e) =>
                            @log('Tier save() click handler triggered. Saving...')

                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            btn.innerHTML = 'Saving...'
                            idx = btn.getAttribute('data-index')

                            tier = if idx isnt 'new' then @get_attached('tier', idx) else new Tier(target: @project_key)

                            amt_edit_el = document.getElementById('tier-amount-'+idx)
                            desc_edit_el = document.getElementById('tier-description-'+idx)
                            name_edit_el = document.getElementById('tier-name-'+idx)

                            tier.amount = parseInt(amt_edit_el.innerHTML, 10)
                            tier.description = desc_edit_el.innerText
                            tier.name = name_edit_el.innerText

                            return $.apptools.api.project.put_tier(tier.to_message()).fulfill
                                success: (response) =>
                                    @log('Tier saved! Applying changes...')

                                    return @attach tier.from_message(response), (_tier) =>
                                        k = _tier.key

                                        name_and_amt_el = document.getElementById('a-'+k)

                                        name_edit_el.innerHTML = _tier.name
                                        amt_edit_el.innerHTML = _tier.amount

                                        name_and_amt_el.innerHTML = _tier.name + ' - ' + _.currency(_tier.amount)

                                        desc_el = document.getElementById(k)
                                        desc_edit_el.innerHTML = _tier.description
                                        desc_el.innerHTML = '<p>'+_tier.description+'</p>'

                                        btn.style.backgroundColor = '#bada55'
                                        btn.innerHTML = 'Tier saved!'

                                        setTimeout(() =>
                                            btn.style.backgroundColor = 'transparent'
                                            btn.innerHTML = 'Save tier'
                                            btn.addEventListener('click', _save, false)
                                        , 500)

                                        return _tier

                                failure: (error) =>
                                    @log('Sorry, something went wrong :( Try again?')
                                    @log(error)

                                    btn.style.backgroundColor = '#ff9e9e'
                                    btn.innerHTML = ':( Try again?'
                                    return btn.addEventListener('click', _save, false)

                        ), false) for save_button in _.get('save', editor)

                        delete_button.addEventListener('click', (_delete = (e) =>
                            @log('Tier delete() click handler triggered. Confirming tier delete...')

                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            btn.innerHTML = 'Really?'
                            idx = btn.getAttribute('data-index')

                            tier = @get_attached('tier', idx)
                            tier_editing_el = document.getElementById('tier-editing-'+idx)
                            tier_el = document.getElementById(tier.key)
                            tier_trigger = document.getElementById('a-'+tier.key)

                            if confirm('Really delete '+tier.amount+' tier?')
                                @log('Tier delete() confirmed. Deleting tier...')

                                return $.apptools.api.project.delete_tier(key: tier.key).fulfill
                                    success: (response) =>
                                        @log('Tier deleted! Applying changes...')

                                        btn.style.backgroundColor = '#bada55'
                                        btn.innerHTML = 'Tier deleted!'

                                        setTimeout(() =>
                                            tier_editing_el.style.opacity = 0
                                            setTimeout(() =>
                                                tier_editing_el.parentNode.removeChild(tier_editing_el)
                                                tier_el.parentNode.removeChild(tier_el)
                                                tier_trigger.parentNode.removeChild(tier_trigger)
                                            , 500)
                                        , 1000)

                                        return

                                    failure: (error) =>
                                        @log('Sorry, something went wrong :( Try again?')
                                        @log(error)

                                        btn.style.backgroundColor = '#ff9e9e'
                                        btn.innerHTML = ':( Try again?'

                                        return btn.addEventListener('click', _delete, false)

                            else
                                @log('Tier delete() canceled by user.')

                                btn.innerHTML = 'Delete tier'
                                return btn.addEventListener('click', _delete, false)

                        ), false) for delete_button in _.get('delete', editor)

                        reset_button.addEventListener('click', (_reset = (e) =>
                            @log('Tier reset() click handler triggered. Confirming tier reset...')

                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            btn.innerHTML = 'Really?'
                            idx = btn.getAttribute('data-index')

                            tier = @get_attached('tier', idx)

                            if confirm('Really discard your changes and reset tier to saved version?')
                                @log('Tier reset() confirmed. Resetting tier to saved values...')

                                return $.apptools.api.project.get_tier(key: tier.key).fulfill
                                    success: (response) =>
                                        @log('Tier reset! Applying changes')

                                        btn.style.backgroundColor = '#bada55'
                                        btn.innerHTML = 'Tier reset!'

                                        return @attach tier.from_message(response), (_goal) =>
                                            document.getElementById('tier-name-'+idx).innerHTML = _tier.name
                                            document.getElementById('tier-amount-'+idx).innerHTML = _tier.amount
                                            document.getElementById('tier-description-'+idx).innerHTML = _tier.description

                                            setTimeout(() =>
                                                btn.style.backgroundColor = 'transparent'
                                                btn.innerHTML = 'Reset tier'
                                                return btn.addEventListener('click', _reset, false)
                                            , 500)

                                            return _tier


                                    failure: (error) =>
                                        @log('Sorry, something went wrong :( Try again?')
                                        @log(error)

                                        btn.style.backgroundColor = '#ff9e9e'
                                        btn.innerHTML = ':( Try again?'
                                        return btn.addEventListener('click', _reset, false)

                            else
                                @log('Tier reset() canceled by user.')

                                btn.innerHTML = 'Reset tier'
                                return btn.addEventListener('click', _reset, false)

                        ), false) for reset_button in _.get('reset', editor)

                        add_button.addEventListener('click', (_add = (e) =>
                            @log('Tier add() click handler triggered. Saving...')

                            e.preventDefault()
                            e.stopPropagation()

                            btn = e.target
                            btn.removeEventListener('click')
                            btn.innerHTML = 'Adding...'
                            idx = 'new'

                            tier = new Tier(target: @project_key)

                            name_edit_el = document.getElementById('tier-name-'+idx)
                            amt_edit_el = document.getElementById('tier-amount-'+idx)
                            desc_edit_el = document.getElementById('tier-description-'+idx)
                            new_edit_el = amt_edit_el.parentNode

                            tier.name = name_edit_el.innerText
                            tier.amount = parseInt(amt_edit_el.innerHTML, 10)
                            tier.description = desc_edit_el.innerText

                            return $.apptools.api.project.put_tier(tier.to_message()).fulfill
                                success: (response) =>
                                    @log('Tier added! Applying changes...')

                                    return @attach tier.from_message(response), (_tier) =>
                                        k = _tier.key
                                        index = @get_attached('tier', k, true)

                                        df = _.create_doc_frag(@internal.process_tier(_tier))
                                        new_edit_el.parentNode.insertBefore(df, new_edit_el.nextSibling)

                                        name_edit_el.innerText = 'New Tier'
                                        amt_edit_el.innerHTML = 0
                                        desc_edit_el.innerHTML = 'Fill this out to add a tier!'

                                        btn.innerHTML = 'Add tier'
                                        btn.addEventListener('click', _add, false)

                                        added = document.getElementById('tier-editing-'+index)

                                        sv_btn.addEventListener('click', _save, false) for sv_btn in _.get('save', added)
                                        rst_btn.addEventListener('click', _reset, false) for rst_btn in _.get('reset', added)
                                        del_btn.addEventListener('click', _delete, false) for del_btn in _.get('delete', added)

                                        btn.style.backgroundColor = '#bada55'
                                        btn.innerHTML = 'Tier added!'
                                        return () =>
                                            btn.addEventListener('click', _add, false)

                                failure: (error) =>
                                    @log('Sorry, something went wrong :( Try again?')
                                    @log(error)

                                    btn.style.backgroundColor = '#ff9e9e'
                                    btn.innerHTML = ':( Try again?'
                                    return btn.addEventListener('click', _add, false)

                        ), false) for add_button in _.get('add', editor)

                        set_focus = (t_f) =>
                            t_f.addEventListener('click', (_focus = (e) =>
                                e.preventDefault()
                                e.stopPropagation()
                                field = e.target
                                field.innerHTML = ''
                                return field.focus()
                                ), false)

                        set_focus(tier_field) for tier_field in _.get('tier-field', editor)

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


        @_init = () =>

            if window._cp and _.get('#project')?

                # setup project method proxies
                ((m) =>
                    @[m] = () => return @project[m].apply(@project, arguments)
                )(method) for method in @constructor::method_proxies

                # event listeners
                document.getElementById('follow').addEventListener('click', @follow, false)
                document.getElementById('share').addEventListener('click', @share, false)
                document.getElementById('back').addEventListener('click', @back, false)

                # Event listeners in the back project dialog.
                document.getElementById('submit-back-project').addEventListener('click', @submit_payment, false)
                document.getElementById('cancel-back-project').addEventListener('click', @close_back_dialog, false)
                for node in document.getElementsByName('tier')
                    node.addEventListener('change', @change_backing_tier, false)
                document.getElementById('back-project-cc-num-input').onkeyup = @detect_cc_type
                for node in document.getElementsByClassName("vote-plus")
                    node.addEventListener('click', @vote_plus_clicked, false)
                for node in document.getElementsByClassName("vote-minus")
                    node.addEventListener('click', @vote_minus_clicked, false)

                if @_state.o
                    document.body.addEventListener('drop', @add_media, false)
                    document.getElementById('promote-goals').addEventListener('click', @goals.edit, false)
                    document.getElementById('promote-tiers').addEventListener('click', @tiers.edit, false)

                    document.getElementById('promote-dropzone').addEventListener('dragenter', d_on = (ev) ->
                        if ev?.preventDefault
                            ev.preventDefault()
                            ev.stopPropagation()

                        ev.target.classList.add('hover')
                    , false)
                    document.getElementById('promote-dropzone').addEventListener('dragover', d_on, false)
                    document.getElementById('promote-dropzone').addEventListener('dragleave', d_off = (ev) ->
                        if ev?.preventDefault
                            ev.preventDefault()
                            ev.stopPropagation()

                        ev.target.className = 'dropzone'
                    , false)
                    document.getElementById('promote-dropzone').addEventListener('dragexit', d_off, false)
                    document.getElementById('promote-dropzone').addEventListener('drop', ((ev) =>
                        d_off(ev)
                        return @add_media(ev)
                    ), false)

            window.__pr = new Project('my-test-project-key')
            return @get()



# proposal controller
class ProposalController extends OpenfireController

    @mount = 'proposal'
    @events = []

    constructor: (openfire, window) ->

        @_init = () =>
            return


if @__openfire_preinit?
    @__openfire_preinit.abstract_base_objects.push Asset, ProjectImage, ProjectVideo, ProjectAvatar
    @__openfire_preinit.abstract_base_classes.push Project, Proposal
    @__openfire_preinit.abstract_base_controllers.push ProjectController, ProposalController
