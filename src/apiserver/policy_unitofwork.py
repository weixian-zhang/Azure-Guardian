from sre_constants import SUCCESS

from app import load_shared_modules
load_shared_modules()
from opa import Opa
from db import PostgreSql
from config import AppConfig
import log

class PolicyUnitOfWork:

    def __init__(self, config: AppConfig):
        
        self.db = PostgreSql(config)

        self.opa = Opa()

    def create_policy(self, resourceProvider, rego, desc, username):

        packageNameOK, packageName = self.opa.get_package_name(rego)

        if not packageNameOK:
            msg = f'Not able to read package name for {rego}. Package name has to be present and unique.'
            log.error(msg)
            return False, msg

        packageNameValid = self.opa.validate_package_name(packageName)
        if not packageNameValid:
            msg = f'Package name {packageName}, cannot contain numbers'
            log.error(msg)
            return False, msg
        
        createPolicyOK, err = self.opa.add_update_policy(rego)
        if not createPolicyOK:
            log.error(err)
            return False, err

        succeed = self.db.create_update_policy(resourceProvider=resourceProvider, packageName=packageName, rego=rego, \
            desc=desc, username=username )

        #rollback policy creation in OPA
        if not succeed:
            if not self.opa.delete_policy(packageName):
                log.error('Rollback of policy creation in OPA unsuccessful')

        