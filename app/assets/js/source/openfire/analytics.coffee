
# analytics controller
class AnalyticsController extends OpenfireController

    @mount = 'analytics'
    @export = 'private'

    @events = [

        ## Internal Events
        'ANALYTICS_INIT',
        'ANALYTICS_PUSH',
        'ANALYTICS_EVENT',
        'ANALYTICS_READY',

        ## Vars + Config
        'ANALYTICS_CONFIG',
        'ANALYTICS_SETVAR',

        ## Tracking Events
        'ANALYTICS_TRACK_EVENT',
        'ANALYTICS_TRACK_SOCIAL',
        'ANALYTICS_TRACK_TIMING',
        'ANALYTICS_TRACK_PAGEVIEW',
        'ANALYTICS_TRACK_CAMPAIGN',
        'ANALYTICS_TRACK_TRANSACTION',

        ## E-Commerce Events
        'ANALYTICS_TRANSACTION_NEWITEM',
        'ANALYTICS_TRANSACTION_COMPLETE'

    ]

    constructor: (openfire, window) ->

        ## build analytics state
        @state =

            # tracker/runtime config
            vars: {}
            agent: {}
            trackers: {}

            # tracked analytics operations
            data:
                events: []
                social: []
                timing: []
                campaigns: []
                transactions: []

            index:
                timing: {}
                networks: {}
                campaigns: {}
                transactions: {}

            # analytics API references
            _ga:
                queue: null
                tracker: null
                scopes: ['visitor', 'session', 'page']
                bindings:
                   ANALYTICS_SETVAR: '_setCustomVar'
                   ANALYTICS_TRACK_EVENT: '_trackEvent'
                   ANALYTICS_TRACK_SOCIAL: '_trackSocial'
                   ANALYTICS_TRACK_TIMING: '_trackTiming'
                   ANALYTICS_TRACK_PAGEVIEW: '_trackPageview'
                   ANALYTICS_TRACK_CAMPAIGN: '_setCampaignTrack'
                   ANALYTICS_TRACK_TRANSACTION: '_addTrans'
                   ANALYTICS_TRANSACTION_NEWITEM: '_addItem'
                   ANALYTICS_TRANSACTION_COMPLETE: '_trackTrans'


            # build analytics config
            config:
                account_ids:
                    openfire: null
                    project: null

                anonymize: false
                samplerate: 1
                multitrack: false

        @_init = (openfire) =>

            _.ready (window) =>
                if window._gacfg?
                    $.openfire.analytics.internal.initialize(window._gat, window._gaq, window._gacfg)
                else
                    $.openfire.analytics.internal.initialize(window._gat, window._gaq)
                return
            return

        ## internal methods
        @internal =

            initialize: (_gat, _gaq, config={}) =>

                # splice in overrides from config
                @state.config = _.extend(true, {}, @state.config, config)
                $.apptools.dev.verbose('OF:Analytics', 'Initializing Google Analytics integration.', _gat, _gaq, @state.config)

                # bind apptools events
                @internal.bind_events()

                if (not _gat?) or (not _gaq?)
                    $.apptools.dev.error('OF:Analytics', 'Failed to find Google Analytics. Make sure it\'s installed and initialization is properly deferred.')
                else
                    # copy over analytics apis
                    @state._ga.queue = _gaq
                    @state._ga.tracker = _gat

                    # init openfire tracker
                    @internal.provision_tracker('openfire', @state.config.account_ids.openfire)

                    # init extra trackers, if multitrack is enabled
                    if @state.config.multitrack
                        for key, value of @state.config.account_ids
                            if key != 'openfire'
                                @internal.provision_tracker(key, value)

                return @

            bind_events: () =>

                ## bind tracker initialization logic
                _.bind 'ANALYTICS_INIT', (name, tracker) =>
                    $.apptools.dev.verbose('OF:Analytics', 'Tracker initialized.', name, tracker)

                    # queue anonymization if it's on
                    if @state.config.anonymize
                        _.trigger 'ANALYTICS_PUSH', ['_gat._anonymize_ip']

                ## bind tracker command logic
                _.bind 'ANALYTICS_PUSH', (method, args...) =>
                    $.apptools.dev.verbose('OF:Analytics', 'Pushing tracker command.', method, args)

                    # add the method on first, then dispatch to the trackers
                    args.unshift(method)
                    @internal.push_command args

                ## bind tracker ready logic
                _.bind 'ANALYTICS_READY', (trackers) =>
                    $.apptools.dev.verbose('OF:Analytics', 'Analytics is READY to receive events.', 'config:', @state.config, 'trackers:', trackers)


                ## bridge low-level tracking events to the command queue
                _.bridge [ 'ANALYTICS_SETVAR'
                           'ANALYTICS_TRACK_EVENT',
                           'ANALYTICS_TRACK_SOCIAL',
                           'ANALYTICS_TRACK_TIMING',
                           'ANALYTICS_TRACK_PAGEVIEW',
                           'ANALYTICS_TRACK_CAMPAIGN',
                           'ANALYTICS_TRACK_TRANSACTION',
                           'ANALYTICS_TRANSACTION_NEWITEM',
                           'ANALYTICS_TRANSACTION_COMPLETE' ],
                           [
                                'ANALYTICS_PUSH'

                           ], (args, source) ->

                                # resolve GA method from event name
                                command_spec = [@state.config._ga.bindings[source]]

                                # if it's an array with more than one item, it's position args
                                if _.is_array(args) and args.length > 1

                                    for value in args

                                        # discard null values
                                        if value?
                                            command_spec.push value
                                        else
                                            continue

                                # if it's an array with a length of one, or an object (kwargs)
                                else

                                    # if it's an object (in position 0 of the 1-item array or as an object itself)
                                    if (_.is_object(args) and not _.is_array(args)) or (args.length == 1 and _.is_object(args[0]))

                                        # pull it out of the array if it's not an object literal
                                        if not _.is_object(args)
                                            args = args[0]

                                        for key, value of args

                                            # discard null values, all values are strings
                                            if value?
                                                command_spec.push value

                                    # if it's a literal string or something
                                    else
                                        command_spec.push args[0]

                                # return hash that is expanded to be ANALYTICS_PUSH context
                                return command_spec


                ## bridge mid-level controller events to the main event trunk
                _.bridge [ 'ANALYTICS_INIT',
                           'ANALYTICS_PUSH',
                           'ANALYTICS_READY' ],
                           [
                                'ANALYTICS_EVENT'

                           ], (args, source) =>

                                event_spec = source.split('_')[0]
                                args.unshift(event_spec)
                                $.apptools.dev.log 'OF:Analytics', 'Emitted "' + event_spec + '".', args
                                return args

                return @

            provision_tracker: (name, account) =>

                @state.trackers[name] = @state._ga.tracker._createTracker(account, name)
                $.apptools.events.trigger('ANALYTICS_INIT', name: name, tracker: @state.trackers[name])
                return @state.trackers[name]

            push_command: (command, all_trackers=true) =>

                if all_trackers
                    targets = @state.trackers
                else
                    targets = [@state.trackers.openfire]

                touched_trackers = 0
                for target in targets
                    target.push command
                    touched_trackers++

                return touched_trackers

        @config =

            flash: (enable=null) =>

                if enable?
                    return @state._ga.tracker._setDetectFlash(enable)
                return @state._ga.tracker._getDetectFlash()

            title: (enable=null) =>

                if enable?
                    return @state._ga.tracker._setDetectTitle(enable)
                return @state._ga.tracker._getDetectTitle()

            client: (enable=null) =>

                if enable?
                    return @state._ga.tracker._setClientInfo(enable)
                return @state._ga.tracker._getClientInfo()

            anonymize: (enable=null) =>

                if enable?
                    @state.config.anonymize = enable
                return @state.config.anonymize

            samplerate: (value=null) =>

                if value?
                    @state.config.samplerate = value
                return @state.config.samplerate

        @vars =

            set: (slot, name, value, scope='page') =>

                if _.is_string(scope)
                    scope = _.indexOf(@state.config._ga.scopes, scope)
                _.trigger 'ANALYTICS_SETVAR', [slot, name, value, scope]
                return @

        @track =

            event: (category, action, label=null, value=null, non_interaction=false) =>

                _command_spec = [category, action]
                if label?
                    _command_spec.push label
                if value?
                    _command_spec.push value
                if non_interaction != false
                    _command_spec.push non_interaction
                _.trigger 'ANALYTICS_TRACK_EVENT', _command_spec
                return @

            social: (network, action, target=null, path=null) =>

                _command_spec = [network, action]
                if target?
                    _command_spec.push target
                if path?
                    _command_spec.push path
                _.trigger 'ANALYTICS_TRACK_SOCIAL', _command_spec
                return @

            timing: (category, variable, time, label=null, samplerate=null) =>

                _command_spec = [category, variable, time]
                if label?
                    _command_spec.push label
                if samplerate?
                    _command_spec.push samplerate
                _.trigger 'ANALYTICS_TRACK_TIMING', _command_spec
                return @

            pageview: (page_url=null) =>

                _command_spec = []
                if page_url?
                    _command_spec.push page_url
                _.trigger 'ANALYTICS_TRACK_PAGEVIEW', _command_spec
                return @

            campaign: (content_key, medium, name, source, term, nokey=null) =>
            transaction: (order_id, affiliation, total, tax, shipping, city, state, country) =>

        @transactions =

            item: (order_id, sku, name, category, price, quantity) =>
                return

            complete: (order_id=null) =>
                return

if @__openfire_preinit?
    @__openfire_preinit.abstract_base_classes.push AnalyticsController
    @__openfire_preinit.abstract_base_controllers.push AnalyticsController
