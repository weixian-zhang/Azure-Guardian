
from argparse import ArgumentError
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class AppConfig:

    def __init__(self) -> None:

        #if .env exist
        load_dotenv()

        self.dbName= ''
        self.dbConnstring = ''
        self.keyvault_name = ''
        self.resourceScanIntervalMins = 10
        self.azidenityTenantId = ''
        self.azidenityClientId= ''
        self.azidenityClientSecret= ''

    def load_config(self):
        

        envarLoader =  EnvarLoader()
        envarConfig = envarLoader.load_config()

        if not self.checkConfigSettingsExists(envarConfig):
            pass

            akvLoader = KeyVaultLoader()

            akvConfigObj =  akvLoader.load_config()

            if not self.checkConfigSettingsExists(akvConfigObj):
                raise ArgumentError('Missing config settings dbName or dbConnstring')



    def checkConfigSettingsExists(self, appconfig):

        props = vars(appconfig)

        if props['dbName'] == '' or props['dbConnstring'] == '':
            return False

        return True
            
       

class ConfigLoader(ABC):

    @abstractmethod
    def load_config() -> AppConfig:
        pass

class EnvarLoader(ConfigLoader):

    def load_config(self) -> AppConfig:

        appConfig = AppConfig()

        appConfig.dbName = os.environ.get('DB_NAME')

        appConfig.dbConnstring = os.environ.get('DB_CONN_STRING')

        appConfig.keyvault_name = os.environ.get('KEYVAULT_NAME')

    #    if dbConnString == None:
    #        raise ArgumentError('Environment variable \'dbConnstring\' cannot be found. Azure Guardian uses MongoDb.')

        appConfig.resourceScanIntervalMins = os.environ.get('RESOURCE_SCANiNTERVAL_MINS')

    #    if rsc_scan_in_mins_envar != None:
    #        self.resource_scan_interval_mins = rsc_scan_in_mins_envar

        appConfig.azidenityTenantId = os.environ.get('AZURE_TENANT_ID')
        appConfig.azidenityClientId = os.environ.get('AZURE_CLIENT_ID')
        appConfig.azidenityClientSecret = os.environ.get('AZURE_CLIENT_SECRET')

class KeyVaultLoader(ConfigLoader):

    def load_config() -> AppConfig:
        pass

    
