__author__ = 'minhtule'

from webapp2 import Request
from uuid import uuid4

GA_TRACKING_COOKIE_NAME = "ga_tracking"
GA_TRACKING_COOKIE_MAX_AGE = 63072000  # 2years * 365days * 24h * 60m * 60s


class Visitor(object):
    """ Visitor object contains information of the user from whom the request is sent.

    These information are needed for some Google Analytics' parameters. They are extracted from the
    http header of the request of webapp2 framework's handler. Although this class is specially design
    to work for Google App Engine, any server that uses webapp2 framework should be able to reuse this
    class.


    """

    def __init__(self, request=None):
        if isinstance(request, Request):
            self.document_url = request.url
            self.document_host = request.host
            self.document_path = request.path
            self.accept_language = request.accept_language
            self.user_agent = request.user_agent
            self.ip_address = request.remote_addr
            self.tracking_cookie = self.__create_cookie(request.cookies)
            self.id = self.tracking_cookie["value"]
        else:
            self.document_url = None
            self.document_host = None
            self.document_path = None
            self.accept_language = None
            self.user_agent = None
            self.ip_address = None
            self.tracking_cookie = self.__create_cookie(None)
            self.id = str(uuid4())

    # This cookie has the default_path="/" and thus it tracks the entire domain
    def __create_cookie(self, cookies=None):
        if GA_TRACKING_COOKIE_NAME in cookies:
            cookie_value = cookies[GA_TRACKING_COOKIE_NAME]
        else:
            cookie_value = str(uuid4())

        return {
            "key": GA_TRACKING_COOKIE_NAME,
            "value": cookie_value,
            "max_age": GA_TRACKING_COOKIE_MAX_AGE,
            "overwrite": True,
            "secure": False,
            "httponly": False
        }

