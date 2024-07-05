#!/usr/bin/env python3
"""test utils  """
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from utils import get_json
import fixtures


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


@parameterized_class([
    {"org_payload": fixtures.TEST_PAYLOAD[0][0],
     "repos_payload": fixtures.TEST_PAYLOAD[0][1],
     "expected_repos": fixtures.TEST_PAYLOAD[0][2],
     "apache2_repos": fixtures.TEST_PAYLOAD[0][3]}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test case for the GithubOrgClient class in the client module.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the class method for the integration test.
        """
        cls.get_patcher = patch('requests.get',
                                side_effect=cls.mocked_requests_get)
        cls.mocked_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the class method for the integration test.
        """
        cls.get_patcher.stop()

    @staticmethod
    def mocked_requests_get(url):
        """
        Mocked requests.get method to return example payloads.
        """
        if url == "https://api.github.com/orgs/google":
            return MockResponse(fixtures.TEST_PAYLOAD[0][0])
        elif url == "https://api.github.com/orgs/google/repos":
            return MockResponse(fixtures.TEST_PAYLOAD[0][1])
        return MockResponse(None, 404)

    def test_public_repos(self):
        """
        Test that GithubOrgClient.public_repos returns
        the expected list of repositories.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test that GithubOrgClient.public_repos returns
        the expected list of repositories
        with the specified license.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"),
                         self.apache2_repos)


class MockResponse:
    """
    Mock response class to simulate requests responses.
    """
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


if __name__ == "__main__":
    unittest.main()
