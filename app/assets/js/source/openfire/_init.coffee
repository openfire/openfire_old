## openfire page init
class Openfire

    constructor: (window) ->

        @sys =

            core_events: ['OPENFIRE_READY']

            # internal config
            config:
                session:
                    cookie: "ofsession"
                    header: "X-AppFactory-Session"
                    timeout: 86400  # one day, for now
                    cookieless: false
                csrf:
                    cookie: "ofcsrf"
                    header: "X-AppFactory-CSRF"

            # internal state
            state:

                status: 'NOT_READY' # System status
                flags: []           # System flags
                preinit: {}         # System preinit
                controllers: {}     # Installed system controllers
                classes: {}         # Installed openfire-related classes
                objects: {}         # Installed openfire-related objects
                session:            # Runtime session info
                    data: null
                    verified: false
                    timestamp: null
                    signature: null
                    established: false
                    authenticated: false
                    csrf:
                        next: null
                        history: []

                consider_preinit: (preinit) =>

                    # first consider base objects
                    if preinit.abstract_base_objects?
                        @sys.install.object(obj) for obj in preinit.abstract_base_objects

                    # next classes
                    if preinit.abstract_base_classes?
                        @sys.install.class(cls) for cls in preinit.abstract_base_classes

                    # then controllers
                    if preinit.abstract_base_controllers?
                        @sys.install.controller(ctrlr) for ctrlr in preinit.abstract_base_controllers

                    return preinit  # preinit HANDLED.


                sniff_headers: (document) =>

                    $.apptools.dev.verbose('openfire', 'Sniffing response cookies.')

                    # only lookin' for cookies right now
                    try
                        session = null
                        for i, cookie of document.cookie.split(";")
                            $.apptools.dev.verbose('openfire:sessions', 'Found a cookie.', i, cookie, cookie.replace('"', '').replace('"', '').split("="))
                            [key, cookie] = cookie.split("=");
                            if key == @sys.config.session.cookie
                                [data, timestamp, signature] = session = cookie.split("|")
                                $.apptools.dev.verbose('openfire:sessions', 'Possibly valid session cookie found!', @sys.config.session.cookie, data, timestamp, signature)
                                if session.length > 2  # must be at least 3 (data|timestamp|hash), could sometimes come through as (data|timestamp|hash|csrf)
                                    ## @TODO: verify session signature
                                    $.apptools.dev.verbose('openfire:sessions', 'Checking session timeout with TTL of ', @sys.config.session.timeout, 'and session creation time of', session[1])
                                    if ((+new Date(+timestamp * 1000)) + (_this.sys.config.session.timeout * 1000)) > +new Date()  # check expiration
                                        session =
                                            data: data
                                            timestamp: timestamp
                                            signature: signature
                                        $.apptools.dev.log('openfire:sessions', 'Valid session found and loaded.', session)
                                break
                            continue

                        if session isnt null and session isnt false
                            @sys.state.session.data = session.data
                            @sys.state.session.timestamp = session.timestamp
                            @sys.state.session.signature = signature.replace('"', '')
                            @sys.state.session.established = true

                    catch err
                        $.apptools.dev.error('openfire:sessions', 'An unknown exception was encountered when attempting to load the user\'s session.', err)
                        @sys.state.session.error = true

                    return @sys.state.session.established

            install:
                # installs an openfire base object
                object: (obj) =>
                    # stash for future queries
                    @sys.state.objects[(o=obj.name)] = obj

                    # register any object events
                    if obj.events?
                        window.apptools?.events?.register(obj.events)

                    # bind to window, if obj isn't private
                    window[o] = obj unless obj.export is 'private'
                    return obj

                # installs an openfire base class
                class: (cls) =>
                    if (mount = cls.mount)?
                        if not @[mount]
                            @[mount] = []
                        if @[mount] instanceof Array
                            @[mount].push(cls)
                            return
                        else
                            cls = new cls(@)
                            cls._init?(@)
                            return

                    @sys.state.classes[(cl=cls.name)] = cls
                    if cls.events?
                        window.apptools?.events?.register(cls.events)

                    window[cl] = cls unless cls.export is 'private'
                    return cls

                # installs an openfire controller
                controller: (ctrlr) =>
                    mount_point = if ctrlr.mount? then ctrlr.mount else ctrlr.name.toLowerCase()
                    if @[mount_point]?
                        deferred_cls = @[mount_point]
                        @[mount_point] = null

                    @sys.state.controllers[mount_point] = ctrlr
                    if ctrlr.events?
                        window.apptools?.events?.register(ctrlr.events)

                    window[mount_point] = ctrlr unless ctrlr.export is 'private'
                    ctrlr = new ctrlr(@, window)

                    @[mount_point] = ctrlr
                    ctrlr._init?(@)

                    @sys.install.class(cls) for cls in deferred_cls if deferred_cls?

                    return ctrlr


            go: (window) =>
                # oh snap it's go time
                window.apptools?.dev?.verbose 'Openfire', 'Openfire systems go.'
                @sys.state.status = 'READY'
                if window.__clock?
                   window.__clock.clockpoint('JavaScript', 'Platform Ready', window.__clock.ts[0][0], 'openfire', 100)

	                $.apptools.events.hook 'RPC_FULFILL', (directive) =>
	                    directive.firetime = window.__clock.pn()

	                $.apptools.events.hook 'RPC_SUCCESS', (directive) =>
                        directive.finishtime = window.__clock.pn()
                        directive.runtime = (Math.floor(directive.finishtime) - Math.floor(directive.firetime))
                        window.__clock.clockpoint("JavaScript", "AppTools RPC", directive.firetime, [directive.request.api, directive.request.method].join('.'), 100)

                return @

        # consider preinit
        if window.__openfire_preinit?
            @sys.state.preinit = window.__openfire_preinit
            @sys.state.consider_preinit(window.__openfire_preinit)

        # sniff headers/session
        if @sys.state.sniff_headers?(document)

            if @sys.config.session.cookieless
                # append session header
                $.apptools.api.internals.config.headers[@sys.config.csrf.header] = @sys.state.session.signature

                # manually copy over cookie
                $.apptools.api.internals.config.headers[@sys.config.session.header] = document.cookie

        # trigger system ready
        return @sys.go(window)

# bind openfire to window
window.Openfire = Openfire
window.openfire = new Openfire(window)

# if jQuery's around, extend it with openfire
if window.jQuery?
    $.extend openfire: window.openfire

# otherwise, we got this on lock.
else
    if not window.$?
        window.$ = {}
    window.$.openfire = window.openfire
