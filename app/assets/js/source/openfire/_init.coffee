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

            # internal state
            state:

                status: 'NOT_READY' # System status
                flags: []           # System flags
                preinit: {}         # System preinit
                controllers: {}     # Installed system controllers
                classes: {}         # Installed openfire-related classes
                objects: {}         # Installed openfire-related objects
                session:            # Runtime session info
                    established: false
                    authenticated: false
                    csrf:
                        next: null
                        history: []

                consider_preinit: (preinit) =>

                    # first consider base objects
                    if preinit.abstract_base_objects?
                        @sys.install.object(obj) for obj in preinit.abstract_base_objects?

                    # next classes
                    if preinit.abstract_base_classes?
                        @sys.install.class(cls) for cls in preinit.abstract_base_classes

                    # then controllers
                    if preinit.abstract_base_controllers?
                        @sys.install.controller(ctrlr) for ctrlr in preinit.abstract_base_controllers

                    return preinit  # preinit HANDLED.

            sniff_headers: (document) =>

                # only lookin' for cookies right now
                session = null
                for i, cookie of document.cookie.split(";")
                    cookie = cookie.split("=");
                    if cookie[0] == @sys.config.session.cookie
                        session = cookie[1].split("|")
                        if session.length > 2  # must be at least 3 (data|timestamp|hash), could sometimes come through as (data|timestamp|hash|csrf)
                            if (@sys.config.session.timeout * 1000) > +new Date()  # check expiration
                                session = cookie[2]
                        break
                    continue

                if session isnt null and session isnt false
                    @sys.state.session.established = true


            install:
                # installs an openfire base object
                object: (obj) =>
                    # stash for future queries
                    @sys.state.objects[(o=obj.constructor.name)] = obj

                    # register any object events
                    if obj.events?
                        window.apptools?.events?.register(event) for event in obj.events

                    # instantiate and bind to window, if obj isn't private
                    if obj.export? isnt 'private' then (obj = new obj(@)) and window[o] = obj else obj = new obj()

                    # lastly init, if it needs it
                    obj._init?()

                    return obj

                # installs an openfire base class
                class: (cls) =>
                    @sys.state.classes[(cl=cls.constructor.name)] = cls
                    if cls.events?
                        window.apptools?.events?.register(event) for event in cls.events
                    if cls.export? isnt 'private' then (cls = new cls(@)) and window[cl] = cls else cls = new cls()
                    cls._init?()

                    return cls

                # installs an openfire controller
                controller: (ctrlr) =>
                    @sys.state.controllers[(c=ctrlr.constructor.name)] = ctrlr
                    if ctrlr.events?
                        window.apptools?.events?.register(event) for event in ctrlr.events
                    if ctrlr.export? isnt 'private' then (ctrlr = new ctrlr(@, window)) and window[c] = ctrlr else ctrlr = new ctrlr(window)
                    ctrlr._init?()

                    return ctrlr


            go: () =>
                # oh snap it's go time
                window.apptools?.dev?.verbose 'Openfire', 'Openfire systems go.'
                @sys.state.status = 'READY'
                return @

        # consider preinit
        if window.__openfire_preinit?
            @sys.state.preinit = window.__openfire_preinit
            @sys.state.consider_preinit(window.__openfire_preinit)

        # sniff headers/session
        session = @sys.sniff_headers(document)

        # trigger system ready
        return @sys.go()

# bind openfire to window
window.Openfire = Openfire
window.openfire = new Openfire(window)

# if jQuery's around, extend it with openfire
if $?
    $.extend openfire: window.openfire

# otherwise, we got this on lock.
else

    window.$ = (id) -> if window.Util? then window.Util.get(id) else document.getElementById(id)
    window.$.openfire = window.openfire
