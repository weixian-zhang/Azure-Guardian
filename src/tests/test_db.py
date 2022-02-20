import unittest
from unittest.mock import Mock, patch

def load_shared_modules():
    import os
    import sys
    # adding shared folder path to system paths
    sharedPath = os.path.join(os.getcwd(),'src', 'shared')
    sys.path.insert(1,sharedPath)
load_shared_modules()

from config import ConfigLoader, AppConfig
from db import Policy

class DBTest(unittest.TestCase):

    def setUp(self) -> None:
        self.rego = '''
                        package microsoft.compute.nic.unattached

                        allow = {
                            allow = true
                        }
                    '''
    
    def test_is_policy_exists_not_exists(self):

        with patch("shared.db.PostgreSql.is_policy_exists") as is_policy_exists:
            is_policy_exists.return_value = False, None

            expected = False
            exists, policy = is_policy_exists('microsoft.compute.nic.unattached')

        self.assertEqual(exists, expected)
        self.assertEqual(policy, None)

    
    def test_is_policy_exists_exists(self):

        with patch("shared.db.PostgreSql.is_policy_exists") as is_policy_exists:
            is_policy_exists.return_value = True, Policy()

            expected = True
            exists, policy = is_policy_exists('microsoft.compute.nic.unattached')

        self.assertEqual(exists, expected)
        self.assertIsInstance(policy, Policy)

    def test_create_or_update_policy_with_no_existing_policy(self): ##, resourceProvider, packageName, desc, username, rego):

        with patch("shared.db.PostgreSql.is_policy_exists") as is_policy_exists:
            is_policy_exists.return_value = False, None

            with patch("shared.db.PostgreSql.update_policy") as update_policy:
                update_policy.return_value = True

                with patch("shared.db.PostgreSql.create_or_update_policy") as create_or_update_policy:
                    create_or_update_policy.return_value = True

                    resourceProvider = 'microsoft.compute.nic.unattached'
                    packageName = 'microsoft.compute.nic.unattached'
                    desc = 'a policy'
                    username = 'john doe'
                    rego = self.rego
                    

                    expected = True
                    result = create_or_update_policy(resourceProvider, packageName, desc, username, rego)

                    self.assertEqual(result, expected)

    def test_create_or_update_policy_with_existing_policy(self): ##, resourceProvider, packageName, desc, username, rego):

        with patch("shared.db.PostgreSql.is_policy_exists") as is_policy_exists:
            is_policy_exists.return_value = True, Policy()

            with patch("shared.db.PostgreSql.update_policy") as update_policy:
                update_policy.return_value = True

                with patch("shared.db.PostgreSql.create_or_update_policy") as create_or_update_policy:
                    create_or_update_policy.return_value = True

                    resourceProvider = 'microsoft.compute.nic.unattached'
                    packageName = 'microsoft.compute.nic.unattached'
                    desc = 'a policy'
                    username = 'john doe'
                    rego = self.rego

                    expected = True
                    result = create_or_update_policy(resourceProvider, packageName, desc, username, rego)

                    self.assertEqual(result, expected)

