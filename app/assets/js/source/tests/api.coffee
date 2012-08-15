# openfire unit tests for the API framework.

# API tests
describe 'openfire api tests', ->

    OF_APIS =
        category: ['list']
        topic: ['list']
        url: ['list']
        proposal: ['list']
        project: ['list']

    beforeEach ->
        # Nothing to do for now.

    # Test existence of all the APIs in the list.
    it 'should make sure all the apis should exist.', ->
        expect(OF_APIS).toBeDefined()
        expect($.apptools.api).toBeDefined()
        for api_name, api_list of OF_APIS
            expect($.apptools.api[api_name]).toBeDefined()
            for api_method in api_list
                expect($.apptools.api[api_name][api_method]).toBeDefined()


    # Define a function to test the 'list' api method for a given api.
    testAPIList = (api_name) ->
        it 'should return more than 0 results for the ' + api_name + ' list method.', ->
            # Test all the list methods specifically.
            content = undefined
            loaded = false
            failed = false

            # Start an async call.
            runs () ->
                $.apptools.api[api_name].list().fulfill
                    success: (response, responseType, responseContent) =>
                        content = responseContent.response.content
                        loaded = true
                    failure: (error) =>
                        loaded = true
                        failed = true

            waitsFor (->
                return loaded
            ), 'The objects should be loaded from the api', 250

            runs ->
                expect(failed).toBeFalsy()
                expect(content).toBeDefined()
                if api_name is 'category'
                    list = content.categories
                else
                    list = content[api_name + 's']
                if list
                    expect(list.length).toBeGreaterThan 0

    for api_name, api_list of OF_APIS
        if not 'list' in api_list
            continue
        testAPIList(api_name)

