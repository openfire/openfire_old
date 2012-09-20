## openfire bbq

# Generic function to fulfill an api request on the bbq page.
fulfillRequest = (request, errMsg) ->
    request.fulfill
        success: (obj, objType, rawResponse) ->
            window.location.reload()

        error: (err) ->
            alert 'There was an error: ' + errMsg


## Base object used to centralize common bbq functions.
class BBQBaseObject

    constructor: (el) ->
        _this = this
        @_element = el
        @_dataDict = {}

        """
        this._element.find('button.start-edit').click () ->
            _this._element.find('.save-edit').show()
            _this._element.find('.start-edit').hide()
            _this._element.find('.cancel-edit').show()
            _this._element.find('.bbq-editable').each () ->
                $(this).replaceWith('<textarea class="' + this.className + '">' + $(this).html() + '</textarea>')

        this._element.find('button.cancel-edit').click () ->
            _this._element.find('.start-edit').show()
            _this._element.find('.save-edit').hide()
            _this._element.find('.cancel-edit').hide()
            _this._element.find('.bbq-editable').each () ->
                $(this).replaceWith('<span class="' + this.className + '">' + $(this).html() + '</span>')

        this._element.find('button.save-edit').click () ->
            _this.put()

        this._element.find('button.delete').click () ->
            _this.delete()
        """

    getAttr: (prefix, name) ->
        return "TODO: Need _element.find()!"
        #return this._element.find('.' + prefix + '-' + name).val() or this._element.find('.' + prefix + '-' + name).html()

    loadData: () ->
        for dataName in @dataList
            @_dataDict[dataName] = @getAttr @dataPrefix, dataName


class BBQCategory extends BBQBaseObject

    constructor: (el) ->
        @dataList = ['key', 'name', 'slug', 'description']
        @dataPrefix = 'category'
        super el
        @categoryKey = @getAttr('category', 'key')

    put: () ->
        @loadData()
        request = $.apptools.api.category.put(@_dataDict)
        fulfillRequest(request)

    delete: () ->
        request = $.apptools.api.category.delete(key: @categoryKey)
        fulfillRequest(request)

    '''
    COMING SOON: DIALOGS!
    startEdit: () ->
        for modal in $.apptools.widgets.modal._state.modals
            if modal._state.cached_id == 'new-category'
                modal.open()
                this._element.find('button.save-edit').click () ->
                    _this.put()
    '''


class BBQProposal extends BBQBaseObject

    constructor: (el) ->
        _this = this
        @dataList = ['key', 'name', 'summary', 'category', 'status', 'pitch', 'tech', 'keywords', 'creator']
        @dataPrefix = 'proposal'
        super el
        @proposalKey = @getAttr 'proposal', 'key'

        """
        TODO: Need el.find()!
        el.find('button.promote-to-project').click ->
            _this.promote()
        el.find('button.suspend').click ->
            _this.suspend()
        el.find('button.reject').click ->
            _this.reject()
        """

    put: () ->
        @loadData()
        request = $.apptools.api.proposal.put(@_dataDict)
        fulfillRequest(request, "Failed to put a proposal")

    delete: () ->
        request = $.apptools.api.proposal.delete(key: @proposalKey)
        fulfillRequest(request, "Failed to delete a proposal")

    promote: () ->
        request = $.apptools.api.proposal.promote(key: @proposalKey)
        fulfillRequest(request, "Failed to promote a proposal to a project")

    suspend: () ->
        request = $.apptools.api.proposal.suspend(key: @proposalKey)
        fulfillRequest(request, "Failed to suspend a proposal")

    reject: () ->
        request = $.apptools.api.proposal.reject(key: @proposalKey)
        fulfillRequest(request, "Failed to reject a proposal")


class BBQProject extends BBQBaseObject

    constructor: (el) ->
        _this = this
        @dataList = ['key', 'name', 'summary', 'category', 'status', 'pitch',
                     'tech', 'keywords', 'creator', 'owners', 'goals', 'tiers']
        @dataPrefix = 'project'
        super el
        @projectKey = @getAttr('project', 'key')

        """
        TODO: Need el.find()!
        el.find('button.go-live').click ->
            _this.goLive()
        el.find('button.suspend').click ->
            _this.suspend()
        el.find('button.shutdown').click ->
            _this.shutdown()

        document.getElementById('project-' + @projectKey + '-image').addEventListener('drop', @uploadImage, false)
        document.getElementById('project-' + @projectKey + '-avatar').addEventListener('drop', @uploadAvatar, false)
        document.getElementById('add-project-' + @projectKey + '-video').addEventListener('click', @addVideo, false)
        """

    uploadImage: (e) =>
        e.preventDefault()
        e.stopPropagation()

        file = e.dataTransfer.files[0]

        $.apptools.api.media.attach_image(
            intake: 'UPLOAD'
            name: file.name
            size: file.size
            target: @projectKey
        ).fulfill
            success: (response) =>
                uploader = $.apptools.widgets.uploader.create 'array',
                    endpoints: [response.endpoint]
                    finish: (response) =>
                        ethan = 1
                        # TODO: Something with the response
                        #@project.attach(new Image(response.media_key, response.serve_url))
                        #$.apptools.events.trigger 'PROJECT_MEDIA_ADDED', @
                uploader.upload(file)
            failure: (error) =>
                alert 'Failed to attach an image.'


    uploadAvatar: (e) =>
        e.preventDefault()
        e.stopPropagation()

        file = e.dataTransfer.files[0]

        $.apptools.api.media.attach_avatar(
            intake: 'UPLOAD'
            name: file.name
            size: file.size
            target: @projectKey
        ).fulfill
            success: (response) =>
                uploader = $.apptools.widgets.uploader.create 'array',
                    endpoints: [response.endpoint]
                    finish: (response) =>
                        ethan = 1
                        # TODO: Something with the response
                        #@project.attach(new Image(response.media_key, response.serve_url))
                        #$.apptools.events.trigger 'PROJECT_MEDIA_ADDED', @
                uploader.upload(file)
            failure: (error) =>
                alert 'Failed to attach an avatar.'


    addVideo: (e) =>
        provider = $(e.currentTarget).siblings('[name="provider"]:checked').val()
        url = $(e.currentTarget).siblings('[name="video-url"]').val()

        $.apptools.api.media.attach_video(
            target: @projectKey
            provider: provider
            reference: url
        ).fulfill
            success: (response) =>
                alert 'Video attached.'
            failure: (error) =>
                alert 'Failed to attach a video.'

    put: () ->
        @loadData()
        request = $.apptools.api.project.put(@_dataDict)
        fulfillRequest(request, "Failed to put a project")

    delete: () ->
        request = $.apptools.api.project.delete(key: @projectKey)
        fulfillRequest(request, "Failed to delete a project")

    goLive: () ->
        request = $.apptools.api.project.go_live(key: @projectKey)
        fulfillRequest(request, "Failed to send a project live")

    suspend: () ->
        request = $.apptools.api.project.suspend(key: @projectKey)
        fulfillRequest(request, "Failed to suspend a project")

    shutdown: () ->
        request = $.apptools.api.project.shutdown(key: @projectKey)
        fulfillRequest(request, "Failed to shut down a project")


class BBQCustomUrl extends BBQBaseObject

    constructor: (el) ->
        @dataList = ['key', 'slug', 'target']
        @dataPrefix = 'custom-url'
        super el
        @customURLKey = @getAttr 'custom-url', 'key'

    put: () ->
        request = $.apptools.api.url.delete(key: @customURLKey)
        fulfillRequest(request)

    delete: () ->
        request = $.apptools.api.url.delete(key: @customURLKey)
        fulfillRequest(request)


class BBQController

    @export = 'private'
    @events = []

    constructor: (openfire, window) ->

        @categories = []
        @proposals = []
        @projects = []
        @customUrls = []

        @_init = () =>
            $(document).ready ->
                if $('.bbq-datatable')?.length
                    $('.bbq-datatable').dataTable()
                    @initBbqNewInlines()
                    @initBbqObjects()


    initBbqObjects: () ->
        _this = this
        $('.category').each () ->
            newCategory = new BBQCategory($(this))
            _this.categories.push newCategory

        $('.proposal').each () ->
            newProposal = new BBQProposal($(this))
            _this.proposals.push newProposal

        $('#start-add-new-category').click (e) ->
            self = $(this)
            self.hide()
            self.next('.dialog-form').show()

        $('.project').each () ->
            newProject = new BBQProject($(this))
            _this.projects.push newProject

        $('.custom-url').each () ->
            newCustomUrl = new BBQCustomUrl($(this))
            _this.customUrls.push newCustomUrl


    initBbqNewInlines: () ->
        _this = this

        $('button.cancel-new-dialog').click ->
            $.apptools.widgets.modal.get('new-category-dialog')?.close()
            $.apptools.widgets.modal.get('new-proposal-dialog')?.close()
            $.apptools.widgets.modal.get('new-custom-url-dialog')?.close()

        $('button.save-new-dialog').click ->
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

                when 'save-new-custom-url-btn'
                    customUrlDict =
                        slug: $('#new-custom-url-slug-input').val()
                        target: $('#new-custom-url-target-input').val()
                    request = $.apptools.api.url.put(customUrlDict)

                else
                    alert 'What button did you just click? (it was ' + @id + ')'

            fulfillRequest request, 'Failed to something.' if request


if @__openfire_preinit?
    @__openfire_preinit.abstract_base_objects.push BBQBaseObject, BBQCategory, BBQProposal, BBQProject, BBQCustomUrl
    @__openfire_preinit.abstract_base_classes.push BBQController
    @__openfire_preinit.abstract_base_controllers.push BBQController
