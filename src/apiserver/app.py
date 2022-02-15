import sys

def load_shared_modules():
    import sys
    import os
    # adding Folder_2 to the system path
    sharedModule = os.path.join(os.getcwd(),'src', 'shared')
    sys.path.insert(1, sharedModule)

load_shared_modules()
from config import ConfigLoader

from db import PostgreSql
from policy_unitofwork import PolicyUnitOfWork

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

            db = PostgreSql(self.appConfig)

            uowPolicy = PolicyUnitOfWork(self.appConfig, db)

            uowPolicy.create_or_update_policy('Microsoft.Compute/VirtualMachines', App.policy, 'abc', 'abc')

        except (Exception) as e:
            #Todo: log to mongo
            print(e, sys.stderr)
            raise

        



