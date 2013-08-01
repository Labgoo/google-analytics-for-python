__author__ = 'minhtule'

from unittest import TestCase
from gap.request import *
from gap.tracker import *
from gap.visitor import *

TRACKING_ID = "UA-42620910-9"
# VISITOR = "555"
VISITOR = Visitor()
TRACKER = Tracker(TRACKING_ID, VISITOR)


class TestRequest(TestCase):
    def test_page_tracking(self):
        page_tracking_request = PageTrackingRequest(TRACKER, "localhost", "/product", "product")
        self.assertTrue(page_tracking_request.send())

