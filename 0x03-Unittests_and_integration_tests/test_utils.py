#!/usr/bin/env python3
"""unit tests"""
import unittest
from unittest.mock import patch, Mock
from typing import Dict
from parameterized import parameterized
from utils import access_nested_map
from utils import get_json


class TestGetJson(unittest.TestCase):
    """
    Test case for the get_json function in the utils module.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that get_json returns the expected
        result and makes the correct HTTP call.
        Parameters:
        test_url (str): The URL to pass to get_json.
        test_payload (dict): The expected JSON payload
        to be returned by get_json.
        mock_get (Mock): The mocked requests.get method.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestAccessNestedMap(unittest.TestCase):
    """TestAccessNestedMap"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access nested map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map, path, exception):
        """Test that access_nested_map raises an error correctly"""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


if __name__ == "__main__":
    unittest.main()
