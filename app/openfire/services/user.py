from google.appengine.ext import ndb
from apptools.services.builtin import Echo
from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.models.user import EmailAddress
from openfire.messages import user as user_messages
from openfire.messages import common as common_messages


## User service api.
class UserService(RemoteService):

    @remote.method(user_messages.ProfileRequest, user_messages.Profile)
    def profile(self, request):

        ''' Return profile information for a user, and edit bio and location. '''

        # TODO: Permissions?
        user_key = ndb.Key('User', request.user)
        user = user_key.get()
        if not user:
            # No user found.
            return user_messages.Profile()

        if request.profile:
            # Put the new profile info before returning. Permissions?
            excluded_fields = ['username', 'firstname', 'lastname', 'email', 'topics']
            user.mutate_from_message(request.profile, exclude=excluded_fields)
            user.put()

        response = user.to_message(message_class=user_messages.Profile, exclude=['topics', 'email'])

        # Update the email and topics.
        emails = EmailAddress.query(ancestor=user_key).fetch()
        topics = ndb.get_multi(user.topics)
        response.email = [email.to_message() for email in emails]
        response.topics = [topic.to_message() for topic in topics]

        # Return the new profile info.
        return response


    @remote.method(user_messages.SetTopics, message_types.VoidMessage)
    def set_topics(self, request):

        ''' Set topics for a user to display. '''

        try:
            try:
                ## try pulling by key first
                user_key = ndb.Key(urlsafe=request.user)
            except:
                ## if not, then pull by username
                user_key = ndb.Key('User', request.user)

            finally:
                user = user_key.get(use_cache=True, use_memcache=True, use_datastore=True)
                assert user is not None
        except AssertionError, e:
            raise self.exceptions.ApplicationError('User not found.')

        if not request.topics or len(request.topics) < 1:
            user.topics = []
        else:
            # Make sure all topics exist.
            topic_keys = [ndb.Key(urlsafe=topic) for topic in request.topics]
            all_topics = ndb.get_multi(topic_keys)
            if None in all_topics:
                raise self.exceptions.ApplicationError('Failed to find one or more input topics.')
            user.topics = topic_keys
        user.put()
        return message_types.VoidMessage()


    @remote.method(user_messages.AccountRequest, user_messages.Account)
    def account(self, request):

        ''' Return or edit account information for a user. '''

        return user_messages.Account()


    @remote.method(common_messages.FollowRequest, Echo)
    def follow(self, request):

        ''' Return following success or failure message. '''

        return Echo(message="You are now following someone...or not.")


    @remote.method(common_messages.FollowersRequest, common_messages.FollowersResponse)
    def followers(self, request):

        ''' Return the followers of a user. Returns a list of user profiles. '''

        return common_messages.FollowersResponse()
