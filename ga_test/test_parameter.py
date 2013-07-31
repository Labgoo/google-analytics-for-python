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

    def test_url_format_basic(self):
        param_text = Parameter("key1", " 2 ^ 3 * a", "text")
        self.assertEqual(param_text.url_format(), u"key1=%202%20%5E%203%20%2A%20a")
        param_currency = Parameter("key%2", -22.343, "currency")
        self.assertEqual(param_currency.url_format(), u"key%252=-22.343")
        param_boolean = Parameter("key/3", True, "boolean")
        self.assertEqual(param_boolean.url_format(), u"key%2F3=1")
        param_integer = Parameter("key_4", 8343, "integer")
        self.assertEqual(param_integer.url_format(), u"key_4=8343")

    def test_url_format_advance(self):
        param1 = Parameter("dp", "/my page €", "text")
        self.assertEqual(param1.url_format(), u"dp=%2Fmy%20page%20%E2%82%AC")

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
        self.assertTrue(AnonymizeIP())

        with self.assertRaises(ValidateException):
            AnonymizeIP(1)
            AnonymizeIP("1")