#!/usr/bin/env python3
"""Unit tests for utils module"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
from typing import Dict, Tuple, Union


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Dict,
                               path: Tuple[str], expected: Union[Dict, int]):
        """Test access_nested_map function"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map: Dict,
                                         path: Tuple[str],
                                         exception: Exception):
        """Test access_nested_map function raises correct exception"""
        with self.assertRaises(exception) as context:
            access_nested_map(nested_map, path)
        if path[-1] not in nested_map:
            self.assertEqual(str(context.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """Tests for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: Dict,
                      mock_get: Mock) -> None:
        """Test get_json function"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator"""

    def test_memoize(self):
        """Test memoize decorator"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            test_class = TestClass()
            mock_method.return_value = 42

            # First call
            result1 = test_class.a_property
            self.assertEqual(result1, 42)
            mock_method.assert_called_once()

            # Second call
            result2 = test_class.a_property
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
