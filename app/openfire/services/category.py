from google.appengine.ext import ndb
from apptools.services.builtin import Echo
from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.messages import common as common_messages
from openfire.models.project import Category


class CategoryService(RemoteService):

    ''' Category service api. '''

    @remote.method(common_messages.CategoryRequest, common_messages.Category)
    def get(self, request):

        ''' Get a single category. '''

        category_key = ndb.Key('Category', request.slug)
        category = category_key.get()
        return category.to_message()


    @remote.method(message_types.VoidMessage, common_messages.Categories)
    def list(self, request):

        ''' Return a list of categories. '''

        categories = Category.query().fetch()
        messages = []
        for category in categories:
            messages.append(category.to_message())
        return common_messages.Categories(categories=messages)


    @remote.method(common_messages.Category, common_messages.Category)
    def put(self, request):

        ''' Create or edit a category. '''

        if not request.key:
            # Create a new category.
            category = Category(key=ndb.Key('Category', request.slug))
        else:
            # Get the category to edit.
            category_key = ndb.Key('Category', request.key)
            category = category_key.get()

        if not category:
            # TODO: What to do on error?
            return common_messages.Category()

        # Update the category.
        category.mutate_from_message(request)
        category.put()

        return category.to_message()


    @remote.method(common_messages.CategoryRequest, Echo)
    def delete(self, request):

        ''' Remove a category. '''

        category_key = ndb.Key('Category', request.slug)
        category_key.delete()
        return Echo(message='Category removed')
