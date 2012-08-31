## openfire user models & controllers
class TopicEditTemplate extends t

    @export: 'public'
    constructor: () ->
        super(['<span class="interest topic-edit clear" data-topic="{{=key}}">',
            '<div class="right">',
                '<span class="ctrl promote">&#xf0020;</span>',
                '<span class="ctrl demote">&#xf001f;</span>',
                '<span class="ctrl remove">&#xf0016;</span>',
            '</div>',
            '{{=name}}',
        '</span>'
        ].join(''))
        return @

class TopicTagTemplate extends t
    @export: 'public'
    constructor: () ->
        super('<span class="interest topic tag" data-topic-slug="{{=slug}}">{{=name}}<span class="delete-tag">x</span></span>')
        return @

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
    @export: 'private'
    model:
        key: String()
        address: String()
        label: String()

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

    @template: ''

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
                profile = (if sync then @user.get() else @user)
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
                topics = @profile.get(sync).topics
                return (if cb? then cb(topics) else topics)

            add: () =>
            remove: () =>

            set: (sync=false, topic_keys, cb) =>
                topics = @user.topics
                if not cb? and typeof topic_keys is 'function'
                    cb = topic_keys
                    topic_keys = null

                if topic_keys?
                    topics.order(topic_keys, 'key') if topic_keys.length is topics.length
                else
                    topic_keys = (item.key for item in topics)

                @user.topics = topics

                return (if not sync then @user else $.apptools.api.user.set_topics(user: @user.username, topics: topic_keys).fulfill
                    success: () =>
                        _topics = topics.slice(0,3)
                        @template.t = '{{>topics}}{{+TopicTagTemplate}}{{/topics}}<span class="tag" id="edit-topics">edit topics</span>'
                        _.get('#topics').innerHTML = @template.parse(_.extend({}, @user, topics: _topics))
                        _.bind(_.get('#edit-topics'), 'click', @topics.edit)
                        return (if cb? then cb(@user) else @user)
                    failure: (e) =>
                        console.log('Error setting user topics:', error)
                        return @user
                )

            edit: () =>
                modal_id = 'user-topic-editor'
                @template.t = [
                    '<div class="absolute snapbottom topics-existing">',
                        '{{>topics}}',
                            '{{+TopicEditTemplate}}',
                        '{{/topics}}',
                    '</div>',
                    '<div class="absolute snapbottom snapright topics-new">',
                        '<h4>search for a topic to add</h4>',
                        '<input type="text" class="autocomplete" id="topic-add-search">',
                        '<p style="margin-top: 10%;">Don\'t see the topic you\'d like? <a href="#" id="topic-suggest">Suggest a topic!</a></p>',
                        '<span class="topic tag" id="topics-save">save topics</span>',
                        '</div>'
                    '</div>'
                ].join('')

                return @topics.list false, (topics) =>

                    auto_id = '#topic-add-search'

                    modal_callback = () =>
                        _bind = (b) =>
                            ctrls = _.get('.ctrl', topics_el)
                            return (if b then _.bind(ctrls, 'click', axn) else _.unbind(ctrls, 'click', axn))

                        axn = (e) =>
                            e.preventDefault()
                            e.stopPropagation()

                            _bind(false)

                            btn = e.target
                            topic_el = btn.parentNode.parentNode
                            parent = topic_el.parentNode

                            t_key = topic_el.getAttribute('data-topic')
                            action = btn.className.split(' ').pop()
                            topics = @user.topics

                            @user.topics = topics[action](t_key)

                            if action is 'promote'
                                parent.insertBefore(parent.removeChild(topic_el), prev) if (prev = topic_el.previousSibling)?

                            else if action is 'demote'
                                (if (nxt = topic_el.nextSibling.nextSibling)? then parent.insertBefore(parent.removeChild(topic_el), nxt) else parent.appendChild(parent.removeChild(topic_el)))

                            else if action is 'remove'
                                parent.removeChild(topic_el)

                            return _bind(true)

                        topics_el = _.get('topics-existing', _.get('#'+modal_id+'modal-dialog'))

                        auto = $.openfire.widgets.autocomplete.get(auto_id)
                        (auto ||= $.openfire.widgets.autocomplete.new(_.get('#topic-add-search'), {api: 'topic_autocomplete', result_key: 'topics'})).finish = (otto) =>
                            topic = new Topic().from_message(otto.choice)
                            new_topic = _.create_doc_frag(@template.parse('{{+TopicEditTemplate}}',{key: otto.choice.key, name: otto.choice.name}))
                            topics_el.appendChild(new_topic)
                            (@user.topics ||= new ListField()).push(topic)
                            return

                        _.bind _.get('#topics-save'), 'click', (e) =>
                            e.preventDefault()
                            e.stopPropagation()
                            t_keys = []
                            t_keys.push(item.getAttribute('data-topic')) for item in _.to_array(topics_el.children)
                            return @topics.set(true, t_keys, () => return modal.close())

                        _.bind(_.get('.ctrl', topics_el), 'click', axn)

                    if !!(modal = $.apptools.widgets.modal.get(modal_id))
                        modal.fadeout() if (active = modal._state.active)

                    else
                        df = _.create_doc_frag _.create_element_string('div',
                            id: modal_id
                            class: 'pre-modal'
                            style: 'opacity: 0;'
                            'data-title': 'editing user topics...'
                        , ''), _.create_element_string('a',
                            id: 'a-'+modal_id
                            style: 'display: none'
                        , '')
                        m = df.firstChild
                        trigger = df.lastChild
                        document.body.appendChild(df)

                        modal = $.apptools.widgets.modal.create(m, trigger)

                    modal.render(@template.parse(@user))

                    return (if !!active then modal.fadein(modal_callback) else modal.open(modal_callback))

            suggest: () =>

        # avatar methods
        @avatar =
            list: () =>

            edit: () =>

            attach: () =>

            remove: () =>

        @_init = () =>
            _.bind(_.get('#edit-topics'), 'click', @topics.edit)
            return @

        return @

if @__openfire_preinit?
    @__openfire_preinit.abstract_base_objects.push TopicEditTemplate,
                                                   TopicTagTemplate
                                                   Session,
                                                   User,
                                                   Topic
    @__openfire_preinit.abstract_base_controllers.push(UserController)
