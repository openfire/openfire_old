## openfire project classes & controllers

# project media
class ProjectImage extends Asset

class ProjectVideo extends Asset

class ProjectAvatar extends Asset

# project object classes

class Goal
    constructor: () ->
        @from_message = (message) =>
            # should eventually live on Model?
            return Util.extend(true, @, message)

        @to_message = () =>
            message = {}
            message[prop] = val for own prop, val of @
            return message

class Tier
    constructor: () ->
        @from_message = (message) =>
            # should eventually live on Model?
            return Util.extend(true, @, message)

        @to_message = () =>
            message = {}
            message[prop] = val for own prop, val of @
            return message



# base project object
class Project # extends Model

    model:
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

    constructor: (key) ->

        @key = key
        @assets =
            store:[]
            index: {}

        @goals =
            store:[]
            index: {}

        @tiers =
            store:[]
            index: {}

        @attach = (kind, obj) =>

            if obj? and kind?

                if @[kind]?
                    key = obj.key

                    if @[kind].index[key]?
                        idx = @[kind].index[key]

                        old_store = @[kind].store
                        new_store = old_store.slice(0, idx)
                        (_ns = old_store.slice(idx+1)).unshift(obj)

                        new_store.push(item) for item in _ns

                        @[kind].store = new_store

                        return obj

                    else @[kind].index[key] = @[kind].store.push(obj) - 1

                else throw 'Invalid project store specified for attach()ment'

            else throw 'Too few arguments passed to attach(): function(store_name, object_to_store){}'

        @from_message = (message, strict=false) =>

            ## updates model with RPC responses
            # should eventually live on Model API
            # can't be simple extend - must compare against 'model' property on prototype to type-validate
            # if strict isnt false, validate just discards non-model properties and returns modelsafed object
            try
                if @::validate(message, @::model, false)
                    @[prop] = val for own prop, val of message

            catch error
                console.log 'Validation error: ', error.toString()

                if not strict
                    try
                        modsafe = @::validate(message, @::model, true)
                        @[p] = v for own p, v of modsafe

                    catch err
                        console.log 'Model-safing RPC message failed: ', err.toString()

            finally
                return @

        @to_message = () =>

            ## converts model to RPC-ready object
            # needs some thought - improvements?
            message = {}
            message[prop] = val for own prop, val of @

            return message

        @get = (callback) =>

            $.apptools.api.project.get(key: @key).fulfill

                success: (response) =>
                    return if callback? then callback?(@from_message(response)) else @from_message(response)

                failure: (error) =>
                    alert 'project get() failure'

        @get_attached = (kind, key, index_only=false) =>

            if key? and @[kind]?

                if (_i = parseInt(key, 10)) > 0 or _i < 0 or _i is 0  # rule out NaN responses from parseInt
                    return @[kind].store[_i] or false

                if (idx = @[kind].index[key])?
                    return if index_only then idx else @[kind].store[idx]
                else
                    return false

            else throw 'Too few arguments passed to get_attached(): function(store_name, index){}'



# base proposal object
class Proposal # extends Model

    model: null

    constructor: (@key) ->
        return @


# project controller
class ProjectController extends OpenfireController

    @mount = 'project'
    @events = [
        'PROJECT_CONTROLLER_READY',
        'PROJECT_CONTROLLER_INIT',
        'PROJECT_MEDIA_ADDED',
        'PROJECT_AVATAR_ADDED',
        'PROJECT_BACKED',
        'PROJECT_EDITED',
        'PROJECT_FOLLOWED',
        'PROJECT_READY',                # @get()
        'PROJECT_SHARED',
        'PROJECT_UPDATED',
    ]

    constructor: (openfire) ->

        @_state = Util.extend(true, {}, window._cp)

        @project = new Project(@_state.ke)
        @project_key = @project.key

        @add_media = (file_or_url, kind) =>

            ## attach a media item to a project
            if @_state.o

                if file_or_url.preventDefault
                    # it's an event, grab the files & try again
                    file_or_url.preventDefault()
                    file_or_url.stopPropagation()

                    e = file_or_url
                    files = e.dataTransfer.files

                    return @add_media(fi, 'image') for fi in files if files?

                if file_or_url.size and file_or_url.type
                    # it's a file!
                    file = file_or_url
                    filetype = file.type
                    console.log('Received dropped ', filetype)

                    reader = new FileReader()
                    reader.file = file
                    reader.onloadend = (e) =>
                        e.preventDefault()
                        e.stopPropagation()
                        Util.get('project-image-drop-preview').setAttribute('src', e.target.result)

                    choice = $.apptools.widgets.modal.create (() =>
                        docfrag = Util.create_doc_frag (() =>
                            return Util.create_element_string('div',
                                id: 'project-image-drop-choice'
                                style: 'width: 100%;margin: 0 auto;opacity: 0;text-align: center;background-color: #eee;font-size: 9pt;'
                                class: 'pre-modal'
                                "data-title": 'Hey, you dropped your photo!'
                            ).split('*').join([
                                '',
                                Util.create_element_string('img',
                                    id: 'project-image-drop-preview'
                                    style: 'max-width: 140px;'
                                    class: 'dropshadow'
                                ),
                                '','', '<span style="font-size: 14px; font-weight: bolder;">My, that looks nice.</span>', '','','',
                                'Would you like to attach "'+file.name+'" to your project?',
                                 '','',
                                [
                                    Util.create_element_string('button',
                                        id: 'project-image-drop-avatar'
                                        class: 'rounded'
                                        value: 'avatar'
                                    ).split('*').join('yes!<br>(as an avatar)')
                                ,
                                    Util.create_element_string('button',
                                        id: 'project-image-drop-image'
                                        class: 'rounded'
                                        value: 'image'
                                    ).split('*').join('yes!<br>(as an image)')
                                ,
                                    Util.create_element_string('button',
                                        id: 'project-image-drop-no'
                                        class: 'rounded'
                                        value: 'no'
                                    ).split('*').join('oops!<br>(no thanks)')
                                ].join('')
                            ].join('<br>'))
                        )()
                        document.body.appendChild(docfrag)
                        return document.getElementById('project-image-drop-choice')
                    )(), (() =>
                        docfrag = Util.create_doc_frag (() =>
                            return Util.create_element_string 'a',
                                id: 'a-project-image-drop-choice'
                                href: '#project-image-drop-choice'
                                style: 'display: none;'
                        )()
                        document.body.appendChild(docfrag)
                        return document.getElementById('a-project-image-drop-choice')
                    )(), (m) =>
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

                    if /^image\/(png|jpeg|gif)$/gi.test(filetype)

                        reader.readAsDataURL(file)

                        Util.get('project-image-drop-image').addEventListener('click', (e) =>

                            if e.preventDefault
                                e.preventDefault()
                                e.stopPropagation()

                            (btn = e.target).innerHTML = 'Great!<br>Uploading...'

                            callback = (res) =>
                                console.log('attach_image() callback reached!')
                                console.log('callback response: ', res)

                                @project.attach(new ProjectImage(res))
                                $.apptools.events.trigger 'PROJECT_MEDIA_ADDED', @

                                btn.style.backgroundColor = '#bada55'
                                btn.innerHTML = 'Awesome!<br>Good to go.'

                                return @

                            $.apptools.api.media.attach_image(
                                target: @project_key
                                size: file.size
                                name: file.name
                            ).fulfill
                                success: (response) =>
                                    if not @uploader?
                                        uploader = $.apptools.widgets.uploader.create 'array',
                                            id: 'body'
                                            endpoints: [response.endpoint]
                                            finish: callback

                                        @uploader = uploader

                                    else
                                        uploader = @uploader.add_endpoint(response.endpoint)
                                        uploader = uploader.add_callback(callback)

                                    uploader.upload(file)

                                failure: (error) =>
                                    btn.style.backgroundColor = '#ee9099'
                                    btn.innerHTML = 'Bummer!<br> :('
                                    alert 'uploaded attach_image() failure'

                        , false)

                        Util.get('project-image-drop-avatar').addEventListener('click', (e) =>

                            if e.preventDefault
                                e.preventDefault()
                                e.stopPropagation()

                            (btn = e.target).innerHTML = 'Great!<br>Uploading...'

                            callback = (res) =>
                                console.log('attach_image() callback reached!')
                                console.log('callback response: ', res)

                                @project.attach(new ProjectAvatar(res))
                                $.apptools.events.trigger 'PROJECT_AVATAR_ADDED', @

                                btn.style.backgroundColor = '#bada55'
                                btn.innerHTML = 'Awesome!<br>Good to go.'

                            $.apptools.api.media.attach_avatar(
                                target: @project_key
                                size: file.size
                                name: file.name
                            ).fulfill
                                success: (response) =>
                                    if not @uploader?
                                        uploader = $.apptools.widgets.uploader.create 'data',
                                            id: 'body'
                                            endpoints: [response.endpoint]
                                            finish: callback

                                        @uploader = uploader

                                    else
                                        uploader = @uploader.add_endpoint(response.endpoint)
                                        uploader = uploader.add_callback(callback)

                                    uploader.upload(file)

                                failure: (error) =>
                                    btn.style.backgroundColor = '#ee9099'
                                    btn.innerHTML = 'Bummer!<br> :('
                                    alert 'uploaded attach_avatar() failure'

                        , false)

                        Util.get('project-image-drop-no').addEventListener('click', (e) =>

                            if e.preventDefault
                                e.preventDefault()
                                e.stopPropagation()

                            return $.apptools.widgets.modal.get('project-image-drop-choice').close()

                        , false)

                        return

                    else throw new MediaError(@constructor.name, 'Tried to upload unsupported filetype. Images must be .jpg, .png, or .gif.')

                else
                    # assume it's a URL
                    url = file_or_url
                    console.log('received url to attach: ', url)

                    if kind is 'image'

                        $.apptools.api.media.attach_image(

                            intake: 'url'
                            target: @project_key

                        ).fulfill

                            success: (response) =>

                                @project.attach(new Image(response.media_key, response.serve_url))
                                $.apptools.events.trigger 'PROJECT_MEDIA_ADDED', @

                            failure: (error) =>
                                alert 'url-linked attach_image() failure'

                    else if kind is 'video'

                        $.apptools.api.media.attach_video(

                            reference: url
                            target: @project_key

                        ).fulfill

                            success: (response) =>

                                @project.attach(new Video(response.media_key, response.serve_url))
                                $.apptools.events.trigger 'PROJECT_MEDIA_ADDED', @

                            failure: (error) =>
                                alert 'attach_video() failure'

                    else throw new MediaError(@constructor.name, 'Unrecognized media kind linked.')

            else throw new UserPermissionsError(@constructor.name, 'Current user is not a project owner.')


        @back = () =>

            ## back a project
            $.apptools.api.project.back(target: @project_key).fulfill

                success: (response) =>
                    $('#back-text').animate opacity: 0,
                        duration: 250
                        complete: () =>
                            document.getElementById('back-text').innerHTML = 'you rock.'
                            document.getElementById('back').classList.add('backed')
                            $('#back-text').animate opacity: 1,
                                duration: 250
                                complete: () =>
                                    alert 'back() success'


                failure: (error) =>
                    alert 'back() failure'


        @edit = () =>

            ## edit an existing project
            # content api?

        @edit_tier = () => return @tiers.edit.apply(@, arguments)
        @edit_goal = () => return @tiers.edit.apply(@, arguments)

            ## edit a project tier


        @follow = () =>

            ## follow a project
            $.apptools.api.project.follow(target: @project_key).fulfill

                success: (response) =>
                    document.getElementById('follow').classList.add('following')
                    alert 'follow() success'

                failure: (error) =>
                    alert 'follow() failure'


        @get = (refresh, callback) =>

            ## get the associated project
            # for server pull, refresh=true
            if not refresh?
                refresh = false

            else if typeof refresh isnt 'boolean'
                callback ?= refresh
                refresh = false

            if typeof callback isnt 'function'
                callback = null

            return if refresh then @project.get(callback) else if callback? then callback.call?(@, @project) else @project

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

        @goals =

            get: (goal_key, callback) =>
                ## get goal by key

                if goal_key is false
                    # just return local version
                    goal_key = callback
                    idx = @project.goals_by_key[goal_key]
                    return if idx then @project.goals[idx] else null

                else
                    # get from the server
                    $.apptools.api.project.get_goal({key: goal_key}).fulfill

                        success: (response) =>
                            goal = @project.attach('goal', new Goal().from_message(response.goal))

                            return if callback? then callback.call(@, goal) else goal

                        failure: (error) =>
                            alert 'goals.get() failure'


            list: (callback) =>

                ## list goals by project key
                $.apptools.api.project.list_goals({project: @project_key}).fulfill

                    success: (response) =>
                        goals = []
                        _at = (_g) =>
                            _goal = new Goal()
                            _goal = _goal.from_message(_g)
                            @project.attach('goals', _goal)
                            return _goal

                        goals.push(_at(goal)) for goal in response.goals

                        return if callback? then callback.call(@, goals) else goals

                    failure: (error) =>
                        alert 'goals.list() failure'
                        console.log('Error listing goals: ' + error)

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

            edit: (goal_or_key) =>

                ## coordinates editing goal properties
                base_id = 'project-goal-editor'
                base_el = null

                return @goals.list (goals) =>
                    _pk = @project_key
                    _idx = null
                    _key = null

                    $.apptools.widgets.modal.create (() =>
                        document.body.appendChild(Util.create_doc_frag(Util.create_element_string('div'
                            id: base_id
                            class: 'pre-modal'
                            style: 'opacity: 0;'
                            'data-title': 'editing project goals...'
                        , ((goal_div='') =>
                            (goal_div += Util.create_element_string('div'
                                id: 'goal-editing-'+ (() =>
                                    go = @project.attach('goals', g)
                                    _idx = @project.get_attached('goals', go.key, true)
                                    return _idx
                                )()
                                class: 'mini-editable goal'

                            , ((parts='') =>
                                parts += Util.create_element_string('h3',
                                    class: 'goal-field amount'
                                    id: 'goal-amount-' + _idx
                                    contenteditable: true
                                , g.amount)
                                parts += Util.create_element_string('p',
                                    class: 'rounded goal-field description'
                                    id: 'goal-description-' + _idx
                                    contenteditable: true
                                , (if g.description? then g.description else '<span class="shh">default description</span>'))
                                parts += Util.create_element_string('button',
                                    id: 'goal-save-' + _idx,
                                    class: 'goal-button save'
                                ,'save goal')
                                parts += Util.create_element_string('button',
                                    id: 'goal-get-' + _idx,
                                    class: 'goal-button get'
                                ,'refresh goal')
                                parts += Util.create_element_string('button',
                                    id: 'goal-delete-' + _idx,
                                    class: 'goal-button delete'
                                ,'delete goal')
                                return parts
                            )()
                            )) for g in goals
                            return goal_div
                        )())))
                        return document.getElementById(base_id)
                    )(), (() =>
                        document.body.appendChild(Util.create_doc_frag(Util.create_element_string('a'
                            id: 'a-'+base_id
                            href: '#'+base_id
                            style: 'display: none'
                        , '')))
                        return document.getElementById('a-'+base_id)
                    )(), (m) =>
                        editors = []
                        populate = (gfield) =>

                            editor = $.apptools.widgets.editor.create(gfield)

                            _idx = editor._state.element_id.split('-').pop()
                            goal = @project.get_attached('goals', _idx)
                            _key = goal.key

                            editor.save = (e) =>

                                if e? and e.preventDefault
                                    e.preventDefault()
                                    e.stopPropagation()

                                goal.target = @project_key
                                goal.amount = parseInt(document.getElementById('goal-amount-'+_idx).innerHTML)
                                goal.description = document.getElementById('goal-description-'+_idx).innerHTML

                                return false if not goal.amount? or not goal.description?

                                pane = document.getElementById(editor._state.pane_id)
                                $(pane).animate
                                    opacity: 0
                                ,
                                    duration: 200
                                    complete: () =>
                                        pane.innerHTML = '<span class="loading spinner momentron">&#xf0045;</span>'
                                        $(pane).animate
                                            opacity: 1
                                        ,
                                            duration: 200

                                $.apptools.api.project.put_goal(goal).fulfill
                                    success: (response) =>
                                        $(pane).animate
                                            opacity: 0
                                        ,
                                            duration: 200
                                            complete: () =>
                                                pane.innerHTML = '<span class="momentron">&#xf0053;</span>'
                                                pane.style.color = '#bada55'
                                                $(pane).animate
                                                    opacity: 1
                                                ,
                                                    duration: 200
                                                    complete: () =>
                                                        setTimeout(() =>
                                                            return editor.hide()
                                                        , 400)

                                        return @project.attach('goals', goal.from_message(response))

                                    failure: (error) =>
                                        $(pane).animate
                                            opacity: 0
                                        ,
                                            duration: 200
                                            complete: () =>
                                                pane.innerHTML = '<span class="momentron">&#xf0054;</span>'
                                                pane.style.color = '#f00'
                                                $(pane).animate
                                                    opacity: 1
                                                ,
                                                    duration: 200
                                                    complete: () =>
                                                        setTimeout(() =>
                                                            return editor.hide()
                                                        , 800)


                            $.apptools.widgets.editor.enable(editor)
                            _el = Util.get((_id = editor._state.element_id))
                            _idx = _id.split('-').pop()

                            document.getElementById('goal-save-'+_idx).addEventListener('click', editor.save, false)

                            (close_x = document.getElementById(base_id + '-modal-close')).removeEventListener('mousedown')
                            close_x.addEventListener('click', () =>
                                return m.close((_m) =>
                                    return $.apptools.widgets.modal.destroy(_m))
                            , false)


                            document.getElementById('goal-get-'+_idx).addEventListener('click', (e) =>

                                if e?.preventDefault
                                    e.preventDefault()
                                    e.stopPropagation()
                                    clicked = e.target
                                    _idx = clicked?.getAttribute('id').split('-').pop()
                                    goal = @project.get_attached('goals', _idx)
                                    _key = goal.key

                                return @goals.get _key, (gol) =>
                                    document.getElementById('goal-amount-'+_idx).innerHTML = gol.amount
                                    document.getElementById('goal-description-'+_idx).innerHTML = gol.description
                                    @project.attach('goals', gol)
                            , false)

                            document.getElementById('goal-delete-'+_idx).addEventListener('click', (e) =>

                                if e?.preventDefault
                                    e.preventDefault()
                                    e.stopPropagation()
                                    clicked = e.target
                                    _idx = clicked?.getAttribute('id').split('-').pop()
                                    goal = @project.get_attached('goals', _idx)
                                    _key = goal.key

                                return @goals.delete(_key)
                            , false)

                            return editor

                        editors.push(populate(goal_field)) for goal_field in fields if (fields = Util.get('goal', document.getElementById(base_id+'-modal-content')))?

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

                    return @

                ### end current edit functionality - below code is future-planned, thanks to bugs :(

                # extract goal & key from params
                if goal_or_key.key.key
                    # we got a goal
                    goal = goal_or_key
                    goal_key = goal.key
                    goals = [goal]

                else if goal_or_key.key and goal_or_key.constructor.name is 'Key'

                    goal_key = goal_or_key
                    goal = @goals.get(goal_key)
                    goals = [goal]


                goal_editor.steps = []
                goal_editor._state.current = 0
                goal_editor.step = (incr, callback) ->
                    if not incr?
                        incr = 1

                    current_idx = @_state.current
                    current_step = @steps[current_idx]
                    next_step = @steps[current_idx + incr]

                    $(current_step).animate opacity: 0
                        duration: 250
                        complete: () =>
                            $(next_step).animate opacity: 1
                                duration: 200
                                complete: () =>
                                    @_state.current += incr
                                    return if callback? then callback?(next_step) else @

                ###


        @share = (sm_service) =>

            ## share a project via social media
            # what do?

            alert 'Testing social sharing!'

        @tiers =

            get: (tier_key, callback) =>
                ## get tier by key

                if tier_key is false
                    # just return local version
                    tier_key = callback
                    idx = @project.tiers_by_key[tier_key]
                    return if idx then @project.tiers[idx] else null

                else
                    # get from the server
                    $.apptools.api.project.get_tier({key: tier_key}).fulfill

                        success: (response) =>
                            tier = @project.attach('tier', new Tier().from_message(response.tier))

                            return if callback? then callback.call(@, tier) else tier

                        failure: (error) =>
                            alert 'tiers.get() failure'


            list: (callback) =>

                ## list tiers by project key
                $.apptools.api.project.list_tiers({project: @project_key}).fulfill

                    success: (response) =>
                        tiers = []
                        _at = (_t) =>
                            _tier = new Tier()
                            _tier = _tier.from_message(_t)
                            @project.attach('tiers', _tier)
                            return _tier

                        tiers.push(_at(tier)) for tier in response.tiers

                        return if callback? then callback.call(@, tiers) else tiers

                    failure: (error) =>
                        alert 'tiers.list() failure'
                        console.log('Error listing tiers: ' + error)

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

            edit: (tier_or_key) =>

                ## coordinates editing tier properties
                base_id = 'project-tier-editor'
                base_el = null

                return @tiers.list (tiers) =>
                    _pk = @project_key
                    _idx = null
                    _key = null

                    $.apptools.widgets.modal.create (() =>
                        document.body.appendChild(Util.create_doc_frag(Util.create_element_string('div'
                            id: base_id
                            class: 'pre-modal'
                            style: 'opacity: 0;'
                            'data-title': 'editing project tiers...'
                        , ((tier_div='') =>
                            (tier_div += Util.create_element_string('div'
                                id: 'tier-editing-'+ (() =>
                                    ti = @project.attach('tiers', t)
                                    _idx = @project.get_attached('tiers', ti.key, true)
                                    return _idx
                                )()
                                class: 'mini-editable tier'

                            , ((parts='') =>
                                parts += Util.create_element_string('h3',
                                    class: 'tier-field amount'
                                    id: 'tier-amount-' + _idx
                                    contenteditable: true
                                , t.amount)
                                parts += Util.create_element_string('p',
                                    class: 'rounded tier-field description'
                                    id: 'tier-description-' + _idx
                                    contenteditable: true
                                , (if t.description? then t.description else '<span class="shh">default description</span>'))
                                parts += Util.create_element_string('button',
                                    id: 'tier-save-' + _idx,
                                    class: 'tier-button save'
                                ,'save tier')
                                parts += Util.create_element_string('button',
                                    id: 'tier-get-' + _idx,
                                    class: 'tier-button get'
                                ,'refresh tier')
                                parts += Util.create_element_string('button',
                                    id: 'tier-delete-' + _idx,
                                    class: 'tier-button delete'
                                ,'delete tier')
                                return parts
                            )()
                            )) for t in tiers
                            return tier_div
                        )())))
                        return document.getElementById(base_id)
                    )(), (() =>
                        document.body.appendChild(Util.create_doc_frag(Util.create_element_string('a'
                            id: 'a-'+base_id
                            href: '#'+base_id
                            style: 'display: none'
                        , '')))
                        return document.getElementById('a-'+base_id)
                    )(), (m) =>
                        editors = []
                        populate = (tfield) =>

                            editor = $.apptools.widgets.editor.create(tfield)
                            $.apptools.widgets.editor.enable(editor)
                            _el = Util.get((_id = editor._state.element_id))
                            _idx = _id.split('-').pop()

                            document.getElementById('tier-save-'+_idx).addEventListener('click', (e) =>

                                if e? and e.preventDefault
                                    e.preventDefault()
                                    e.stopPropagation()
                                    clicked = e.target
                                    _idx = clicked?.getAttribute('id').split('-').pop()
                                    tier = @project.get_attached('tiers', _idx)
                                    _key = tier.key

                                tier.target = @project_key
                                tier.amount = parseInt(document.getElementById('tier-amount-'+_idx).innerHTML)
                                tier.description = document.getElementById('tier-description-'+_idx).innerHTML

                                return false if not tier.amount? or not tier.description?

                                $.apptools.api.project.put_tier(tier).fulfill
                                    success: (response) =>
                                        _el.style.backgroundColor = '#bada55'
                                        clicked?.classList.add('success')

                                        setTimeout(() =>
                                            $(_el).animate
                                                'background-color': 'transparent'
                                            ,
                                                duration: 300
                                                complete: () =>
                                                    editor.hide()
                                        , 200)

                                        return @project.attach('tiers', new tier.from_message(response))

                                    failure: (error) =>
                                        _el.style.backgroundColor = 'red'
                                        clicked.classList.add('failure')
                                        alert 'tier put() failure'
                            , false)

                            document.getElementById('tier-get-'+_idx).addEventListener('click', (e) =>

                                if e?.preventDefault
                                    e.preventDefault()
                                    e.stopPropagation()
                                    clicked = e.target
                                    _idx = clicked?.getAttribute('id').split('-').pop()
                                    tier = @project.get_attached('tiers', _idx)
                                    _key = tier.key

                                return @tiers.get _key, (teer) =>
                                    document.getElementById('tier-amount-'+_idx).innerHTML = teer.amount
                                    document.getElementById('tier-description-'+_idx).innerHTML = teer.description
                                    @project.attach('tiers', teer)
                            , false)

                            document.getElementById('tier-delete-'+_idx).addEventListener('click', (e) =>

                                if e?.preventDefault
                                    e.preventDefault()
                                    e.stopPropagation()
                                    clicked = e.target
                                    _idx = clicked?.getAttribute('id').split('-').pop()
                                    tier = @project.get_attached('tiers', _idx)
                                    _key = tier.key

                                return @tiers.delete(_key)
                            , false)

                            return editor

                        editors.push(populate(tier_field)) for tier_field in fields if (fields = Util.get('tier', document.getElementById(base_id+'-modal-content')))?

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

                    return @

        @update = () =>

            ## post an update to a project
            if @_state.o
                $.apptools.api.project.post(target: @project_key).fulfill

                    success: () =>
                        # no response i think?
                        alert 'update() success'

                    failure: (error) =>
                        alert 'update() failure'

            else throw new UserPermissionsError(@constructor.name, 'Current user is not a project owner.')


        @_init = () =>

            if window._cp
                document.getElementById('follow').addEventListener('click', @follow, false)
                document.getElementById('share').addEventListener('click', @share, false)
                document.getElementById('back').addEventListener('click', @back, false)

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

            return @get()



# proposal controller
class ProposalController extends OpenfireController

    @events = []

    constructor: (openfire, window) ->

        @_init = () =>
            return


if @__openfire_preinit?
    @__openfire_preinit.abstract_base_objects.push(Asset)
    @__openfire_preinit.abstract_base_objects.push(ProjectImage)
    @__openfire_preinit.abstract_base_objects.push(ProjectVideo)
    @__openfire_preinit.abstract_base_objects.push(ProjectVideo)
    @__openfire_preinit.abstract_base_classes.push(Project)
    @__openfire_preinit.abstract_base_classes.push(Proposal)
    @__openfire_preinit.abstract_base_controllers.push(ProjectController)
    @__openfire_preinit.abstract_base_controllers.push(ProposalController)
