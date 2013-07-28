# -*- coding: utf-8 -*-

__author__ = 'minhtule'

from unittest import TestCase
from ga.parameter import *


class TestParameter(TestCase):
    def test_value(self):
        self.assertTrue(Parameter("key1", "right format", "text"))
        self.assertTrue(Parameter("key2", -54.234, "currency"))
        self.assertTrue(Parameter("key3", True, "boolean"))
        self.assertTrue(Parameter("key4", 343, "integer"))

        with self.assertRaises(ValidateException):
            Parameter("key5", 2.34, Parameter.VALUE_TYPE_TEXT)
            Parameter("key6", "wrong format", Parameter.VALUE_TYPE_CURRENCY)
            Parameter("key7", 4, Parameter.VALYE_TYPE_BOOLEAN)
            Parameter("key8", True, Parameter.VALUE_TYPE_INTEGER)

    def test_protocol_version(self):
        protocol_version = ProtocolVersion()
        self.assertEqual(protocol_version.value, "1")

    def test_tracking_id(self):
        self.assertTrue(TrackingID("UA-42620910-11"))

        with self.assertRaises(ValidateException):
            TrackingID("UUA-42620910-11")
            TrackingID("UA-4262091a-11")
            TrackingID("UA-42620910-1a")

    def test_anonymize_ip(self):
        self.assertTrue(AnonymizeIP(True))

        with self.assertRaises(ValidateException):
            AnonymizeIP(1)
            AnonymizeIP("1")