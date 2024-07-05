#!/usr/bin/env python3
"""test utils  """
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from utils import get_json


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case for the GithubOrgClient class in the client module.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        Parameters:
        org_name (str): The name of the organization to test.
        mock_get_json (Mock): The mocked get_json method.
        """
        expected_result = {"login": org_name}
        mock_get_json.return_value = expected_result
        client = GithubOrgClient(org_name)
        result = client.org
        url = "https://api.github.com/orgs/"
        mock_get_json.assert_called_once_with(f"{url}{org_name}")
        self.assertEqual(result, expected_result)

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that GithubOrgClient._public_repos_url
        returns the correct URL.
        """
        url = "https://api.github.com/orgs/google/repos"
        mock_org.return_value = {"repos_url": url}
        client = GithubOrgClient("google")
        result = client._public_repos_url
        self.assertEqual(result, url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns
        the expected list of repositories.
        Parameters:
        mock_get_json (Mock): The mocked get_json method.
        """
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload
        mystring = 'client.GithubOrgClient._public_repos_url'
        url = 'https://api.github.com/orgs/google/repos'
        with patch(mystring, new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = url
            client = GithubOrgClient("google")
            result = client.public_repos()
            expected_result = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_result)
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": None}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that GithubOrgClient.has_license returns the correct value.

        Parameters:
        repo (dict): The repository information to test.
        license_key (str): The license key to check for.
        expected (bool): The expected result of has_license.
        """
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
