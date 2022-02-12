
from argparse import ArgumentError
from distutils.command.config import config
import os
from dotenv import load_dotenv
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import log
import time
from utils import Utils

config_key_db_name = 'DB-NAME'
config_key_db_connstring = 'DB-CONN-STRING'
config_key_keyvault_name = 'KEYVAULT-NAME'
config_key_resource_scan_interval_mins = 'RESOURCE-SCAN-INTERVAL-MINS'
config_key_azidenity_tenantid = 'AZURE-TENANT-ID'
config_key_azidenity_clientid = 'AZURE-CLIENT-ID'
config_key_azidenity_clientsecret = 'AZURE-CLIENT-SECRET'

class AppConfig:


    def __init__(self, dbName = '', dbConnstring = '', resourceScanIntervalMins = 10,
    azidenityTenantId = '', azidenityClientId = '', azidenityClientSecret = '') -> None:

        self.dbName= dbName
        self.dbConnstring = dbConnstring
        self.resourceScanIntervalMins = resourceScanIntervalMins
        self.azidenityTenantId = azidenityTenantId
        self.azidenityClientId= azidenityClientId
        self.azidenityClientSecret= azidenityClientSecret

class ConfigLoader:

    def load_config(self) -> AppConfig:

        #if .env exist
        load_dotenv()
        
        loadConfigSuccess = False
        ok = False
        appconfig = None

        
        while not ok:

            ok, appconfig = self.load_from_environ()

            if ok:
                return appconfig
            else:
                ok, appconfig = self.load_from_akv()
                if ok:
                    return appconfig

            log.info('DbName and DB connection string settings are not found in environment variables or Azure Key Vault')

            time.sleep(3)


    def load_from_environ(self) -> bool:

        dbName =  os.environ.get(config_key_db_name)
        dbConnStr =  os.environ.get(config_key_db_connstring)

        if not self.isDBNameConnStringExists(dbName, dbConnStr):
            return False, None

        resourceScanIntervalMins = os.environ.get(config_key_resource_scan_interval_mins)
        if resourceScanIntervalMins == None:
           self.resourceScanIntervalMins = 10
        else:
           self.resourceScanIntervalMins = resourceScanIntervalMins

        tenantId = os.environ.get(config_key_azidenity_tenantid)
        clientId = os.environ.get(config_key_azidenity_clientid)
        clientsecret = os.environ.get(config_key_azidenity_clientsecret)

        self.set_environ_azserviceprincpal_cred(tenantId, clientId, clientsecret)
        return True, AppConfig(dbName, dbConnStr, resourceScanIntervalMins, tenantId, clientId, clientsecret)

    def load_from_akv(self) -> bool:

        azcred = DefaultAzureCredential()

        akvName = os.environ.get(config_key_keyvault_name)

        if not self.isAKVNameExists(akvName):
            raise ArgumentError('Azure Key Vault name does not exist')

        akvUrl = f"https://{akvName}.vault.azure.net"

        akvSecretClient = SecretClient(vault_url=akvUrl, credential=azcred)

        try:

            dbName =  akvSecretClient.get_secret(config_key_db_name).value
            dbConnStr =  akvSecretClient.get_secret(config_key_db_connstring).value

            if not self.isDBNameConnStringExists(dbName, dbConnStr):
                return False, None

        except (Exception) as e:
            log.error(e)
            return False, None
   

        def get_scan_internal(akvClient):
            try:
                resourceScanIntervalMins = akvClient.get_secret(config_key_resource_scan_interval_mins).value
                if not resourceScanIntervalMins:
                    return resourceScanIntervalMins
                pass
            except:
                return 10

        def get_tenantid(akvClient):
            try:
                tenantId = akvSecretClient.get_secret(config_key_azidenity_tenantid).value
                if not tenantId:
                    return tenantId
                pass
            except:
                return None

        def get_clientid(akvClient):
            try:
                clientId = akvSecretClient.get_secret(config_key_azidenity_clientid).value
                if not clientId:
                    return clientId
                pass
            except:
                return None

        def get_clientsecret(akvClient):
            try:
                clientsecret = akvSecretClient.get_secret(config_key_azidenity_clientsecret).value
                if not clientsecret:
                    return clientsecret
                pass
            except:
                return None

        resourceScanIntervalMins = get_scan_internal(akvSecretClient)
        tenantId = get_tenantid(akvSecretClient)
        clientId = get_clientid(akvSecretClient)
        clientsecret = get_clientsecret(akvSecretClient)
        
        self.set_environ_azserviceprincpal_cred(tenantId, clientId, clientsecret)
        return True, AppConfig(dbName, dbConnStr, resourceScanIntervalMins, tenantId, clientId, clientsecret)

    def isAKVNameExists(self, akvName):

        if not akvName:
            return False

        return True


    # if managed identity is not used, switch to service principal
    # azure.identity.EnvironmentCredential will check environ for tenant id, client id and client secret
    def set_environ_azserviceprincpal_cred(self, tenantid, clientid, clientsecret) -> None:

        if not Utils.is_none_or_empty_str(tenantid) and not Utils.is_none_or_empty_str(clientid) and not Utils.is_none_or_empty_str(clientsecret):
            os.environ.setdefault(config_key_azidenity_tenantid, tenantid) 
            os.environ.setdefault(config_key_azidenity_clientid, clientid)
            os.environ.setdefault(config_key_azidenity_clientsecret, clientsecret)

    def isDBNameConnStringExists(self, dbName, dbConnString):

        #props = vars(appconfig)

        if Utils.is_none_or_empty_str(dbName) or Utils.is_none_or_empty_str(dbConnString):
            return False

        return True    
       



class EnvironLoader(ConfigLoader):

    def load_config(self) -> AppConfig:

        #appConfig = AppConfig()

        # appConfig.dbName = os.environ.get(config_key_db_name)

        # appConfig.dbConnstring = os.environ.get(config_key_db_connstring)

        # appConfig.keyvault_name = os.environ.get(config_key_keyvault_name)

        # resourceScanIntervalMins = os.environ.get(config_key_resource_scan_interval_mins)

        # if resourceScanIntervalMins == None:
        #    self.resourceScanIntervalMins = 10
        # else:
        #    self.resourceScanIntervalMins = resourceScanIntervalMins

        # appConfig.azidenityTenantId = os.environ.get(config_key_azidenity_tenantid)
        # appConfig.azidenityClientId = os.environ.get(config_key_azidenity_clientid)
        # appConfig.azidenityClientSecret = os.environ.get(config_key_azidenity_clientsecret)

        dbName =  os.environ.get(config_key_db_name)
        dbConnStr =  os.environ.get(config_key_db_connstring)

        resourceScanIntervalMins = os.environ.get(config_key_resource_scan_interval_mins)
        if resourceScanIntervalMins == None:
           self.resourceScanIntervalMins = 10
        else:
           self.resourceScanIntervalMins = resourceScanIntervalMins

        azidenityTenantId = os.environ.get(config_key_azidenity_tenantid)
        azidenityClientId = os.environ.get(config_key_azidenity_clientid)
        azidenityClientSecret = os.environ.get(config_key_azidenity_clientsecret)

        return AppConfig(dbName, dbConnStr, resourceScanIntervalMins, azidenityTenantId, azidenityClientId, azidenityClientSecret)

class KeyVaultLoader(ConfigLoader):

    def load_config(self, ) -> AppConfig:
        
        azcred = DefaultAzureCredential()

        akvName = os.environ.get(config_key_keyvault_name)

        if not self.isAKVNameExists(akvName):
            raise ArgumentError('Azure Key Vault name does not exist')

        akvUrl = f"https://{akvName}.vault.azure.net"

        akvSecretClient = SecretClient(vault_url=akvUrl, credential=azcred)

        try:

            dbName =  akvSecretClient.get_secret(config_key_db_name).value
            dbConnStr =  akvSecretClient.get_secret(config_key_db_connstring).value

            resourceScanIntervalMins = akvSecretClient.get_secret(config_key_resource_scan_interval_mins).value
            if resourceScanIntervalMins == None:
                self.resourceScanIntervalMins = 10
            else:
                self.resourceScanIntervalMins = resourceScanIntervalMins

            azidenityTenantId = akvSecretClient.get_secret(config_key_azidenity_tenantid).value
            azidenityClientId = akvSecretClient.get_secret(config_key_azidenity_clientid).value
            azidenityClientSecret = akvSecretClient.get_secret(config_key_azidenity_clientsecret).value

            return AppConfig(dbName, dbConnStr, resourceScanIntervalMins, azidenityTenantId, azidenityClientId, azidenityClientSecret)

        except (Exception) as e:
            log.error(e)
            pass


    def isAKVNameExists(self, akvName):

        if akvName == '':
            return False

        return True
    
