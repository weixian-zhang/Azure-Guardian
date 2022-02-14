from argparse import ArgumentError
from azresource_scanner import AzResourceScanner
import sys
from dotenv import load_dotenv

def load_shared_modules():
    import sys
    import os
    # adding Folder_2 to the system path
    sharedPath = os.path.join(os.getcwd(),'src', 'shared')
    sys.path.insert(1,sharedPath)

load_shared_modules()
from config import ConfigLoader, AppConfig
from db import PostgreSql

class App:

    def __init__(self) -> None:

        self.appconfig = None

        try:
            #self.policy_eval_test()

            configLoader = ConfigLoader()

            self.appConfig = configLoader.load_config()

            db = PostgreSql(self.appConfig)

            # db.create_policy('Microsoft.Storage/Disks','f','f','f','f')

            # db.create_policy('Microsoft.Compute/VirtualMachines','sads','fasdas','f','f')

            # policies = db.list_all_policies()

            # for p in policies:
            #     print(p.resource_provider)
            #     print(p.name)

            #db.update_policy('da', 'updated')

            #db.delete_policy('da')
          

            #self.rsc_scanner = ResourceScanner()

            #subs = ['ee611083-4581-4ba1-8116-a502d4539206']

            #az_subs = rsc_scanner.get_all_subscriptions_by_azidenity()

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

        isPolicyExist = opa_manager.is_policy_exist("azdisk.attachornot")

        # opa_manager.add_policy(policy, "test")

        # opa_manager.eval_policy(input, "test")

        



