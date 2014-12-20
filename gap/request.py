__author__ = 'minhtule'

from parameter import *
import urllib2
import logging
import utility


def append_parameter(parameters, parameter_creator_func, value, is_required=False):
    if is_required or value is not None:
        param = parameter_creator_func(value)
        parameters.append(param)


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
        append_parameter(self.__params, UserLanguage, tracker.original_request_language)
        self.__params.extend(other_parameters)

    def add_custom_dimension(self, index, value):
        self.__params.append(CustomDimension(CustomDimension.key_for_index(index), value))

    def add_custom_metric(self, index, value):
        self.__params.append(CustomMetric(CustomMetric.key_for_index(index), value))

    def send(self):
        request = urllib2.Request(self.GOOGLE_ANALYTICS_HOST,
                                  origin_req_host=self.__tracker.original_request_ip)
        request.add_header("User-Agent", self.__tracker.original_request_user_agent)

        data_payload = self.__build_data_payload()
        request.add_data(data_payload)

        result = urllib2.urlopen(request)

        logging.debug(LOGGING_PREFIX + data_payload)

        if result.code == 200:
            return True
        else:
            logging.error(LOGGING_PREFIX + "Request to GA server failed with code " + result.code)
            return False

    def __build_data_payload(self):
        return "&".join([param.url_format() for param in self.__params])


class PageTrackingRequest(HTTPRequest):
    PAGE_TRACKING_HIT_TYPE = "pageview"

    def __init__(self, tracker, document_hostname=None, document_path=None, document_title=None):
        other_params = []
        append_parameter(other_params, DocumentHostName, document_hostname, is_required=False)
        append_parameter(other_params, DocumentPath, document_path, is_required=False)
        append_parameter(other_params, DocumentTitle, document_title, is_required=False)
        super(PageTrackingRequest, self).__init__(tracker, self.PAGE_TRACKING_HIT_TYPE, other_params)


class EventTrackingRequest(HTTPRequest):
    EVENT_TRACKING_HIT_TYPE = "event"

    def __init__(self, tracker, category, action, label=None, value=None):
        other_params = []
        append_parameter(other_params, EventCategory, category, is_required=True)
        append_parameter(other_params, EventAction, action, is_required=True)
        append_parameter(other_params, EventLabel, label, is_required=False)
        append_parameter(other_params, EventValue, value, is_required=False)

        super(EventTrackingRequest, self).__init__(tracker, self.EVENT_TRACKING_HIT_TYPE, other_params)


class TransactionTrackingRequest(HTTPRequest):
    TRANSACTION_TRACKING_HIT_TYPE = 'transaction'

    def __init__(self, tracker, transaction_id, transaction_affiliation=None, transaction_revenue=None, transaction_shipping=None, transaction_tax=None, currency_code=None):
        other_params = []

        append_parameter(other_params, TransactionID, transaction_id, is_required=True)
        append_parameter(other_params, TransactionAffiliation, transaction_affiliation, is_required=False)
        append_parameter(other_params, TransactionRevenue, transaction_revenue, is_required=False)
        append_parameter(other_params, TransactionShipping, transaction_shipping, is_required=False)
        append_parameter(other_params, TransactionTax, transaction_tax, is_required=False)
        append_parameter(other_params, CurrencyCode, currency_code, is_required=False)

        super(TransactionTrackingRequest, self).__init__(tracker, self.TRANSACTION_TRACKING_HIT_TYPE, other_params)


class ItemTrackingRequest(HTTPRequest):
    ITEM_TRACKING_HIT_TYPE = 'item'

    def __init__(self, tracker, transaction_id, item_name, item_price=None, item_quantity=None, item_code=None, item_category=None, currency_code=None):
        other_params = []

        append_parameter(other_params, TransactionID, transaction_id, is_required=True)
        append_parameter(other_params, ItemName, item_name, is_required=True)
        append_parameter(other_params, ItemPrice, item_price, is_required=False)
        append_parameter(other_params, ItemQuantity, item_quantity, is_required=False)
        append_parameter(other_params, ItemCode, item_code, is_required=False)
        append_parameter(other_params, ItemCategory, item_category, is_required=False)
        append_parameter(other_params, CurrencyCode, currency_code, is_required=False)

        super(ItemTrackingRequest, self).__init__(tracker, self.ITEM_TRACKING_HIT_TYPE, other_params)
