## openfire user controllers
class UserController extends OpenfireController

    @events = []

    constructor: (openfire, window) ->

	    @_init = () =>
	        return

	    return

if @__openfire_preinit?
	@__openfire_preinit.abstract_base_controllers.push(UserController)
