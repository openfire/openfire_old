from protorpc import message_types, remote
from openfire.services import RemoteService
from openfire.messages import activity as activity_messages


## Activity service api.
#
class ActivityService(RemoteService):

    @remote.method(activity_messages.SiteMetricsRequest, activity_messages.SiteMetricsResponse)
    def site_metrics(self, request):

        ''' Return the requested site metrics. '''

        return activity_messages.SiteMetricsResponse()


    @remote.method(activity_messages.KnownBackersRequest, activity_messages.KnownBackersResponse)
    def known_backers(self, request):

        ''' Return known backers site-wide or for a specific project. '''

        return activity_messages.KnownBackersResponse()


    @remote.method(activity_messages.KnownFollowersRequest, activity_messages.KnownFollowersResponse)
    def known_followers(self, request):

        ''' Return known followers site-wide or for a specific project. '''

        return activity_messages.KnownFollowersResponse()
