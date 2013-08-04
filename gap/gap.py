__author__ = 'minhtule'

from tracker import *
from visitor import *
import webapp2


class GAP(object):

    def __init__(self, request_handler):
        self.default_tracker = None
        self.__trackers = {}
        if isinstance(request_handler, webapp2.RequestHandler):
            self.__request_handler = request_handler
            self.__visitor = Visitor(request_handler.request)
            self.__set_cookie_in_response()
        else:
            self.__request_handler = None
            self.__visitor = None

    def get_tracker_with_tracking_id(self, tracking_id):
        if tracking_id in self.__trackers:
            tracker = self.__trackers[tracking_id]
        else:
            tracker = Tracker(tracking_id, self.__visitor)
            if not self.__trackers:
                self.__trackers[tracking_id] = tracker
                self.default_tracker = tracker

        return tracker

    def __set_cookie_in_response(self):
        response = self.__request_handler.response
        response.set_cookie(GA_TRACKING_COOKIE_NAME,
                           self.__visitor.id,
                           max_age=GA_TRACKING_COOKIE_MAX_AGE,
                           overwrite=True,
                           httponly=False)