# This document contains the openfire javascript unit tests.

# First test!
describe 'openfire apis', ->

    beforeEach ->
        # TODO: How do we initialize all the apis?

    it 'all the apis should exist.', ->
        alert 'How do we initialize the apis?'
        expect($.apptools.api).toBeDefined
        expect($.apptools.api.category).toBeDefined
        expect($.apptools.api.category.list).toBeDefined

    it 'should list all the categories', ->
        $.apptools.api.category.list().fulfil
            success: (response) =>
                expect(response).toBeDefined
                expect(response.categories.length).toBeGreaterThan 0
            failure: (error) =>
                expect(true).toBeFalsy
