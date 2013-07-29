__author__ = 'minhtule'

from unittest import TestCase
from ga.request import *
from ga.tracker import *
from ga.visitor import *

TRACKING_ID = "UA-42620910-9"
VISITOR = Visitor()
TRACKER = Tracker(TRACKING_ID, VISITOR)


class TestRequest(TestCase):
    def test_page_tracking(self):
        page_tracking_request = PageTrackingRequest(TRACKER, "localhost", "/product", "product")
        self.assertTrue(page_tracking_request.send())

