from argparse import ArgumentError
from resource_scanner import ResourceScanner
import os
import sys
from dotenv import load_dotenv

class App:

    def __init__(self) -> None:

        try:
            #if .env exist
            load_dotenv()

            self.app_config = AppConfig()
            self.app_config.load_from_envvar()

            self.rsc_scanner = ResourceScanner()

        except (Exception) as e:
            #Todo: log to mongo
            print(e, sys.stderr)
            raise

    #def start(self):

        # try:



        #     #subs = ['ee611083-4581-4ba1-8116-a502d4539206']

        #     # az_subs = rsc_scanner.get_all_subscription_ids()

        #     # sub_ids = []
        #     # for sub in az_subs:
        #     #     sub_ids.append(sub.id)

        #     # rsc_scanner.get_all_resources(sub_ids)

        # except (Exception) as e:
        #     #Todo: log to mongo
        #     print(e, sys.stderr)
        #     raise


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


