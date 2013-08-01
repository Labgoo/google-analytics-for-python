__author__ = 'minhtule'

from parameter import *
from utility import gap_logger
import urllib2


class HTTPRequest(object):
    """

    """

    GOOGLE_ANALYTICS_HOST = "http://www.google-analytics.com/collect"

    def __init__(self, tracker, hit_type, other_parameters):
        self.__tracker = tracker
        self.__params = []
        self.__params.append(ProtocolVersion())  # Protocol Version
        self.__params.append(TrackingID(tracker.tracking_id))  # Tracking ID
        self.__params.append(ClientID(tracker.client_id))  # Client ID
        self.__params.append(HitType(hit_type))  # Hit type
        self.__params.append(CacheBuster())  # Cache Buster, random number to clear cache
        createAndAppendParameter(self.__params, UserLanguage, tracker.original_request_language)
        self.__params.extend(other_parameters)

    def send(self):
        request = urllib2.Request(self.GOOGLE_ANALYTICS_HOST,
                                  origin_req_host=self.__tracker.original_request_ip)
        request.add_header("User-Agent", self.__tracker.original_request_user_agent)

        data_payload = self.__build_data_payload()
        request.add_data(data_payload)

        result = urllib2.urlopen(request)

        gap_logger.debug(data_payload)
        gap_logger.debug(result.code)

        if result.code == 200:
            return True
        return False

    def __build_data_payload(self):
        return "&".join([param.url_format() for param in self.__params])


class PageTrackingRequest(HTTPRequest):
    PAGE_TRACKING_HIT_TYPE = "pageview"

    def __init__(self, tracker, document_hostname=None, document_path=None, document_title=None):
        other_params = []
        createAndAppendParameter(other_params, DocumentHostName, document_hostname, is_required=False)
        createAndAppendParameter(other_params, DocumentPath, document_path, is_required=False)
        createAndAppendParameter(other_params, DocumentTitle, document_title, is_required=False)
        super(PageTrackingRequest, self).__init__(tracker, self.PAGE_TRACKING_HIT_TYPE, other_params)


class EventTrackingRequest(HTTPRequest):
    EVENT_TRACKING_HIT_TYPE = "event"

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

