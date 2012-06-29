## openfire bbq

# Generic function to fulfill an api request on the bbq page.
fulfillRequest = (request, errMsg) ->
    request.fulfill
        success: (obj, objType, rawResponse) ->
            document.location.reload()

        error: (err) ->
            alert 'There was an error: ' + errMsg


## Base object used to centralize common bbq functions.
class BBQBaseObject

    constructor: (el) ->
        _this = this
        @_element = el
        @_dataDict = {}

        this._element.find('button.start-edit').click () ->
            _this._element.find('.save-edit').show()
            _this._element.find('.start-edit').hide()
            _this._element.find('.cancel-edit').show()
            _this._element.find('.editable').each () ->
                $(this).replaceWith('<textarea class="' + this.className + '">' + $(this).html() + '</textarea>')

        this._element.find('button.cancel-edit').click () ->
            _this._element.find('.start-edit').show()
            _this._element.find('.save-edit').hide()
            _this._element.find('.cancel-edit').hide()
            _this._element.find('.editable').each () ->
                $(this).replaceWith('<span class="' + this.className + '">' + $(this).html() + '</span>')

        this._element.find('button.save-edit').click () ->
            _this.put()

        this._element.find('button.delete').click () ->
            _this.delete()

    getAttr: (prefix, name) ->
        this._element.find('.' + prefix + '-' + name).val() or this._element.find('.' + prefix + '-' + name).html()

    loadData: () ->
        for dataName in @dataList
            @_dataDict[dataName] = @getAttr 'category', dataName


class BBQCategory extends BBQBaseObject

    constructor: (el) ->
        @dataList = ['key', 'name', 'slug', 'description']
        super el

    put: () ->
        @loadData()
        request = $.apptools.api.category.put(@_dataDict)
        fulfillRequest(request)

    delete: () ->
        request = $.apptools.api.category.delete(key: @getAttr 'category', 'key')
        fulfillRequest(request)


class BBQProposal extends BBQBaseObject

    constructor: (el) ->
        _this = this
        @dataList = ['key', 'name', 'summary', 'category', 'status', 'pitch', 'tech', 'keywords', 'creator']
        super el
        el.find('button.promote-to-project').click ->
            _this.promote()
        el.find('button.suspend').click ->
            _this.suspend()
        el.find('button.reject').click ->
            _this.reject()

    put: () ->
        @loadData()
        request = $.apptools.api.proposal.put(@_dataDict)
        fulfillRequest(request, "Failed to put a proposal")

    delete: () ->
        request = $.apptools.api.proposal.delete(key: @getAttr 'proposal', 'key')
        fulfillRequest(request, "Failed to delete a proposal")

    promote: () ->
        request = $.apptools.api.proposal.promote(key: @getAttr 'proposal', 'key')
        fulfillRequest(request, "Failed to promote a proposal to a project")

    suspend: () ->
        request = $.apptools.api.proposal.suspend(key: @getAttr 'proposal', 'key')
        fulfillRequest(request, "Failed to suspend a proposal")

    reject: () ->
        request = $.apptools.api.proposal.reject(key: @getAttr 'proposal', 'key')
        fulfillRequest(request, "Failed to reject a proposal")


class BBQProject extends BBQBaseObject

    constructor: (el) ->
        _this = this
        @dataList = ['key', 'name', 'summary', 'category', 'status', 'pitch',
                     'tech', 'keywords', 'creator', 'owners', 'goals', 'tiers']
        super el
        el.find('button.go-live').click ->
            _this.goLive()
        el.find('button.suspend').click ->
            _this.suspend()
        el.find('button.shutdown').click ->
            _this.shutdown()

    put: () ->
        @loadData()
        request = $.apptools.api.project.put(@_dataDict)
        fulfillRequest(request, "Failed to put a project")

    delete: () ->
        request = $.apptools.api.project.delete(key: @getAttr 'project', 'key')
        fulfillRequest(request, "Failed to delete a project")

    goLive: () ->
        request = $.apptools.api.project.go_live(key: @getAttr 'project', 'key')
        fulfillRequest(request, "Failed to send a project live")

    suspend: () ->
        request = $.apptools.api.project.suspend(key: @getAttr 'project', 'key')
        fulfillRequest(request, "Failed to suspend a project")

    shutdown: () ->
        request = $.apptools.api.project.shutdown(key: @getAttr 'project', 'key')
        fulfillRequest(request, "Failed to shut down a project")


class BBQController

    @export = 'private'
    @events = []

    constructor: (openfire, window) ->

        @categories = []
        @proposals = []
        @projects = []
        @customUrls = []

        @_init = () =>
            @initBbqNewInlines()
            @initBbqCategories()


    initBbqCategories: () ->
        _this = this
        $('.category').each () ->
            newCategory = new BBQCategory($(this))
            _this.categories.push newCategory

        $('.proposal').each () ->
            newProposal = new BBQProposal($(this))
            _this.proposals.push newProposal

        $('.project').each () ->
            newProject = new BBQProject($(this))
            _this.projects.push newProject


    initBbqNewInlines: () ->
        _this = this
        $('button.show-new-inline').click ->
            self = $(this)
            self.hide()
            self.next('.inline-form').show()

        $('button.cancel-new-inline').click ->
            self = $(this)
            self.parents('.inline-form').hide()
            self.parents('.inline-form').prev('.show-new-inline').show()

        $('button.save-new-inline').click ->
            reqeust = null
            switch @id
                when 'save-new-category-btn'
                    categoryDict =
                        name: $('#new-category-name-input').val()
                        slug: $('#new-category-url-input').val()
                        description: $('#new-category-description-input').val()
                    request = $.apptools.api.category.put(categoryDict)

                when 'save-new-proposal-btn'
                    proposalDict =
                        name: $('#new-proposal-name-input').val()
                        slug: $('#new-proposal-url-input').val()
                        summary: $('#new-proposal-summary-input').val()
                        category: $('#new-proposal-category-input').val()
                        status: $('#new-proposal-status-input').val()
                        pitch: $('#new-proposal-pitch-input').val()
                        tech: $('#new-proposal-tech-input').val()
                        keywords: $('#new-proposal-keywords-input').val()
                        creator: $('#new-proposal-creator-input').val()
                    request = $.apptools.api.proposal.put(proposalDict)

                else
                    alert 'What button did you just click? (it was ' + @id + ')'

            fulfillRequest request, 'Failed to something.' if request


if @__openfire_preinit?
    @__openfire_preinit.abstract_base_controllers.push(BBQController)
