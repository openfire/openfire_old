## openfire user models & controllers

# base session object: represents a single session
class Session extends OpenfireObject

    @export: 'private'
    @events: ['SESSION_OPEN', 'SESSION_CLOSE']

    constructor: () ->

        # internal state
        @_state =
            status: null
            init: false

        # internal methods
        @internal =

            resolve_storage_driver: () =>   # where to have be storing session details?
                return

            provision_token: () =>          # provision session token
                return

        # start a session
        @start = () =>
            return

        # end the session
        @end = () =>
            return


# base user class: it's a user.
class User extends Model

    @export: 'private'
    @events: []

    model:
        username: String()
        firstname: String()
        lastname: String()
        bio: String()
        topics: Array(Topic())
        location: String()
        email: Array()

    constructor: () ->
        
        super

        @attach_topic = (topic, callback) ->
            return



# topic: describes a topic of interest, attached to a User
class Topic extends Model

    @export: 'private'

    model:
        slug: String()
        name: String()
        description: String()
        user_count: Number()


class UserController extends OpenfireController

    @mount: 'user'
    @export: 'private'
    @events: [
        'USER_CREATED'
        'USER_REFRESHED'
        'USER_UPDATED'
        'USER_DELETED'
        'PROFILE_UPDATED'
        'TOPIC_ADDED'
        'TOPIC_REMOVED'
        'USER_AVATAR_ADDED'
        'USER_LOGIN'
        'USER_LOGOUT'
        'USER_CONTROLLER_INIT'
        'USER_CONTROLLER_READY'
    ]

    login: () ->
        return

    logout: () ->
        return

    create: () ->
        return

    constructor: (openfire, window) ->

         @_state =

            init: false

        @session = new Session()

        # auth methods
        @open = () =>
            return @session.start()

        @close = () =>
            return @session.end()

        @login = () =>
            return

        @logout = () =>
            return


        # user methods
        @create = () =>
            return        

        @get = () =>
            return

        @update = () =>
            return

        @delete = () =>
            return

        # profile methods
        @update_profile = () =>
            return

        @attach_avatar = () =>
            return

        @add_topic = () =>
            return

        @suggest_topic = () =>
            return

	    @_init = () =>
	        return

	    return

if @__openfire_preinit?
    @__openfire_preinit.abstract_base_objects.push(Session)
    @__openfire_preinit.abstract_base_classes.push(User)
    @__openfire_preinit.abstract_base_classes.push(Topic)
	@__openfire_preinit.abstract_base_controllers.push(UserController)
