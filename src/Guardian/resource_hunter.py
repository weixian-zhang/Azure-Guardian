from typing import Any
import azure.mgmt.resourcegraph as arg
import json

from azure_identity_credential_wrapper import AzureIdentityCredentialAdapter

from azure.mgmt.resource import SubscriptionClient
from azure.identity import DefaultAzureCredential, VisualStudioCodeCredential

class ResourceHunter:

    def get_all_resources(self, subs) -> 'ARGResult':

        azcred = DefaultAzureCredential()#AzureIdentityCredentialAdapter(DefaultAzureCredential())

        subsList = self.get_subscription_ids(azcred, subs)

        argClient = arg.ResourceGraphClient(azcred);

        strQuery = 'Resources'
        argQueryOptions = arg.models.QueryRequestOptions(result_format="objectArray")

        # Create query
        argQuery = arg.models.QueryRequest(subscriptions=subsList, query=strQuery, options=argQueryOptions)

        # Run query
        jsonResult = argClient.resources(argQuery)

        result_dict = jsonResult.as_dict()

        arg_result = self.create_arg_result(result_dict)

        return arg_result

    def create_arg_result(self, result_dict):

        arg_result = ARGResult(result_dict['total_records'], result_dict['result_truncated'])

        for rsc in result_dict['data']:

            argrsc = ARGResource(rsc['id'], rsc['name'], rsc['type'], rsc['tenantId'], rsc['kind']
            , rsc['location'], rsc['resourceGroup'], rsc['subscriptionId'],
             rsc['managedBy'], rsc['sku'], rsc['plan'], rsc['properties'], rsc['tags'])

            arg_result.arg_resources.append(argrsc)

        return arg_result


    def get_subscription_ids(self, azcred, subscriptions):

        subsList = []

        if(len(subscriptions) > 0):
            for sub in subscriptions:
                print(sub)
                subsList.append(sub)
            return subsList

        #if no subscription ids pass in, get all subscription ids
        subClient = SubscriptionClient(azcred)

        subRaw = [];
        for sub in subClient.subscriptions.list():
            subRaw.append(sub.as_dict())

        subsList = []
        for sub in subRaw:
            subsList.append(sub.get('subscription_id'))

        return subsList

class ARGResult:
    def __init__(self, total_records, result_truncated) -> None:
        self.total_records = total_records
        self.result_truncated = result_truncated
        self.arg_resources = []

class ARGResource:
    def __init__(self, id, name, type, tenantId, kind, location,
     resourceGroup, subscriptionId, managedBy, sku, plan, properties, tags) -> None:
        self.id = id
        self.name = name
        self.type = type
        self.tenantId = tenantId
        self.kind = kind
        self.location = location
        self.resourceGroup = resourceGroup
        self.subscriptionId = subscriptionId
        self.managedBy = managedBy
        self.sku = sku
        self.plan = plan
        self.properties = properties
        self.tags = tags


