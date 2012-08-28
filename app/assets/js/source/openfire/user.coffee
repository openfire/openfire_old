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

    constructor: (@user) ->
        super

        @get = () =>
            return $.apptools.api.user.profile(user: @username).fulfill
                success: (r) =>
                    @from_message(r)
                    return @
                failure: (e) =>
                    return @

        @put = (sync=false) =>
            return $.apptools.api.user.profile(@to_message()).fulfill
                success: (r) =>
                    @from_message(r)
                    return @
                failure: (e) =>
                    return @

    attach_topic: (topic, callback) =>
        return @


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

    template: ''

    constructor: (openfire, window) ->
        if (u = $.apptools.user.current_user)?
            @user = new User(username: u.username)
            @user.get()

        super()

        @_state =
            init: false

        # auth methods
        @login = () =>
            return

        @logout = () =>
            return

        # profile methods
        @profile =

            get: (sync=false, cb) =>
                if typeof sync is 'function'
                    cb = sync
                    sync = false
                profile = @get(sync)
                return (if cb? then cb(profile) else profile)

            put: (cb) =>
                return $.apptools.api.user.profile(@user.to_message()).fulfill
                    success: (response) =>
                        return @user.from_message(response)
                    failure: (error) =>
                        $.apptools.dev.error('User profile put() error:', error)
                        return @user

            edit: () =>

        # topic methods
        @topics =

            list: (sync=false, cb) =>
                if typeof sync is 'function'
                    cb = sync
                    sync = false
                topics = @get(sync).topics
                return (if cb? then cb(topics) else topics)

            add: () =>
            remove: () =>

            set: (topic_array, sync=false) =>
                user = @user
                user.topics = new ListField().join(topic_array)
                return (@user = user) if not sync
                return $.apptools.api.user.set_topics(user.to_message()).fulfill
                    success: (r) =>
                        _.get('#topics').innerHTML = @template.render('{{>topics}}<span class="interest topic tag" data-topic-slug="{{=slug}}">{{=name}}<span class="delete-tag">x</span></span>{{/topics}}', user)
                        return @user = user.from_message(response)
                    failure: (e) =>
                        console.log('Error setting user topics:', error)
                        return @user

            edit: () =>
                modal_id = 'user-topic-editor'
                t = '{{>topics}}<span class="topic-edit" id="topic-edit-{{=key}}">{{=name}}</span>{{/topics}}'

                return @topics.list true, (topics) =>

                    if !!(modal = $.apptools.widgets.modal.get(modal_id))
                        return modal.render(@template.render(t, @user.to_message()))

                    else
                        df = _.create_doc_frag _.create_element_string('div',
                            id: modal_id
                            class: 'pre-modal'
                            style: 'opacity: 0;'
                            'data-title': 'editing user topics...'
                        , @template.render(t, @user.to_message())), _.create_element_string('a',
                            id: 'a-'+modal_id
                            style: 'display: none'
                        , '')
                        modal = df.firstChild
                        trigger = df.lastChild
                        document.body.appendChild(df)

                        return $.apptools.widgets.modal.create(modal, trigger, (m) =>
                            return m.open()
                        , {})

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
