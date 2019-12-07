""" Tests for app_utils """

# Python
import unittest

# Libraries
import mock

# Project
import app_utils


class TestGetUrl(unittest.TestCase):
    """ Tests for app_utils.get_url() """

    def test_no_url(self):
        """ No url provided -- throw exception """
        args = mock.Mock()
        args.url = None
        env = {}
        with self.assertRaises(Exception):
            app_utils.get_url(args, env=env)

    def test_arg_url(self):
        """ URL from arg.url """
        args = mock.Mock()
        args.url = "https://example.com"
        env = {}
        self.assertEqual("https://example.com",
                         app_utils.get_url(args, env))

    def test_env_url(self):
        """ URL from passed environment """
        args = mock.Mock()
        args.url = None
        env = {"DYNALIST_URL": "https://example.com"}
        self.assertEqual("https://example.com",
                         app_utils.get_url(args, env))


class TestGetToken(unittest.TestCase):
    """ Tests for app_utils.get_token() """

    def test_no_token(self):
        """ No token provided -- throw exception """
        args = mock.Mock()
        args.token = None
        env = {}
        with self.assertRaises(Exception):
            app_utils.get_token(args, env=env)

    def test_arg_token(self):
        """ Token from arg.token """
        args = mock.Mock()
        args.token = "abcdef123"
        env = {}
        self.assertEqual("abcdef123",
                         app_utils.get_token(args, env))

    def test_env_token(self):
        """ Token from passed environment """
        args = mock.Mock()
        args.token = None
        env = {"DYNALIST_TOKEN": "abcdef123"}
        self.assertEqual("abcdef123",
                         app_utils.get_token(args, env))


# vim: foldmethod=indent
