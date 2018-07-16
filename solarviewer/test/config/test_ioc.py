import unittest
from typing import List

from mock import Mock

from solarviewer.config.ioc import features, RequiredFeature, HasAttributes, HasMethods, MatchingFeatures, IsInstanceOf


class Object:
    test = Mock()


class TestIoC(unittest.TestCase):
    feature: Object = RequiredFeature("TEST1")
    method: Object = RequiredFeature("TEST2", HasMethods("required_method"))
    attr: Object = RequiredFeature("TEST3", HasAttributes("required_attribute"))

    features.Provide("1", "1")
    features.Provide("2", "2")
    features.Provide("3", "3")
    features: List[str] = MatchingFeatures(IsInstanceOf(str))

    def test_provide(self):
        mock = Object()

        features.Provide("TEST1", mock)
        self.feature.test()

        mock.test.assert_called_once()

    def test_has_method(self):
        mock = Object()
        mock.required_method = Mock()

        features.Provide("TEST2", mock)
        self.method.required_method()

        mock.required_method.assert_called_once()

    def test_has_attribute(self):
        mock = Object()
        mock.required_attribute = "TEST3"

        features.Provide("TEST3", mock)

        self.assertEqual(self.attr.required_attribute, "TEST3")

    def test_matching(self):
        self.assertEqual(["1", "2", "3"], self.features)
