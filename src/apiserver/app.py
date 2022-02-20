import json
import sys

def load_shared_modules():
    import sys
    import os
    # adding Folder_2 to the system path
    sharedModule = os.path.join(os.getcwd(),'src', 'shared')
    sys.path.insert(1, sharedModule)

load_shared_modules()
from config import ConfigLoader

from azresource import AzResource, AzureSubscription

def load_shared_modules():
    import sys
    import os
    # adding Folder_2 to the system path
    sharedPath = os.path.join(os.getcwd(),'src', 'shared')
    sys.path.insert(1,sharedPath)

load_shared_modules()
from config import ConfigLoader, AppConfig
from db import PostgreSql
from utils import to_json
from opa import PolicyUnitOfWork

class App:

    policy = '''

            package test.a.b.c

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

    def __init__(self) -> None:

        self.appconfig = None

        try:
            #self.policy_eval_test()

            configLoader = ConfigLoader()

            self.appConfig = configLoader.load_config()

            # opa = PolicyUnitOfWork(self.appConfig, PostgreSql(self.appConfig))

            # opa.create_or_update_policy('dasd', App.policy, 'das', 'dsasa')

            # subs: AzureSubscription
            # subs =  azrsc.get_all_subscriptions_by_azidenity()
            # subIds = []
            # for s in subs:
            #     subIds.append(s.id)
            # subIds = ['ee611083-4581-4ba1-8116-a502d4539206']

            # result =  azrsc.get_all_resources(subIds)

            # print(to_json(result.arg_resources, default=lambda o: o.__dict__, 
            # sort_keys=True, indent=4))

        except (Exception) as e:
            #Todo: log to mongo
            print(e, sys.stderr)
            raise

        



