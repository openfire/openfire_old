from apptools.services.builtin import Echo
from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.messages import user, common


## User service api.
class UserService(RemoteService):

    @remote.method(user.ProfileRequest, user.Profile)
    def profile(self, request):

        ''' Return or edit profile information for a user '''

        return user.Profile()


    @remote.method(user.AccountRequest, user.Account)
    def account(self, request):

        ''' Return or edit account information for a user. '''

        return user.Account()


    @remote.method(common.FollowRequest, Echo)
    def follow(self, request):

        ''' Return following success or failure message. '''

        return Echo(message="You are now following someone...or not.")


    @remote.method(common.FollowersRequest, common.FollowersResponse)
    def followers(self, request):

        ''' Return the followers of a user. Returns a list of user profiles. '''

        return common.FollowersResponse()
