__author__ = 'minhtule'


from ga.request import *


class Tracker(object):
    """

    """
    def __init__(self, tracking_id, client_id):
        self.__tracking_id = TrackingID(tracking_id)
        self.__client_id = ClientID(client_id)
        self.__debug_enabled = False

    @property
    def tracking_id(self):
        return self.__tracking_id

    @property
    def client_id(self):
        return self.__client_id

    @property
    def debug_enabled(self):
        return self.__debug_enabled

    @debug_enabled.setter
    def debug_enabled(self, value):
        self.__debug_enabled = value

    # Public method

    def sendEvent(self, category, action, label=None, value=None):
        request = EventTrackingRequest(self, category, action, label, value)
        request.send()
