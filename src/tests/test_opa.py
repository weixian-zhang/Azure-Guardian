import unittest
from unittest.mock import Mock, patch
from requests import Timeout

def load_shared_modules():
    import os
    import sys
    # adding shared folder path to system paths
    sharedPath = os.path.join(os.getcwd(),'src', 'shared')
    sys.path.insert(1,sharedPath)
load_shared_modules()

from config import AppConfig, ConfigLoader
from db import DB
from opa import Opa, PolicyUnitOfWork


class OPATest(unittest.TestCase):

    def setUp(self) -> None:
        self.rego = '''
                package microsoft.compute.nic.unattached

                allow = {
                    allow = true
                }
            '''

        self.config: AppConfig
        
        configLoader = ConfigLoader()
        self.config = configLoader.load_config()

        db = Mock()

        self.policyUOW = PolicyUnitOfWork(self.config, db)


    @patch('requests.get', side_effect=Timeout())
    def test_is_server_ready_timeout(self, mock_request):
        
        expected = False

        opa = Opa()

        result = opa.is_server_ready()

        self.assertEqual(result, expected)

    def test_policy_unitofwork_create_or_update_policy_invalid_package_name(self):

        with patch('opa.Opa.validate_package_name') as validate_package_name:
            validate_package_name.return_value = False
        
            expected = False

            resourceProvider = 'microsoft.compute.vm'
            desc = 'a policy'
            username = 'johndoe'

            ok, _ = self.policyUOW.create_or_update_policy(resourceProvider, self.rego, desc, username)

            self.assertEqual(ok, expected)

    def test_policyunitofwork_create_or_update_policy_opa_addupdate_policy_fail(self):
    
        with patch('opa.Opa.add_update_policy') as add_update_policy:

            add_update_policy.return_value = False, Exception('DB not contactable')
        
            resourceProvider = 'microsoft.compute.vm'
            desc = 'a policy'
            username = 'johndoe'

            ok, err = self.policyUOW.create_or_update_policy(resourceProvider, self.rego, desc, username)

            expected = False

            self.assertEqual(ok, expected)
            self.assertNotEqual(err, None)


        
