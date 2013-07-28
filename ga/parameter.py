__author__ = 'minhtule'

from ga.exception import ValidateException
from ga.utility import *
import re
import urllib
import random
import sys

REGEX_OBJECT_TYPE = type(re.compile(""))


class Parameter(object):
    """Parameter of http request specified by Google Analytics

    Details at https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters

    """

    VALUE_TYPE_TEXT = "text"
    VALUE_TYPE_CURRENCY = "currency"
    VALUE_TYPE_BOOLEAN = "boolean"
    VALUE_TYPE_INTEGER = "integer"

    def __init__(self, key, value, value_type, is_required=False, max_length=None,
                 valid_key_pattern=None, valid_value_pattern=None, valid_values=None):
        self.__key = key
        self.__value = value
        self.__value_type = value_type
        self.__is_required = is_required
        self.__max_length = max_length
        self.__valid_key_pattern = valid_key_pattern
        self.__valid_value_pattern = valid_value_pattern
        self.__valid_values = valid_values
        self.validate_key()
        self.validate_value()

        # boolean values are internally stored as 0 or 1
        if self.__value_type == self.VALUE_TYPE_BOOLEAN:
            self.__value = int(self.__value)

    @property
    def key(self):
        return self.__key

    @property
    def value(self):
        return self.__value

    @property
    def value_type(self):
        return self.__value_type

    @property
    def is_required(self):
        return self.__is_required

    @property
    def max_length(self):
        return self.__max_length

    @property
    def valid_key_pattern(self):
        return self.__valid_key_pattern

    @property
    def valid_value_pattern(self):
        return self.__valid_value_pattern

    @property
    def valid_values(self):
        return self.__valid_values

    def __str__(self):
        return "%s=%s" % (self.__key, self.__value)

    # Public methods

    # def url_format(self):
    #     unicode_key = unicode(self.key, "utf-8")
    #     url_formatted_key = urllib.quote(unicode_key)
    #
    #     # convert Boolean values to 0, 1
    #     value = int(self.value) if self.value_type == self.VALUE_TYPE_BOOLEAN else self.value
    #     unicode_value = unicode(value, "utf-8")
    #     url_formatted_value = urllib.quote(unicode_value, "")
    #     return "%s=%s" % (url_formatted_key, url_formatted_value)

    def validate_key(self):
        if not self.valid_key_pattern and not self.valid_key_pattern.match(self.key):
            raise ValidateException("%s's key has invalid format" % self.__class__.__name__)

    def validate_value(self):
        validate_func_name = "validate_%s" % self.value_type
        validate_func = self.__getattribute__(validate_func_name)
        if not validate_func():
            raise ValidateException("%s's value must be of type %s" % (self.__class__.__name__, self.value_type))

        if isinstance(self.valid_value_pattern, REGEX_OBJECT_TYPE) and not self.valid_value_pattern.match(self.value):
            raise ValidateException("%s's value has invalid format" % self.__class__.__name__)

        if self.valid_values and self.value not in self.valid_values:
            raise ValidateException("%s has invalid value" % self.__class__.__name__)

    def validate_text(self):
        return isinstance(self.value, str) and not is_empty_string(self.value)

    def validate_integer(self):
        return isinstance(self.value, int)

    def validate_currency(self):
        return isinstance(self.value, float)

    def validate_boolean(self):
        return isinstance(self.value, bool)


###############################################################################
# GENERAL
###############################################################################


class ProtocolVersion(Parameter):
    PROTOCOL_VERSION_PARAM_KEY = "v"

    def __init__(self, value="1"):
        super(ProtocolVersion, self).__init__(self.PROTOCOL_VERSION_PARAM_KEY,
                                              value,
                                              self.VALUE_TYPE_TEXT,
                                              is_required=True)


class TrackingID(Parameter):
    TRACKING_ID_PARAM_KEY = "tid"
    TRACKING_ID_VALID_VALUE_PATTERN = re.compile(r"^UA-[0-9]*-[0-9]*$")

    def __init__(self, value):
        super(TrackingID, self).__init__(self.TRACKING_ID_PARAM_KEY,
                                         value,
                                         self.VALUE_TYPE_TEXT,
                                         is_required=True,
                                         valid_value_pattern=self.TRACKING_ID_VALID_VALUE_PATTERN)


class AnonymizeIP(Parameter):
    ANONYMIZE_IP_PARAM_KEY = "aip"

    def __init__(self, value):
        super(AnonymizeIP, self).__init__(self.ANONYMIZE_IP_PARAM_KEY,
                                          value,
                                          self.VALUE_TYPE_BOOLEAN)


class QueueTime(Parameter):
    QUEUE_TIME_PARAM_KEY = "qt"

    def __init__(self, value):
        super(QueueTime, self).__init__(self.QUEUE_TIME_PARAM_KEY,
                                        value,
                                        self.VALUE_TYPE_INTEGER)


class CacheBuster(Parameter):
    CACHE_BUSTER_PARAM_KEY = "z"

    def __init__(self):
        value = str(random.randrange(sys.maxint))
        super(CacheBuster, self).__init__(self.CACHE_BUSTER_PARAM_KEY,
                                          value,
                                          self.VALUE_TYPE_TEXT)


###############################################################################
# VISITOR
###############################################################################


class ClientID(Parameter):
    CLIENT_ID_PARAM_KEY = "cid"

    def __init__(self, value):
        super(ClientID, self).__init__(self.CLIENT_ID_PARAM_KEY,
                                       value,
                                       self.VALUE_TYPE_TEXT,
                                       is_required=True)


###############################################################################
# SESSION
###############################################################################


class SessionControl(Parameter):
    SESSION_CONTROL_PARAM_KEY = "sc"
    SESSION_CONTROL_VALID_VALUES = ["start", "end"]

    def __init__(self, value):
        super(SessionControl, self).__init__(self.SESSION_CONTROL_PARAM_KEY,
                                             value,
                                             self.VALUE_TYPE_TEXT,
                                             valid_values=self.SESSION_CONTROL_VALID_VALUES)


###############################################################################
# TRAFFIC SOURCES
###############################################################################


class DocumentReferrer(Parameter):
    DOCUMENT_REFERRER_PARAM_KEY = "dr"
    DOCUMENT_REFERRER_MAX_LENGTH = 2048

    def __init__(self, value):
        super(DocumentReferrer, self).__init__(self.DOCUMENT_REFERRER_PARAM_KEY,
                                               value,
                                               self.VALUE_TYPE_TEXT,
                                               max_length=self.DOCUMENT_REFERRER_MAX_LENGTH)


class CampaignName(Parameter):
    CAMPAIGN_NAME_PARAM_KEY = "cn"
    CAMPAIGN_NAME_MAX_LENGTH = 100

    def __init__(self, value):
        super(CampaignName, self).__init__(self.CAMPAIGN_NAME_PARAM_KEY,
                                           value,
                                           self.VALUE_TYPE_TEXT,
                                           max_length=self.CAMPAIGN_NAME_MAX_LENGTH)


class CampaignSource(Parameter):
    CAMPAIGN_SOURCE_PARAM_KEY = "cs"
    CAMPAIGN_SOURCE_MAX_LENGTH = 100

    def __init__(self, value):
        super(CampaignSource, self).__init__(self.CAMPAIGN_SOURCE_PARAM_KEY,
                                             value,
                                             self.VALUE_TYPE_TEXT,
                                             max_length=self.CAMPAIGN_SOURCE_MAX_LENGTH)


class CampaignMedium(Parameter):
    CAMPAIGN_MEDIUM_PARAM_KEY = "cm"
    CAMPAIGN_MEDIUM_MAX_LENGTH = 50

    def __init__(self, value):
        super(CampaignMedium, self).__init__(self.CAMPAIGN_MEDIUM_PARAM_KEY,
                                             value,
                                             self.VALUE_TYPE_TEXT,
                                             max_length=self.CAMPAIGN_MEDIUM_MAX_LENGTH)


class CampaignKeyword(Parameter):
    CAMPAIGN_KEYWORD_PARAM_KEY = "ck"
    CAMPAIGN_KEYWORD_MAX_LENGTH = 500

    def __init__(self, value):
        super(CampaignKeyword, self).__init__(self.CAMPAIGN_KEYWORD_PARAM_KEY,
                                              value,
                                              self.VALUE_TYPE_TEXT,
                                              max_length=self.CAMPAIGN_KEYWORD_MAX_LENGTH)


class CampaignContent(Parameter):
    CAMPAIGN_CONTENT_PARAM_KEY = "cc"
    CAMPAIGN_CONTENT_MAX_LENGTH = 500

    def __init__(self, value):
        super(CampaignContent, self).__init__(self.CAMPAIGN_CONTENT_PARAM_KEY,
                                              value,
                                              self.VALUE_TYPE_TEXT,
                                              max_length=self.CAMPAIGN_CONTENT_MAX_LENGTH)


class CampaignID(Parameter):
    CAMPAIGN_ID_PARAM_KEY = "ci"
    CAMPAIGN_ID_MAX_LENGTH = 100

    def __init__(self, value):
        super(CampaignID, self).__init__(self.CAMPAIGN_ID_PARAM_KEY,
                                         value,
                                         self.VALUE_TYPE_TEXT,
                                         max_length=self.CAMPAIGN_ID_MAX_LENGTH)


class GoogleAdWordsID(Parameter):
    GOOGLE_ADWORDS_ID_PARAM_KEY = "gclid"

    def __init__(self, value):
        super(GoogleAdWordsID, self).__init__(self.GOOGLE_ADWORDS_ID_PARAM_KEY,
                                              value,
                                              self.VALUE_TYPE_TEXT)


class GoogleDisplayAdsID(Parameter):
    GOOGLE_DISPLAY_ADS_ID_PARAM_KEY = "dclid"

    def __init__(self, value):
        super(GoogleDisplayAdsID, self).__init__(self.GOOGLE_DISPLAY_ADS_ID_PARAM_KEY,
                                                 value,
                                                 self.VALUE_TYPE_TEXT)
        

###############################################################################
# SYSTEM INFO
###############################################################################


class ScreenResolution(Parameter):
    SCREEN_RESOLUTION_PARAM_KEY = "sr"
    SCREEN_RESOLUTION_MAX_LENGTH = 20
    
    def __init__(self, value):
        super(ScreenResolution, self).__init__(self.SCREEN_RESOLUTION_PARAM_KEY,
                                               value,
                                               self.VALUE_TYPE_TEXT,
                                               max_length=self.SCREEN_RESOLUTION_MAX_LENGTH)


class ViewportSize(Parameter):
    VIEWPORT_SIZE_PARAM_KEY = "vp"
    VIEWPORT_SIZE_MAX_LENGTH = 20

    def __init__(self, value):
        super(ViewportSize, self).__init__(self.VIEWPORT_SIZE_PARAM_KEY,
                                           value,
                                           self.VALUE_TYPE_TEXT,
                                           max_length=self.VIEWPORT_SIZE_MAX_LENGTH)


class DocumentEncoding(Parameter):
    DOCUMENT_ENCODING_PARAM_KEY = "de"
    DOCUMENT_ENCODING_DEFAULT_VALUE = "UTF-8"
    DOCUMENT_ENCODING_MAX_LENGTH = 20

    def __init__(self, value):
        super(DocumentEncoding, self).__init__(self.DOCUMENT_ENCODING_PARAM_KEY,
                                               value,
                                               self.VALUE_TYPE_TEXT,
                                               max_length=self.DOCUMENT_ENCODING_MAX_LENGTH)


class ScreenColors(Parameter):
    SCREEN_COLORS_PARAM_KEY = "sd"
    SCREEN_COLORS_MAX_LENGTH = 20

    def __init__(self, value):
        super(ScreenColors, self).__init__(self.SCREEN_COLORS_PARAM_KEY,
                                           value,
                                           self.VALUE_TYPE_TEXT,
                                           max_length=self.SCREEN_COLORS_MAX_LENGTH)


class UserLanguage(Parameter):
    USER_LANGUAGE_PARAM_KEY = "ul"
    USER_LANGUAGE_MAX_LENGTH = 20

    def __init__(self, value):
        super(UserLanguage, self).__init__(self.USER_LANGUAGE_PARAM_KEY,
                                           value,
                                           self.VALUE_TYPE_TEXT,
                                           max_length=self.USER_LANGUAGE_MAX_LENGTH)


class JavaEnabled(Parameter):
    JAVA_ENABLED_PARAM_KEY = "je"

    def __init__(self, value):
        super(JavaEnabled, self).__init__(self.JAVA_ENABLED_PARAM_KEY,
                                          value,
                                          self.VALUE_TYPE_BOOLEAN)


class FlashVersion(Parameter):
    FLASH_VERSION_PARAM_KEY = "fl"

    def __init__(self, value):
        super(FlashVersion, self).__init__(self.FLASH_VERSION_PARAM_KEY,
                                           value,
                                           self.VALUE_TYPE_TEXT,
                                           max_length=20)


###############################################################################
# HIT
###############################################################################


class HitType(Parameter):
    HIT_TYPE_PARAM_KEY = "t"
    HIT_TYPE_VALID_VALUES = ["pageview", "appview", "event", "transaction", "item", "social", "exception", "timing"]

    def __init__(self, value):
        super(HitType, self).__init__(self.HIT_TYPE_PARAM_KEY,
                                      value,
                                      self.VALUE_TYPE_TEXT,
                                      is_required=True,
                                      valid_values=self.HIT_TYPE_VALID_VALUES)


class NonInteractionHit(Parameter):
    NON_INTERACTION_HIT_PARAM_KEY = "ni"

    def __init__(self, value):
        super(NonInteractionHit, self).__init__(self.NON_INTERACTION_HIT_PARAM_KEY,
                                                value,
                                                self.VALUE_TYPE_BOOLEAN)


###############################################################################
# CONTENT INFORMATION
###############################################################################


class DocumentLocationURL(Parameter):
    DOCUMENT_LOCATION_URL_PARAM_KEY = "dl"
    DOCUMENT_LOCATION_URL_MAX_LENGTH = 2048

    def __init__(self, value):
        super(DocumentLocationURL, self).__init__(self.DOCUMENT_LOCATION_URL_PARAM_KEY,
                                                  value,
                                                  self.VALUE_TYPE_TEXT,
                                                  max_length=self.DOCUMENT_LOCATION_URL_MAX_LENGTH)


class DocumentHostName(Parameter):
    DOCUMENT_HOST_NAME_PARAM_KEY = "dh"
    DOCUMENT_HOST_NAME_MAX_LENGTH = 100

    def __init__(self, value):
        super(DocumentHostName, self).__init__(self.DOCUMENT_HOST_NAME_PARAM_KEY,
                                               value,
                                               self.VALUE_TYPE_TEXT,
                                               max_length=self.DOCUMENT_HOST_NAME_MAX_LENGTH)


class DocumentPath(Parameter):
    DOCUMENT_PATH_PARAM_KEY = "dp"
    DOCUMENT_PATH_MAX_LENGTH = 2048
    DOCUMENT_PATH_VALID_PATTERN = re.compile(r"^//.*")

    def __init__(self, value):
        super(DocumentPath, self).__init__(self.DOCUMENT_PATH_PARAM_KEY,
                                           value,
                                           self.VALUE_TYPE_TEXT,
                                           max_length=self.DOCUMENT_PATH_MAX_LENGTH,
                                           valid_value_pattern=self.DOCUMENT_PATH_VALID_PATTERN)


class DocumentTitle(Parameter):
    DOCUMENT_TITLE_PARAM_KEY = "dt"
    DOCUMENT_TITLE_MAX_LENGTH = 1500

    def __init__(self, value):
        super(DocumentTitle, self).__init__(self.DOCUMENT_TITLE_PARAM_KEY,
                                            value,
                                            self.VALUE_TYPE_TEXT,
                                            max_length=self.DOCUMENT_TITLE_MAX_LENGTH)


class ContentDescription(Parameter):
    CONTENT_DESCRIPTION_PARAM_KEY = "cd"
    CONTENT_DESCRIPTION_MAX_LENGTH = 2048

    def __init__(self, value):
        super(ContentDescription, self).__init__(self.CONTENT_DESCRIPTION_PARAM_KEY,
                                                 value,
                                                 self.VALUE_TYPE_TEXT,
                                                 max_length=self.CONTENT_DESCRIPTION_MAX_LENGTH)


###############################################################################
# APP TRACKING
###############################################################################


class ApplicationName(Parameter):
    APPLICATION_NAME_PARAM_KEY = "an"
    APPLICATION_NAME_MAX_LENGTH = 100

    def __init__(self, value):
        super(ApplicationName, self).__init__(self.APPLICATION_NAME_PARAM_KEY,
                                              value,
                                              self.VALUE_TYPE_TEXT,
                                              max_length=self.APPLICATION_NAME_MAX_LENGTH)


class ApplicationVersion(Parameter):
    APPLICATION_VERSION_PARAM_KEY = "av"
    APPLICATION_VERSION_MAX_LENGTH = 100

    def __init__(self, value):
        super(ApplicationVersion, self).__init__(self.APPLICATION_VERSION_PARAM_KEY,
                                                 value,
                                                 self.VALUE_TYPE_TEXT,
                                                 max_length=self.APPLICATION_VERSION_MAX_LENGTH)


###############################################################################
# EVENT TRACKING
###############################################################################


class EventCategory(Parameter):
    EVENT_CATEGORY_PARAM_KEY = "ec"
    EVENT_CATEGORY_MAX_LENGTH = 150

    def __init__(self, value):
        super(EventCategory, self).__init__(self.EVENT_CATEGORY_PARAM_KEY,
                                            value,
                                            self.VALUE_TYPE_TEXT,
                                            max_length=self.EVENT_CATEGORY_MAX_LENGTH)


class EventAction(Parameter):
    EVENT_ACTION_PARAM_KEY = "ea"
    EVENT_ACTION_MAX_LENGTH = 500

    def __init__(self, value):
        super(EventAction, self).__init__(self.EVENT_ACTION_PARAM_KEY,
                                          value,
                                          self.VALUE_TYPE_TEXT,
                                          max_length=self.EVENT_ACTION_MAX_LENGTH)


class EventLabel(Parameter):
    EVENT_LABEL_PARAM_KEY = "el"
    EVENT_LABEL_MAX_LENGTH = 500

    def __init__(self, value):
        super(EventLabel, self).__init__(self.EVENT_LABEL_PARAM_KEY,
                                         value,
                                         self.VALUE_TYPE_TEXT,
                                         max_length=self.EVENT_LABEL_MAX_LENGTH)


class EventValue(Parameter):
    EVENT_VALUE_PARAM_KEY = "ev"

    def __init__(self, value):
        super(EventValue, self).__init__(self.EVENT_VALUE_PARAM_KEY,
                                         value,
                                         self.VALUE_TYPE_INTEGER)


###############################################################################
# E-COMMERCE
###############################################################################


class TransactionID(Parameter):
    TRANSACTION_ID_PARAM_KEY = "ti"
    TRANSACTION_ID_MAX_LENGTH = 500

    def __init__(self, value):
        super(TransactionID, self).__init__(self.TRANSACTION_ID_PARAM_KEY,
                                            value,
                                            self.VALUE_TYPE_TEXT,
                                            max_length=self.TRANSACTION_ID_MAX_LENGTH)


class TransactionAffiliation(Parameter):
    TRANSACTION_AFFILIATION_PARAM_KEY = "ta"
    TRANSACTION_AFFILIATION_MAX_LENGTH = 500

    def __init__(self, value):
        super(TransactionAffiliation, self).__init__(self.TRANSACTION_AFFILIATION_PARAM_KEY,
                                                     value,
                                                     self.VALUE_TYPE_TEXT,
                                                     max_length=self.TRANSACTION_AFFILIATION_MAX_LENGTH)


class TransactionRevenue(Parameter):
    TRANSACTION_REVENUE_PARAM_KEY = "tr"

    def __init__(self, value):
        super(TransactionRevenue, self).__init__(self.TRANSACTION_REVENUE_PARAM_KEY,
                                                 value,
                                                 self.VALUE_TYPE_CURRENCY)


class TransactionShipping(Parameter):
    TRANSACTION_SHIPPING_PARAM_KEY = "ts"

    def __init__(self, value):
        super(TransactionShipping, self).__init__(self.TRANSACTION_SHIPPING_PARAM_KEY,
                                                  value,
                                                  self.VALUE_TYPE_CURRENCY)


class TransactionTax(Parameter):
    TRANSACTION_TAX_PARAM_KEY = "tt"

    def __init__(self, value):
        super(TransactionTax, self).__init__(self.TRANSACTION_TAX_PARAM_KEY,
                                             value,
                                             self.VALUE_TYPE_CURRENCY)


class ItemName(Parameter):
    ITEM_NAME_PARAM_KEY = "in"
    ITEM_NAME_MAX_LENGTH = 500

    def __init__(self, value):
        super(ItemName, self).__init__(self.ITEM_NAME_PARAM_KEY,
                                       value,
                                       self.VALUE_TYPE_TEXT,
                                       max_length=self.ITEM_NAME_MAX_LENGTH)


class ItemPrice(Parameter):
    ITEM_PRICE_PARAM_KEY = "ip"

    def __init__(self, value):
        super(ItemPrice, self).__init__(self.ITEM_PRICE_PARAM_KEY,
                                        value,
                                        self.VALUE_TYPE_CURRENCY)


class ItemQuantity(Parameter):
    ITEM_QUANTITY_PARAM_KEY = "iq"

    def __init__(self, value):
        super(ItemQuantity, self).__init__(self.ITEM_QUANTITY_PARAM_KEY,
                                           value,
                                           self.VALUE_TYPE_INTEGER)


class ItemCode(Parameter):
    ITEM_CODE_PARAM_KEY = "ic"
    ITEM_CODE_MAX_LENGTH = 500

    def __init__(self, value):
        super(ItemCode, self).__init__(self.ITEM_CODE_PARAM_KEY,
                                       value,
                                       self.VALUE_TYPE_TEXT,
                                       max_length=self.ITEM_CODE_MAX_LENGTH)


class ItemCategory(Parameter):
    ITEM_CATEGORY_PARAM_KEY = "iv"
    ITEM_CATEGORY_MAX_LENGTH = 500

    def __init__(self, value):
        super(ItemCategory, self).__init__(self.ITEM_CATEGORY_PARAM_KEY,
                                           value,
                                           self.VALUE_TYPE_TEXT,
                                           max_length=self.ITEM_CATEGORY_MAX_LENGTH)


class CurrencyCode(Parameter):
    CURRENCY_CODE_PARAM_KEY = "cu"
    CURRENCY_CODE_MAX_LENGTH = 10
    
    # TODO check that the value conforms to ISO 4217 currency code
    def __init__(self, value):
        super(CurrencyCode, self).__init__(self.CURRENCY_CODE_PARAM_KEY,
                                           value,
                                           self.VALUE_TYPE_TEXT,
                                           max_length=self.CURRENCY_CODE_MAX_LENGTH)
        
        
###############################################################################
# SOCIAL INTERACTIONS
###############################################################################


class SocialNetwork(Parameter):
    SOCIAL_NETWORK_PARAM_KEY = "sn"
    SOCIAL_NETWORK_MAX_LENGTH = 50
    
    def __init__(self, value):
        super(SocialNetwork, self).__init__(self.SOCIAL_NETWORK_PARAM_KEY,
                                            value,
                                            self.VALUE_TYPE_TEXT,
                                            max_length=self.SOCIAL_NETWORK_MAX_LENGTH)


class SocialAction(Parameter):
    SOCIAL_ACTION_PARAM_KEY = "sa"
    SOCIAL_ACTION_MAX_LENGTH = 50
    
    def __init__(self, value):
        super(SocialAction, self).__init__(self.SOCIAL_ACTION_PARAM_KEY,
                                           value,
                                           self.VALUE_TYPE_TEXT,
                                           max_length=self.SOCIAL_ACTION_MAX_LENGTH)


class SocialActionTarget(Parameter):
    SOCIAL_ACTION_TARGET_PARAM_KEY = "st"
    SOCIAL_ACTION_TARGET_MAX_LENGTH = 2048
    
    def __init__(self, value):
        super(SocialActionTarget, self).__init__(self.SOCIAL_ACTION_TARGET_PARAM_KEY,
                                                 value,
                                                 self.VALUE_TYPE_TEXT,
                                                 max_length=self.SOCIAL_ACTION_TARGET_MAX_LENGTH)


###############################################################################
# TIMING
###############################################################################


class UserTimingCategory(Parameter):
    USER_TIMING_CATEGORY_PARAM_KEY = "utc"
    USER_TIMING_CATEGORY_MAX_LENGTH = 150
    
    def __init__(self, value):
        super(UserTimingCategory, self).__init__(self.USER_TIMING_CATEGORY_PARAM_KEY,
                                                 value,
                                                 self.VALUE_TYPE_TEXT,
                                                 max_length=self.USER_TIMING_CATEGORY_MAX_LENGTH)
        

class UserTimingVariableName(Parameter):
    USER_TIMING_VARIABLE_NAME_PARAM_KEY = "utv"
    USER_TIMING_VARIABLE_NAME_MAX_LENGTH = 500
    
    def __init__(self, value):
        super(UserTimingVariableName, self).__init__(self.USER_TIMING_VARIABLE_NAME_PARAM_KEY,
                                                     value,
                                                     self.VALUE_TYPE_TEXT,
                                                     max_length=self.USER_TIMING_VARIABLE_NAME_MAX_LENGTH)
        

class UserTimingTime(Parameter):
    USER_TIMING_TIME_PARAM_KEY = "utt"
    
    def __init__(self, value):
        super(UserTimingTime, self).__init__(self.USER_TIMING_TIME_PARAM_KEY,
                                             value,
                                             self.VALUE_TYPE_INTEGER)
        

class UserTimingLabel(Parameter):
    USER_TIMING_LABEL_PARAM_KEY = "utl"
    USER_TIMING_LABEL_MAX_LENGTH = 500
    
    def __init__(self, value):
        super(UserTimingLabel, self).__init__(self.USER_TIMING_LABEL_PARAM_KEY,
                                              value,
                                              self.VALUE_TYPE_TEXT,
                                              max_length=self.USER_TIMING_LABEL_MAX_LENGTH)
        

class UserPageLoadTime(Parameter):
    USER_PAGE_LOAD_TIME_PARAM_KEY = "plt"
    
    def __init__(self, value):
        super(UserPageLoadTime, self).__init__(self.USER_PAGE_LOAD_TIME_PARAM_KEY,
                                               value,
                                               self.VALUE_TYPE_INTEGER)
        

class UserDNSTime(Parameter):
    USER_DNS_TIME_PARAM_KEY = "dns"
    
    def __init__(self, value):
        super(UserDNSTime, self).__init__(self.USER_DNS_TIME_PARAM_KEY,
                                          value,
                                          self.VALUE_TYPE_INTEGER)
        

class PageDownloadTime(Parameter):
    PAGE_DOWNLOAD_TIME_PARAM_KEY = "pdt"
    
    def __init__(self, value):
        super(PageDownloadTime, self).__init__(self.PAGE_DOWNLOAD_TIME_PARAM_KEY,
                                               value,
                                               self.VALUE_TYPE_INTEGER)


class RedirectResponseTime(Parameter):
    REDIRECT_RESPONSE_TIME_PARAM_KEY = "rrt"
    
    def __init__(self, value):
        super(RedirectResponseTime, self).__init__(self.REDIRECT_RESPONSE_TIME_PARAM_KEY,
                                                   value,
                                                   self.VALUE_TYPE_INTEGER)


class TCPConnectTime(Parameter):
    TCP_CONNECT_TIME_PARAM_KEY = "tcp"

    def __init__(self, value):
        super(TCPConnectTime, self).__init__(self.TCP_CONNECT_TIME_PARAM_KEY,
                                             value,
                                             self.VALUE_TYPE_INTEGER)


class ServerResponseTime(Parameter):
    SERVER_RESPONSE_TIME_PARAM_KEY = "srt"

    def __init__(self, value):
        super(ServerResponseTime, self).__init__(self.SERVER_RESPONSE_TIME_PARAM_KEY,
                                                 value,
                                                 self.VALUE_TYPE_INTEGER)


###############################################################################
# EXCEPTIONS
###############################################################################


class ExceptionDescription(Parameter):
    EXCEPTION_DESCRIPTION_PARAM_KEY = "exd"
    EXCEPTION_DESCRIPTION_MAX_LENGTH = 150

    def __init__(self, value):
        super(ExceptionDescription, self).__init__(self.EXCEPTION_DESCRIPTION_PARAM_KEY,
                                                   value,
                                                   self.VALUE_TYPE_TEXT,
                                                   max_length=self.EXCEPTION_DESCRIPTION_MAX_LENGTH)


class IsExceptionFatal(Parameter):
    IS_EXCEPTION_FATAL_PARAM_KEY = "exf"

    def __init__(self, value=True):
        super(IsExceptionFatal, self).__init__(self.IS_EXCEPTION_FATAL_PARAM_KEY,
                                               value,
                                               self.VALUE_TYPE_BOOLEAN)


###############################################################################
# CUSTOM METRIC
###############################################################################


class CustomDimension(Parameter):
    CUSTOM_DIMENSION_VALID_KEY_PATTERN = re.compile(r"^cd[1-9][0-9]*$")
    CUSTOM_DIMENSION_MAX_LENGTH = 150

    def __init__(self, key, value):
        super(CustomDimension, self).__init__(key,
                                              value,
                                              self.VALUE_TYPE_TEXT,
                                              max_length=self.CUSTOM_DIMENSION_MAX_LENGTH,
                                              valid_key_pattern=self.CUSTOM_DIMENSION_VALID_KEY_PATTERN)


class CustomMetric(Parameter):
    CUSTOM_METRIC_VALID_KEY_PATTERN = re.compile(r"^cm[1-9][0-9]*$")

    def __init__(self, key, value):
        super(CustomMetric, self).__init__(key,
                                           value,
                                           self.VALUE_TYPE_INTEGER,
                                           valid_key_pattern=self.CUSTOM_METRIC_VALID_KEY_PATTERN)