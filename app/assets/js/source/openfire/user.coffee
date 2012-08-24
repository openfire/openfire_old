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
        @start = @open = () =>
            return

        # end the session
        @end = @close = () =>
            return

# base user class: it's a user.
class User extends Model

    @export: 'public'
    @events: []

    model:
        key: String()
        username: String()
        firstname: String()
        lastname: String()
        bio: String()
        topics: ListField(Topic)
        location: String()
        email: ListField(Email)

    attach_topic: (topic, callback) =>
        return @


# topic: describes a topic of interest, attached to a User
class Topic extends Model

    @export: 'public'

    model:
        key: String()
        slug: String()
        name: String()
        description: String()
        user_count: Number()

# an account email, attached to a user
class Email extends Model


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

    constructor: (openfire, window) ->

        @_state =
            init: false

        @user = new User()
        @session = new Session()

        # auth methods
        @login = () =>
            return

        @logout = () =>
            return

        # user methods (won't use until accts)
        @new = () =>
            return

        @get = () =>
            return

        @update = () =>
            return

        @delete = () =>
            return

        # profile methods
        @profile =

            get: (sync=false) =>
                return @user if not sync
                return $.apptools.api.user.profile(user: @user.key).fulfill
                    success: (response) =>
                        return @user.from_message(response)
                    failure: (error) =>
                        $.apptools.dev.error('User profile get() error:', error)
                        return @user

            put: () =>
                return $.apptools.api.user.profile(@user.to_message()).fulfill
                    success: (response) =>
                        return @user.from_message(response)
                    failure: (error) =>
                        $.apptools.dev.error('User profile put() error:', error)
                        return @user

            edit: () =>

        # topic methods
        @topics =

            list: (sync=false) =>
                return @profile.get(sync).topics

            add: () =>

            remove: () =>

            pick: (topic) =>
                @user.topics.pick(topic)
                return @user

            set: (topic_array) =>
                @user.topics = new ListField().join(topic_array)
                return @user

            edit: () =>

            suggest: () =>

        # avatar methods
        @avatar =
            list: () =>

            edit: () =>

            attach: () =>

            remove: () =>

        @_init = () =>
            return @

        return @

if @__openfire_preinit?
    @__openfire_preinit.abstract_base_objects.push(Session)
    @__openfire_preinit.abstract_base_classes.push(User)
    @__openfire_preinit.abstract_base_classes.push(Topic)
    @__openfire_preinit.abstract_base_controllers.push(UserController)
