__author__ = 'minhtule'

from uuid import uuid4
import webapp2


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
        if isinstance(request, webapp2.Request):
            self.request = request
            self.id = self.__get_id()
            self.document_url = request.url
            self.document_host = request.host
            self.document_path = request.path
            self.language = self.__extract_language()
            self.user_agent = request.user_agent
            self.ip_address = request.remote_addr
        else:
            # This should be only used for testing
            self.request = None
            self.id = str(uuid4())
            self.document_url = None
            self.document_host = None
            self.document_path = None
            self.language = None
            self.user_agent = None
            self.ip_address = None

    def __get_id(self):
        cookies = self.request.cookies
        try:
            cookie_value = cookies[GA_TRACKING_COOKIE_NAME]
        except (KeyError, TypeError):
            cookie_value = str(uuid4())

        return cookie_value

    def __extract_language(self):
        """

        """
        try:
            accept_language = self.request.accept_language._parsed
            # sorted according to the "q" parameter (relative quality factor) in the decreasing order
            sorted(accept_language, key=lambda language: language[1], reverse=True)

            # use only the first language in the sorted list and ignore the rest
            # even there may be more than 1 language with q = 1
            return str.lower(accept_language[0][0])
        except AttributeError:
            return None