## openfire propose page.

# TODO: Shoud be using the proposal object instead.
PROPOSAL_PROP_LIST = ['name', 'desired_url', 'summary', 'category', 'pitch', 'tech', 'team']
INITIAL_GOAL_PROP_LIST = ['amount', 'description', 'funding_day_limit', 'deliverable_description', 'deliverable_date']
FUTURE_GOAL_PROP_LIST = ['summary', 'description']

INT_PROP_LIST = ['funding_day_limit']
FLOAT_PROP_LIST = ['amount']
DATE_PROP_LIST = ['deliverable_date']
SELECT_PROP_LIST = ['category']

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

            _.ready(() ->
                if window.jQuery? and jQuery.fn?.smartWizard?
                    if $("#propose-wizard").smartWizard
                        $("#propose-wizard").smartWizard
                            labelFinish: 'Create proposal'
                            onShowStep: onShowStepCb
                            onLeaveStep: onLeaveStepCb
                            onFinish: onFinishCb
            )

        @convertProp = (name, val) =>
            try
                if name in INT_PROP_LIST
                    return parseInt(val)
                else if name in FLOAT_PROP_LIST
                    return parseFloat(val)
                else if name in DATE_PROP_LIST
                    date = new Date(val)
                    return date.toISOString()
            catch err
                console.log('Failed to decode value.')
            return val

        @collectProposeForm = () =>

            for prop in PROPOSAL_PROP_LIST
                propContent = $("#proposal-" + prop).val()
                $("#" + prop + "-summary").html(propContent)
                if prop in SELECT_PROP_LIST
                    propDisplay = $("#proposal-" + prop + " option:selected").html()
                    $("#" + prop + "-summary-display").html(propDisplay)
            for prop in INITIAL_GOAL_PROP_LIST
                propContent = $("#proposal-initial-goal-" + prop).val()
                $("#initial-goal-" + prop + "-summary").html(propContent)
            for prop in FUTURE_GOAL_PROP_LIST
                propContent = $("#proposal-future-goal-" + prop).val()
                $("#future-goal-" + prop + "-summary").html(propContent)


        @buildProposalParams = () =>

            @collectProposeForm()
            proposalParams = {}
            for prop in PROPOSAL_PROP_LIST
                propContent = $("#" + prop + '-summary').html()
                propContent = @convertProp(prop, propContent)
                proposalParams[prop] = propContent

            initialGoalParams = {}
            for prop in INITIAL_GOAL_PROP_LIST
                propContent = $("#initial-goal-" + prop + '-summary').html()
                propContent = @convertProp(prop, propContent)
                initialGoalParams[prop] = propContent
            proposalParams['initial_goal'] = initialGoalParams

            futureGoalParams = {}
            for prop in FUTURE_GOAL_PROP_LIST
                propContent = $("#future-goal-" + prop + '-summary').html()
                propContent = @convertProp(prop, propContent)
                futureGoalParams[prop] = propContent
            proposalParams['future_goal'] = futureGoalParams

            return proposalParams


        @createProposal = () =>
            proposalParams = @buildProposalParams()
            $.apptools.api.proposal.put(proposalParams).fulfill
                success: (obj, objType, rawResponse) ->
                    alert 'Your proposal has been created! You will now be redirected to your new proposal page.'
                    location.href = '/proposal/' + obj.key

                failure: (err) ->
                    alert 'There was an error: ' + err

if @__openfire_preinit?
    @__openfire_preinit.abstract_base_controllers.push(ProposeController)
