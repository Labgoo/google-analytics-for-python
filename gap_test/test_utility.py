__author__ = 'minhtule'

from unittest import TestCase
from gap.utility import *


class TestUtility(TestCase):
    def test_is_empty_string(self):
        self.assertTrue(is_empty_string(""))
        self.assertTrue(is_empty_string("    "))
        self.assertTrue(is_empty_string(" \t "))
        self.assertFalse(is_empty_string("  a  "))