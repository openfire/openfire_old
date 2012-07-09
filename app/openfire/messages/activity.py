from protorpc import messages


#### ++++ Object Messages ++++ ####
class Activity(messages.Message):

    ''' A single activity object. '''

    pass


class ActivityStream(messages.Message):

    ''' A set of activity objects for a given target and timeperiod. '''

    pass


#### ++++ Request/Response Messages ++++ ####
class SiteMetricsRequest(messages.Message):

    ''' A request for any of the site metrics that we provide. '''

    pass


class SiteMetricsResponse(messages.Message):

    ''' A response with for any of the site metrics that we provide. '''

    pass


class KnownBackersRequest(messages.Message):

    ''' A request for known backers. '''

    pass


class KnownBackersResponse(messages.Message):

    ''' A response for known backers. '''

    pass


class KnownFollowersRequest(messages.Message):

    ''' A request for known followers. '''

    pass


class KnownFollowersResponse(messages.Message):

    ''' A response for known followers. '''

    pass


