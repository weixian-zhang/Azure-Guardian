from argparse import ArgumentError
from resource_scanner import ResourceScanner
from opa_manager import OpaManager

import os
import sys
import json
from dotenv import load_dotenv

class App:

    def __init__(self) -> None:

        try:
            #if .env exist
            load_dotenv()

            self.policy_eval_test()

            self.app_config = AppConfig()
            self.app_config.load_from_envvar()

            self.rsc_scanner = ResourceScanner()

            #subs = ['ee611083-4581-4ba1-8116-a502d4539206']

            #az_subs = rsc_scanner.get_all_subscription_ids()

            # sub_ids = []
            # for sub in az_subs:
            #     sub_ids.append(sub.id)

            #argresult = self.rsc_scanner.get_all_resources(subs)
            
            # j = argresult.toJson()

            # print(j)


            

        except (Exception) as e:
            #Todo: log to mongo
            print(e, sys.stderr)
            raise

    def policy_eval_test(self):

        policy = '''

            package test.2

            allow {
                is_compliance = is_tenantId_allowed
            }
            
            is_tenantId_allowed { 
                input.tenantId == "72f988bf-86f1-41af-91ab-2d7cd011db47" 
            }
	    '''

        input = '''
            {
                "id": "/subscriptions/ee611083-4581-4ba1-8116-a502d4539206/resourceGroups/AzureBackupRG_southeastasia_1/providers/Microsoft.Compute/restorePointCollections/AzureBackup_vm-web_140738144265919",
                "name": "AzureBackup_vm-web_140738144265919",
                "type": "microsoft.compute/restorepointcollections",
                "tenantId": "72f988bf-86f1-41af-91ab-2d7cd011db47",
                "kind": "",
                "location": "southeastasia",
                "resourceGroup": "azurebackuprg_southeastasia_1",
                "subscriptionId": "ee611083-4581-4ba1-8116-a502d4539206",
                "managedBy": "",
                "sku": null,
                "plan": null,
                "properties": {
                    "source": {
                        "id": "/subscriptions/ee611083-4581-4ba1-8116-a502d4539206/resourceGroups/rgGCCSHOL/providers/Microsoft.Compute/virtualMachines/vm-web"
                    }
                },
                "tags": null
            }
        '''
        opa_manager = OpaManager()

        opa_manager.add_policy(policy, "test")

        opa_manager.eval_policy(input, "test")

        


class AppConfig:

    def __init__(self) -> None:
        self.mongo_connstring = ''
        self.resource_scan_interval_mins = 10
        self.resource_scanner_azidenity_tenantid = ''
        self.resource_scanner_azidenity_clientid= ''
        self.resource_scanner_azidenity_clientsecret= ''

    def load_from_envvar(self):

       mongo_connstring_envar = os.environ.get('mongo_connstring')

       if mongo_connstring_envar == None:
           raise ArgumentError('Environment variable \'mongo_connstring\' cannot be found. Azure Guardian uses MongoDb.')

       self.mongo_connstring = mongo_connstring_envar

       rsc_scan_in_mins_envar = os.environ.get('resource_scan_interval_mins')
       if rsc_scan_in_mins_envar != None:
           self.resource_scan_interval_mins = rsc_scan_in_mins_envar

       self.resource_scanner_azidenity_tenantid = os.environ.get('resource_scanner_azidenity_tenantid')
       self.resource_scanner_azidenity_clientid = os.environ.get('resource_scanner_azidenity_clientid')
       self.resource_scanner_azidenity_clientsecret = os.environ.get('resource_scanner_azidenity_clientsecret')


