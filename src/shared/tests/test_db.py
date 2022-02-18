# from distutils.command.config import config
# from distutils.core import setup
import unittest
from unittest import mock

import shared.log
from shared.config import ConfigLoader, AppConfig
from shared.db import Policy

class DBTest(unittest.TestCase):

    def setUp(self) -> None:
        pass
    
    def test_is_policy_exists_not_exists(self): #, resourceProvider, packageName, desc, username, rego):

        with mock.patch("shared.db.PostgreSql.is_policy_exists") as is_policy_exists:
            is_policy_exists.return_value = False, None

            expected = False
            exists, policy = is_policy_exists('microsoft.compute.nic.unattached')

        self.assertEqual(exists, expected)
        self.assertEqual(policy, None)

    def test_is_policy_exists_exists(self): #, resourceProvider, packageName, desc, username, rego):

        with mock.patch("shared.db.PostgreSql.is_policy_exists") as is_policy_exists:
            is_policy_exists.return_value = True, Policy()

            expected = True
            exists, policy = is_policy_exists('microsoft.compute.nic.unattached')

        self.assertEqual(exists, expected)
        self.assertIsInstance(policy, Policy)