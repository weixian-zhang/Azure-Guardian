
from argparse import ArgumentError
from distutils.command.config import config
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import log
import time

config_key_db_name = 'DB_NAME'
config_key_db_connstring = 'DB_CONN_STRING'
config_key_keyvault_name = 'KEYVAULT_NAME'
config_key_resource_scan_interval_mins = 'RESOURCE_SCAN_INTERVAL_MINS'
config_key_azidenity_tenantid = 'AZURE_TENANT_ID'
config_key_azidenity_clientid = 'AZURE_CLIENT_ID'
config_key_azidenity_clientsecret = 'AZURE_CLIENT_SECRET'

class AppConfig:


    def __init__(self, dbName = '', dbConnstring = '', resourceScanIntervalMins = 10,
    azidenityTenantId = '', azidenityClientId = '', azidenityClientSecret = '') -> None:

        #if .env exist
        load_dotenv()


        self.dbName= dbName
        self.dbConnstring = dbConnstring
        self.resourceScanIntervalMins = resourceScanIntervalMins
        self.azidenityTenantId = azidenityTenantId
        self.azidenityClientId= azidenityClientId
        self.azidenityClientSecret= azidenityClientSecret

    def load_config(self):
        
        loadConfigSuccess = False

        
        while not loadConfigSuccess:

            if self.load_from_environ():
                loadConfigSuccess = True
            else:
                if self.load_from_akv():
                    loadConfigSuccess = True

            if not loadConfigSuccess:
                time.sleep(3)


    def load_from_environ(self) -> bool:

        environLoader =  EnvironLoader()

        environConfig = environLoader.load_config()

        if self.checkDBNameConnStringExists(environConfig):

                self.set_environ_azclientidsecret()
                return True

        return False

    def load_from_akv(self) -> bool:

        akvLoader = KeyVaultLoader()

        akvConfig =  akvLoader.load_config()

        if self.checkDBNameConnStringExists(akvConfig):
            self.set_environ_azclientidsecret(akvConfig)
            return True

        return False



    # if managed identity is not used, switch to service principal
    # azure.identity.EnvironmentCredential will check environ for tenant id, client id and client secret
    def set_environ_azclientidsecret(self) -> None:
        
        os.environ.setdefault(config_key_azidenity_tenantid, self.azidenityTenantId) 
        os.environ.setdefault(config_key_azidenity_clientid, self.azidenityClientId)
        os.environ.setdefault(config_key_azidenity_clientsecret, self.azidenityClientSecret)

    def checkDBNameConnStringExists(self, appconfig):

        props = vars(appconfig)

        if props['dbName'] == '' or props['dbConnstring'] == '':
            return False

        return True         
       

class ConfigLoader(ABC):

    @abstractmethod
    def load_config() -> AppConfig:
        pass

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


    def isAKVNameExists(self, akvName):

        if akvName == '':
            return False

        return True
    
