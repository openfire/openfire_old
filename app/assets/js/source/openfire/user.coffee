## openfire user profile models & controllers

class Topic extends Model

    model:
        slug: String()
        name: String()
        description: String()
        user_count: Number()

class Profile extends Model

    @events: ['PROFILE_TOPIC_ATTACHED']

    model:
        username: String()
        email: String()
        firstname: String()
        lastname: String()
        bio: String()
        location: String()
        topics: Array()

    constructor: (key) ->

        super(key)

        @topics = []
        @get = (sync, callback) =>
            @::log('Pulling profile from server...')
            $.apptools.api.user.profile


class ProfileController extends OpenfireController

    @export: 'private'
    @events: [
        'PROFILE_CONTROLLER_INIT',
        'PROFILE_CONTROLLER_READY',
        'PROFILE_SAVED',
        'PROFILE_LOADED'
    ]

    constructor: (openfire, window) ->

        @user = null
        @profile = null

        @put = () =>

            return @
            # $.apptools.api.user.profile

        @get = () =>

	    @_init = () =>
	        return

	    return

if @__openfire_preinit?
	@__openfire_preinit.abstract_base_controllers.push(UserController)
