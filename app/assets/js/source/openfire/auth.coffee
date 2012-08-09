## openfire auth classes & controllers

# base session object: represents a single session
class Session extends OpenfireObject

    @export: 'private'
    @events: ['SESSION_START', 'SESSION_ENDED']

    constructor: (openfire) ->

        # internal state
        @_state =
            status: null
            init: false

        # internal methods
        @internal =

            resolve_storage_driver: () =>   # where to have be storing session details?
                return storage

            provision_token: () =>          # provision session token
                return token

        # start a session
        @start = () =>
            return session

        # end the session
        @end = () =>
            return


# base user class: it's a user.
class User extends Model

    @export: 'private'
    @events: []

    constructor: (openfire) ->
        return


# base auth controller: handles frontend user & login services
class AuthController extends OpenfireController

    @events: []

    constructor: (openfire, window) ->

        # internal state
        @_state =
            init: false

        # internal methods
        @internal =

            session:
                # initiate session
                open: () =>
                    return (s = new Session()).start()

                # end session
                close: (session) =>
                    return session.end()

        # login handler - generates dialogue & handles auth
        @login = () =>
            return

        # registers a user & probably handles the session and all that jazz. Lots going on, lots of api calls!
        @create_user = () =>
            return

        @_init = () =>
            return


if @__openfire_preinit?
    @__openfire_preinit.abstract_base_objects.push(Session)
    @__openfire_preinit.abstract_base_classes.push(User)
    @__openfire_preinit.abstract_base_controllers.push(AuthController)
