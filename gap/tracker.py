__author__ = 'minhtule'

from request import *


class Tracker(object):
    """

    """

    def __init__(self, tracking_id, visitor):
        self.__tracking_id = tracking_id
        self.__visitor = visitor
        self.__debug_enabled = False

    @property
    def tracking_id(self):
        return self.__tracking_id

    @property
    def client_id(self):
        return self.__visitor.id

    @property
    def visitor(self):
        return self.__visitor

    @property
    def debug_enabled(self):
        return self.__debug_enabled

    @debug_enabled.setter
    def debug_enabled(self, value):
        self.__debug_enabled = value

    @property
    def original_request_ip(self):
        return self.visitor.ip_address

    @property
    def original_request_user_agent(self):
        return self.visitor.user_agent

    @property
    def original_request_language(self):
        return self.visitor.language

    # Public method
    def sendPage(self, hostname=None, path=None, title=None):
        if hostname is None:
            hostname = self.visitor.document_host
        if path is None:
            path = self.visitor.document_path

        request = PageTrackingRequest(self, hostname, path, title)
        request.send()

    def sendEvent(self, category, action, label=None, value=None, custom_dimensions=None, custom_metrics=None):
        custom_dimensions = custom_dimensions or []
        custom_metrics = custom_metrics or []

        request = EventTrackingRequest(self, category, action, label, value)

        for custom_dimension in custom_dimensions:
            request.add_custom_dimension(custom_dimension.index, custom_dimension.value)

        for custom_metric in custom_metrics:
            request.add_custom_metric(custom_metric.index, custom_metric.value)

        request.send()