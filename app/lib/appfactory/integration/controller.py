import config
import webapp2

from appfactory.integration.abstract import CommandBus


class ControllerBus(CommandBus):
	pass


IntegrationBridge = ControllerBus()
