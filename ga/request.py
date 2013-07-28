__author__ = 'minhtule'

from ga.parameter import *
from labgoo.lb_logging import lb_logger


class HTTPRequest(object):
    """

    """

    HOST = "http://www.google-analytics.com/collect"

    def __init__(self, tracker, hit_type, other_parameters):
        self.__tracker = tracker
        self.__params = []
        self.__params.append(ProtocolVersion())  # Protocol Version
        self.__params.append(tracker.tracking_id)  # Tracking ID
        self.__params.append(tracker.client_id)  # Client ID
        self.__params.append(hit_type)  # Hit type
        self.__params.extend(other_parameters)

    def send(self):
        data_payload = self.__build_data_payload()
        result = urllib.urlopen(self.HOST, data_payload)

        lb_logger.debug(data_payload)
        lb_logger.debug(result.code)

        if result.code == 200:
            return True
        return False

    def __build_data_payload(self):
        return "&".join([param.url_format() for param in self.__params])


class PageTrackingRequest(HTTPRequest):
    PAGE_TRACKING_HIT_TYPE = HitType("pageview")

    def __init__(self, tracker, document_hostname=None, document_path=None, document_title=None):
        other_params = []
        createAndAppendParameter(other_params, DocumentHostName, document_hostname, is_required=False)
        createAndAppendParameter(other_params, DocumentPath, document_path, is_required=False)
        createAndAppendParameter(other_params, DocumentTitle, document_title, is_required=False)
        super(PageTrackingRequest, self).__init__(tracker, self.PAGE_TRACKING_HIT_TYPE, other_params)


class EventTrackingRequest(HTTPRequest):
    EVENT_TRACKING_HIT_TYPE = HitType("event")

    def __init__(self, tracker, category, action, label=None, value=None):
        other_params = []
        createAndAppendParameter(other_params, EventCategory, category, is_required=True)
        createAndAppendParameter(other_params, EventAction, action, is_required=True)
        createAndAppendParameter(other_params, EventLabel, label, is_required=False)
        createAndAppendParameter(other_params, EventValue, value, is_required=False)
        super(EventTrackingRequest, self).__init__(tracker, self.EVENT_TRACKING_HIT_TYPE, other_params)


def createAndAppendParameter(parameters, parameter_creator_func, value, is_required=False):
        if is_required or value is not None:
            param = parameter_creator_func(value)
            parameters.append(param)

