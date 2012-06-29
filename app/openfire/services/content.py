import hashlib
from protorpc import remote
from apptools.services import RequestError
from openfire.services import RemoteService
from openfire.models.content import ContentSnippet
from openfire.messages import content as messages


class SnippetNotFoundError(RequestError):
    pass


## Content service api.
#
class ContentService(RemoteService):

    ''' Server-side backend for content management features. '''

    @remote.method(messages.SaveContentRequest, messages.ContentResponse)
    def save_snippet(self, request):

        ''' Save a new version of a content snippet. '''

        if request.snippet_keyname is not None:
            self.api.memcache.delete('Snippet//' + hashlib.sha256(request.snippet_keyname).hexdigest())

        if request.snippet_key is not None:
            self.api.memcache.delete('Snippet//' + hashlib.sha256(request.snippet_key).hexdigest())

        snippet = ContentSnippet(key=self.api.ndb.Key('ContentSnippet', request.snippet_keyname),
                    content=request.inner_html)
        snippet.put()

        if snippet.key.string_id() is not None:
            self.api.memcache.set('Snippet//' + hashlib.sha256(snippet.key.string_id()).hexdigest(), snippet.content)
        self.api.memcache.set('Snippet//' + hashlib.sha256(snippet.key.urlsafe()).hexdigest(), snippet.content)

        return messages.ContentResponse(snippet_key=str(snippet.key.urlsafe()),
                    snippet_keyname=str(snippet.key.string_id()), inner_html=request.inner_html)


    @remote.method(messages.GetContentRequest, messages.ContentResponse)
    def get_snippet(self, request):

        ''' Retrieve a named or keyed snippet. '''

        if request.snippet_keyname is not None:
            snippet = ContentSnippet.get_by_key_name(request.snippet_keyname)
        else:
            snippet = ContentSnippet.get(self.api.db.Key(request.snippet_key))

        if snippet is not None:
            return messages.ContentResponse(snippet_key=str(snippet.key()), snippet_keyname=snippet.key().name(),
                        inner_html=snippet.content)
        else:
            raise SnippetNotFoundError('Could not resolve snippet.')
