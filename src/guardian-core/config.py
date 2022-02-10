
from argparse import ArgumentError
from distutils.command.config import config
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import log
import time

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

        #if .env exist
        load_dotenv()

        self.dbName= dbName
        self.dbConnstring = dbConnstring
        self.resourceScanIntervalMins = resourceScanIntervalMins
        self.azidenityTenantId = azidenityTenantId
        self.azidenityClientId= azidenityClientId
        self.azidenityClientSecret= azidenityClientSecret

class ConfigLoader:

    def load_config(self) -> AppConfig:
        
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

        resourceScanIntervalMins = os.environ.get(config_key_resource_scan_interval_mins)
        if resourceScanIntervalMins == None:
           self.resourceScanIntervalMins = 10
        else:
           self.resourceScanIntervalMins = resourceScanIntervalMins

        tenantId = os.environ.get(config_key_azidenity_tenantid)
        clientId = os.environ.get(config_key_azidenity_clientid)
        clientsecret = os.environ.get(config_key_azidenity_clientsecret)

        if self.checkDBNameConnStringExists(dbName, dbConnStr):
            self.set_environ_azserviceprincpal_cred(tenantId, clientId, clientsecret)
            return True, AppConfig(dbName, dbConnStr, resourceScanIntervalMins, tenantId, clientId, clientsecret)

        return False, None

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

            resourceScanIntervalMins = akvSecretClient.get_secret(config_key_resource_scan_interval_mins).value
            if resourceScanIntervalMins == None:
                self.resourceScanIntervalMins = 10
            else:
                self.resourceScanIntervalMins = resourceScanIntervalMins

            tenantId = akvSecretClient.get_secret(config_key_azidenity_tenantid).value
            clientId = akvSecretClient.get_secret(config_key_azidenity_clientid).value
            clientsecret = akvSecretClient.get_secret(config_key_azidenity_clientsecret).value

            if self.checkDBNameConnStringExists(dbName, dbConnStr):
                self.set_environ_azserviceprincpal_cred(tenantId, clientId, clientsecret)
                return True, AppConfig(dbName, dbConnStr, resourceScanIntervalMins, tenantId, clientId, clientsecret)

        except (Exception) as e:
            log.error(e)

        return False, None

    def isAKVNameExists(self, akvName):

        if akvName == '':
            return False

        return True


    # if managed identity is not used, switch to service principal
    # azure.identity.EnvironmentCredential will check environ for tenant id, client id and client secret
    def set_environ_azserviceprincpal_cred(self, tenantid, clientid, clientsecret) -> None:
        
        os.environ.setdefault(config_key_azidenity_tenantid, tenantid) 
        os.environ.setdefault(config_key_azidenity_clientid, clientid)
        os.environ.setdefault(config_key_azidenity_clientsecret, clientsecret)

    def checkDBNameConnStringExists(self, dbName, dbConnString):

        #props = vars(appconfig)

        if dbName == None or dbConnString == None:
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
    
