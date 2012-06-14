from protorpc import remote
from protorpc import message_types

from openfire.messages import alerts
from openfire.services import RemoteService


class AlertsService(RemoteService):

	''' Service for managing matcher/prospective alerts. '''

	@remote.method(alerts.SubscriptionRequest, alerts.Subscription)
	def subscribe(self, request):

		''' Subscribe to alerts for something. '''

		pass

	@remote.method(alerts.SubscriptionRequest, message_types.VoidMessage)
	def unsubscribe(self, request):

		''' Unsubscribe from alerts for something. '''

		pass

	@remote.method(alerts.SubscriptionRequest, alerts.Subscription)
	def edit(self, request):

		''' Edit an existing subscription's query or settings. '''

		pass

	@remote.method(alerts.SubscriptionsRequest, alerts.Subscriptions)
	def subscriptions(self, request):

		''' Retrieve a list of existing subscriptions. '''

		pass

	@remote.method(alerts.NotificationsRequest, alerts.Notifications)
	def pending(self, request):
		
		''' Retrieve only unread notifications. '''

		pass

	@remote.method(alerts.NotificationsRequest, alerts.Notifications)
	def all(self, request):

		''' Retrieve all notifications, regardless of status. '''

		pass
