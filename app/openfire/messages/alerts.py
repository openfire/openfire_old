from protorpc import messages


#### ++++ Object Messages ++++ ####
class ProspectiveQuery(messages.Message):

	''' A registered prospective query. '''

	pass


class AlertSettings(messages.Message):

	''' Settings for alerts based on matches from a prospective query. '''

	pass


class Subscription(messages.Message):

	''' A subscription to a system object. '''

	pass


class Notification(messages.Message):

	''' A notification of a match on a prospective query that is part of a subscription to a system object. '''

	pass


#### ++++ Container Messages ++++ ####
class Subscriptions(messages.Message):

	''' A list of subscriptions. '''

	pass


class Notifications(messages.Message):

	''' A list of notifications. '''

	pass


#### ++++ Request Messages ++++ ####
class SubscriptionRequest(messages.Message):

	''' A request for a subscription, or to unsubscribe, or to edit an existing subscription. '''

	pass


class NotificationsRequest(messages.Message):

	''' A response with containing a list of notifications. '''

	pass
