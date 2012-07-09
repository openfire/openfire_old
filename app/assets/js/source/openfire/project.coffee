## openfire project classes & controllers

class Asset extends OpenfireObject

    key: null
    url: null

    constructor: (@key, @url) ->
        return @

class Image extends Asset

class Video extends Asset



# base project object
class Project # extends Model

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

    @assets = []
    @assets_by_key = {}

    constructor: (@key) ->
        return @

    attach: (asset) =>
        @assets_by_key[asset.key] = @assets.push(asset) - 1
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
        'PROJECT_BACKED',
        'PROJECT_EDITED',
        'PROJECT_FOLLOWED',
        'PROJECT_READY',                # @get()
        'PROJECT_SHARED',
        'PROJECT_UPDATED',
    ]
    @project = null
    @project_key = null

    constructor: (openfire, window) ->

        @_state = Util.extend(true, {}, window._cp)

        @project = new Project(k = new Key(@_state.ke))
        @project_key = @project.key.key

        @_init = () =>
            return @get()


    add_media: (file_or_url, kind) =>

        ## attach a media item to a project
        if @_state.o

            if file_or_url.type
                # it's a file!
                file = file_or_url

                if /^image\/(png|jpeg|gif)$/gi.test(file.type)

                    # a valid file!
                    $.apptools.api.media.attach_image(

                        intake: 'upload'
                        name: file.name
                        size: file.size
                        target: @project_key

                    ).fulfill

                        success: (response) =>

                            uploader = new Uploader

                                endpoints: [response.endpoint]
                                session: $.openfire.sys.state.session.data or null
                                finish: (response) =>

                                    @project.attach(new Image(response.media_key, response.serve_url))
                                    $.apptools.events.trigger 'PROJECT_MEDIA_ADDED', @

                            uploader.upload(file)

                        failure: (error) =>
                            alert 'uploaded attach_image() failure'

                else throw new MediaError(@constructor.name, 'Tried to upload unsupported filetype. Images must be .jpg, .png, or .gif.')

            else
                # assume it's a URL
                url = file_or_url

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

                else throw new MediaError(@constructor.name, 'Invalid media kind specified.')

        else throw new UserPermissionsError(@constructor.name, 'Current user is not a project owner.')


    back: () =>

        ## back a project
        $.apptools.api.project.back(target: @project_key).fulfill

            success: (response) =>
                alert 'back() success'

            failure: (error) =>
                alert 'back() failure'


    edit: () =>

        ## edit an existing project
        # content api?


    follow: () =>

        ## follow a project
        $.apptools.api.project.follow(target: @project_key).fulfill

            success: (response) =>
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


    share: (sm_service) =>

        ## share a project via social media
        # what do?


    update: () =>

        ## post an update to a project
        if @_state.o
            $.apptools.api.project.post(target: @project_key).fulfill

                success: () =>
                    # no response i think?
                    alert 'update() success'

                failure: (error) =>
                    alert 'update() failure'




# proposal controller
class ProposalController extends OpenfireController

    @events = []

    constructor: (openfire, window) ->

        @_init = () =>
            return


if @__openfire_preinit?
    @__openfire_preinit.abstract_base_objects.push(Asset)
    @__openfire_preinit.abstract_base_objects.push(Image)
    @__openfire_preinit.abstract_base_objects.push(Video)
    @__openfire_preinit.abstract_base_classes.push(Project)
    @__openfire_preinit.abstract_base_classes.push(Proposal)
    @__openfire_preinit.abstract_base_controllers.push(ProjectController)
    @__openfire_preinit.abstract_base_controllers.push(ProposalController)
