## openfire project classes & controllers

# base project object
class Project extends OpenfireObject


# base proposal object
class Proposal extends OpenfireObject


# project controller
class ProjectController extends OpenfireController

    @key = null
    @events = []

    constructor: (openfire, window) ->

        @_init = () =>

            $('#back').click(@action.back)
            $('#follow').click(@action.follow)
            $('.sharebutton').click(@action.share)

            return

        @action =
            follow: (event) =>

                event.preventDefault()
                event.stopPropagation()

                $.apptools.dev.verbose('project:action', 'User requested to FOLLOW this project.', event)

                ## follow a project
                $.apptools.api.project.follow().fulfill({

                    success: () =>
                        alert 'Success.'

                    failure: () =>
                        alert 'Failure.'

                })

            share: (event) =>

                event.preventDefault()
                event.stopPropagation()

                $.apptools.dev.verbose('project:action', 'User requested to SHARE this project.', event)

                ## share a project
                $.apptools.api.project.share().fulfill({

                    success: () =>
                        alert 'Success.'

                    failure: () =>
                        alert 'Failure.'

                })

            back: (event) =>

                event.preventDefault()
                event.stopPropagation()

                $.apptools.dev.verbose('project:action', 'User requested to BACK this project.', event)

                ## back a project
                $.apptools.api.project.back().fulfill({

                    success: () =>
                        alert 'Success.'

                    failure: () =>
                        alert 'Failure.'

                })


# proposal controller
class ProposalController extends OpenfireController

    @events = []

    constructor: (openfire, window) ->

        @_init = () =>
            return


if @__openfire_preinit?
    @__openfire_preinit.abstract_base_objects.push(Project)
    @__openfire_preinit.abstract_base_objects.push(Proposal)
    @__openfire_preinit.abstract_base_controllers.push(ProjectController)
    @__openfire_preinit.abstract_base_controllers.push(ProposalController)
