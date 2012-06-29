## openfire bbq
class BBQController

    @export = 'private'
    @events = []

    constructor: (openfire, window) ->

        @_init = () =>
            @initBbqInlines()
            return

    initBbqInlines: () ->
        _this = this

        $('.show-new-inline').click ->
            self = $(@)
            self.hide()
            self.next('.inline-form').show()

        $('.cancel-new-inline').click ->
            self = $(@)
            self.parents('.inline-form').hide()
            self.parents('.inline-form').prev('.show-new-inline').show()

        $('.save-new-inline').click ->
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

            _this.fulfillBbqRequest request, 'Failed to something.' if request


        $('.delete-object').click ->
            request = undefined
            toDelete = undefined
            toDelete = @id.match(/delete-(\w+)-(\w+)/)
            request = null
            switch toDelete[1]
                when 'category'
                    request = $.apptools.api.category.delete(slug: toDelete[2])
                when 'proposal'
                    request = $.apptools.api.proposal.delete(slug: toDelete[2])
                else
                    alert 'That failed: (' + toDelete + ')'

            _this.fulfillBbqRequest request, 'Failed to delete ' + toDelete[1]  if request

        $('.start-edit-inline').click ->
            toEdit = @id.match(/start-edit-(\w+)-(\w+)/)
            editType = toEdit[1]
            slug = toEdit[2]
            $('#start-edit-' + editType + '-' + slug).hide()
            $('#save-edit-' + editType + '-' + slug).show()
            $('#cancel-edit-' + editType + '-' + slug).show()
            $('#' + editType + '-display-' + slug).hide()
            $('#' + editType + '-inputs-' + slug).show()

        $('.cancel-edit-inline').click ->
            toEdit = @id.match(/cancel-edit-(\w+)-(\w+)/)
            editType = toEdit[1]
            slug = toEdit[2]
            $('#start-edit-' + editType + '-' + slug).show()
            $('#save-edit-' + editType + '-' + slug).hide()
            $('#cancel-edit-' + editType + '-' + slug).hide()
            $('#' + editType + '-display-' + slug).show()
            $('#' + editType + '-inputs-' + slug).hide()


        $('.save-edit-inline').click ->
            toSave = @id.match(/save-edit-(\w+)-(\w+)/)
            switch toSave[1]
                when 'category'
                    categoryDict =
                        key: $('#category-inputs-' + toSave[2] + ' .slug-input').val()
                        slug: $('#category-inputs-' + toSave[2] + ' .slug-input').val()
                        name: $('#category-inputs-' + toSave[2] + ' .name-input').val()
                        description: $('#category-inputs-' + toSave[2] + ' .description-input').val()

                    request = $.apptools.api.category.put(categoryDict)
                when 'proposal'
                else
                    alert 'What button did you just click? (it was ' + @id + ')'

            _this.fulfillBbqRequest request, 'Failed to edit something.'


    fulfillBbqRequest: (request, errMsg) ->
        request.fulfill
            success: (obj, objType, rawResponse) ->
                document.location.reload()

            error: (err) ->
                alert 'There was an error: ' + errMsg

@__openfire_preinit.abstract_base_controllers.push(BBQController)
