#!/usr/bin/env python3
"""test utils  """
import unittest
from unittest.mock import patch
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


if __name__ == "__main__":
    unittest.main()
