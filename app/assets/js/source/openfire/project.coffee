## openfire project classes & controllers

# project media
class ProjectImage extends Asset

class ProjectVideo extends Asset

class ProjectAvatar extends Asset

# project object classes

class Goal

    constructor: (@key) ->
        return @

class Tier

    constructor: (@key) ->
        return @



# base project object
class Project # extends Model

    ###
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
    ###

    constructor: (@key) ->

        @assets = []
        @goals = []
        @tiers = []

        @index =
            assets_by_key: {}
            goals_by_key: {}
            tiers_by_key: {}

        return @

    attach_asset: (a) =>
        @index.assets_by_key[a.key] = @assets.push(a) - 1
        return @

    attach_goal: (g) =>
        @index.goals_by_key[g.key] = @goals.push(g) - 1
        return @

    attach_tier: (t) =>
        @index.tiers_by_key[t.key] = @tiers.push(t) - 1
        return @

    from_message: (message) =>
        # should eventually live on Model?

        return Util.extend(true, @, message)


# base proposal object
class Proposal # extends Model

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
    @project = null
    @project_key = null
    @uploader = null

    constructor: (openfire) ->

        @_state = Util.extend(true, {}, window._cp)

        @project = new Project(k = new Key(@_state.ke))
        @project_key = @project.key.key
        @goals = {}
        @tiers = {}

        @_init = () =>

            if window._cp
                document.getElementById('follow').addEventListener('click', @follow, false)
                document.getElementById('share').addEventListener('click', @share, false)
                document.getElementById('back').addEventListener('click', @back, false)

                if @_state.o
                    document.body.addEventListener('drop', @add_media, false)

            return @get()


    add_media: (file_or_url, kind) =>

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


    back: () =>

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


    edit: () =>

        ## edit an existing project
        # content api?

    edit_goal: (key) =>

        goal_editor = $.apptools.widgets.modal.create (() =>
            docfrag = Util.create_doc_frag([
                '<div id="project-goal-editor-modal" class="pre-modal" style="text-align: center" data-title="editing goal...">',
                    '<div id="project-goal-editor-title" class="mini-editable"></div>',
                    '<div id="project-goal-editor-contribution-type" class="mini-editable"></div>',
                    '<div id="project-goal-editor-amount" class="mini-editable"></div>',
                    '<div id="project-goal-editor-description" class="mini-editable"></div>',
                    '<button id="project-goal-editor-save" value="save all">save all</button>'
                '</div>'
            ].join(''))
            document.body.appendChild(docfrag)
            return document.getElementById('project-goal-editor-modal')
        )(),(() =>
            docfrag = Util.create_doc_frag((() =>
                return Util.create_element_string 'a',
                    href: '#project-goal-editor-modal'
                    id: 'a-project-goal-editor-modal'
                    style: 'display: none;'
            )())
            document.body.appendChild(docfrag)
            return document.getElementById('a-project-goal-editor-modal')
        )(), (m) ->

            $.apptools.widgets.editor.create(field) for field in document.getElementById('project-goal-editor-modal').children
            return m.open()

        Util.get()



    edit_tier: () =>

        ## edit a project


    follow: () =>

        ## follow a project
        $.apptools.api.project.follow(target: @project_key).fulfill

            success: (response) =>
                document.getElementById('follow').classList.add('following')
                alert 'follow() success'

            failure: (error) =>
                alert 'follow() failure'


    get: (from_server) =>

        if from_server

            $.apptools.api.project.get(target: @project_key).fulfill

                success: (response) =>
                    return @project.from_message(response)

                failure: (error) =>
                    alert 'get() failure'

        else return @project


    get_backers: () =>

        ## get project backers
        $.apptools.api.project.backers(target: @project_key).fulfill

            success: (response) =>
                # response.users = []
                alert 'get_backers() success'

            failure: (error) =>
                alert 'get_backers() failure'


    get_followers: () =>

        ## get project followers
        $.apptools.api.project.followers(target: @project_key).fulfill

            success: (response) =>
                # response.profiles = []
                alert 'get_followers() success'

            failure: (error) =>
                alert 'get_followers() failure'


    get_updates: () =>

        ## get recent updates
        $.apptools.api.project.posts(target: @project_key).fulfill

            success: (response) =>
                # response.posts = []
                alert 'get_updates() success'

            failure: (error) =>
                alert 'get_updates() failure'

    goals:

        get: (key, callback) =>

            ## get goal by key
            $.apptools.api.project.get_goal({}).fulfill

                success: (response) =>
                    alert 'goals.get() success'
                    callback.call(@, response) if callback?

                failure: (error) =>
                    alert 'goals.get() failure'


        list: (callback) =>

            ## list goals by project key
            $.apptools.api.project.list_goals({}).fulfill

                success: () =>
                    alert 'goals.list() success'
                    callback.call(@, response) if callback?

                failure: (error) =>
                    alert 'goals.list() failure'

        put: (key, callback) =>

            ## put goal by key
            $.apptools.api.project.put_goal({}).fulfill

                success: () =>
                    alert 'goals.put() success'
                    callback.call(@, response) if callback?

                failure: (error) =>
                    alert 'goals.put() failure'

        delete: (key, callback) =>

            ## delete goal by key
            $.apptools.api.project.delete_goal({}).fulfill

                success: () =>
                    alert 'goals.delete() success'
                    callback.call(@, response) if callback?

                failure: (error) =>
                    alert 'goals.delete() failure'


    share: (sm_service) =>

        ## share a project via social media
        # what do?

        alert 'Testing social sharing!'

    tiers:

        get: () =>

            ## get tier by key
            $.apptools.api.project.get_tier({}).fulfill

                success: () =>
                    alert 'tiers.get() success'

                failure: (error) =>
                    alert 'tiers.get() failure'

        list: () =>

            ## list tiers by project key
            $.apptools.api.project.list_tiers({}).fulfill

                success: () =>
                    alert 'tiers.list() success'

                failure: (error) =>
                    alert 'tiers.list() failure'

        put: () =>

            ## put tier by key
            $.apptools.api.project.put_tier({}).fulfill

                success: () =>
                    alert 'tiers.put() success'

                failure: (error) =>
                    alert 'tiers.put() failure'

        delete: () =>

            ## delete tier by key
            $.apptools.api.project.delete_tier({}).fulfill

                success: () =>
                    alert 'tiers.delete() success'

                failure: (error) =>
                    alert 'tiers.delete() failure'


    update: () =>

        ## post an update to a project
        if @_state.o
            $.apptools.api.project.post(target: @project_key).fulfill

                success: () =>
                    # no response i think?
                    alert 'update() success'

                failure: (error) =>
                    alert 'update() failure'

        else throw new UserPermissionsError(@constructor.name, 'Current user is not a project owner.')



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
