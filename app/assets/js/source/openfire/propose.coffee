## openfire propose page.

PROP_LIST = ['name', 'url', 'summary', 'category', 'pitch', 'first-goal', 'last-goal', 'tech', 'team']

class ProposeController

    @export = 'private'
    @events = []

    constructor: (openfire, window) ->

        @_init = () =>

            onShowStepCb = (obj) =>
                stepnumber = obj.attr('rel')

                if stepnumber == '4'
                    @collectProposeForm()

                return true

            onLeaveStepCb = (obj) =>
                stepnumber = obj.attr('rel')
                return true

            onFinishCb = (obj) =>
                @collectProposeForm()
                @createProposal()

            $(document).ready ->
                $("#propose-wizard").smartWizard
                    labelFinish: 'Create proposal'
                    onShowStep: onShowStepCb
                    onLeaveStep: onLeaveStepCb
                    onFinish: onFinishCb

        @createProposal = () =>
            @collectProposeForm()
            proposalParams = {}
            for prop in PROP_LIST
                propContent = $("#" + prop + '-summary').html()
                proposalParams[prop] = propContent
            $.apptools.api.proposal.put(proposalParams).fulfill
                success: (obj, objType, rawResponse) ->
                    alert 'Your proposal has been created! You will now be redirected to your new proposal page.'
                    location.href = '/proposal/' + obj.key

                error: (err) ->
                    alert 'There was an error: ' + err


        @collectProposeForm = () =>

            for prop in PROP_LIST
                propContent = $("#proposal-" + prop).val()
                $("#" + prop + "-summary").html(propContent)


if @__openfire_preinit?
    @__openfire_preinit.abstract_base_controllers.push(ProposeController)
