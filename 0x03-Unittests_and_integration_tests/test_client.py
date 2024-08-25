#!/usr/bin/env python3
"""Unit and integration tests for client module"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
import requests
from typing import Dict, List


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google"),
        ("abc"),
        ("")  # Test with empty string
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json):
        """Test GithubOrgClient.org method"""
        test_class = GithubOrgClient(org_name)
        test_class.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test _public_repos_url property"""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/orgs/testorg/repos"}
            test_class = GithubOrgClient("testorg")
            result = test_class._public_repos_url
            self.assertEqual(result,
                             "https://api.github.com/orgs/testorg/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method"""
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://test_url.com"
            test_class = GithubOrgClient("testorg")
            result = test_class.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),  # Test with empty repo
        ({"license": None}, "my_license", False),  # Test with None license
        ({"license": {"key": "my_license"}}, "", False)
    ])
    def test_has_license(self, repo: Dict, license_key: str, expected: bool):
        """Test has_license method"""
        test_class = GithubOrgClient("testorg")
        result = test_class.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up for the integration tests"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Side effect function for mock get"""
            mock_response = Mock()
            if url.endswith("/orgs/google"):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith("/orgs/google/repos"):
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down after the integration tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos method"""
        test_class = GithubOrgClient("google")
        result = test_class.public_repos()
        self.assertEqual(result, self.expected_repos)

        # Test that the mocked method was called exactly once
        self.mock_get.assert_called_once()

    def test_public_repos_with_license(self):
        """Integration test for public_repos method with license"""
        test_class = GithubOrgClient("google")
        result = test_class.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)

        # Test that the mocked method was called exactly once
        self.mock_get.assert_called_once()

    def test_public_repos_with_invalid_license(self):
        """Test public_repos with an invalid license"""
        test_class = GithubOrgClient("google")
        result = test_class.public_repos(license="invalid_license")
        self.assertEqual(result, [])  # Should return an empty list

    def test_public_repos_with_invalid_org(self):
        """Test public_repos with an invalid organization"""
        test_class = GithubOrgClient("invalid_org")
        result = test_class.public_repos()
        self.assertEqual(result, [])  # Should return an empty list


if __name__ == '__main__':
    unittest.main()
