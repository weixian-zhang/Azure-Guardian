from typing import Any
import azure.mgmt.resourcegraph as arg
import json

from azure_identity_credential_wrapper import AzureIdentityCredentialAdapter

from azure.mgmt.resource import SubscriptionClient
from azure.identity import DefaultAzureCredential, VisualStudioCodeCredential

class ResourceGatherer:

    def __init__(self) -> None:
        self.resources_dict = {}

    def get_all_resources(self, az_sub_ids) -> 'ARGResult':

        azcred = DefaultAzureCredential()

        argClient = arg.ResourceGraphClient(azcred);

        arg_result = self.get_resources_handle_pagination(argClient, az_sub_ids)

        return arg_result


    def get_all_subscription_ids(self):

        azcred = AzureIdentityCredentialAdapter(DefaultAzureCredential())

        subsList = []

        #if no subscription ids pass in, get all subscription ids
        subClient = SubscriptionClient(azcred)

        subRaw = [];
        for sub in subClient.subscriptions.list():
            subRaw.append(sub.as_dict())

        subsList = []
        for sub in subRaw:
            id = sub.get('subscription_id')
            name = sub.get('display_name')
            subsList.append(AzureSubscription(name, id))

        return subsList

    def get_resources_handle_pagination(self, argClient, az_sub_ids) -> 'ARGResult':

        arg_query = 'Resources'
        page_size = 1000
        skip = 0

        argQueryOptions = arg.models.QueryRequestOptions(top= page_size, skip = skip, result_format="objectArray")

        # Create query
        argQuery = arg.models.QueryRequest(subscriptions=az_sub_ids, query=arg_query, options=argQueryOptions)

        # Run query
        query_response = argClient.resources(argQuery)
        # result as dictionary
        result_dict = query_response.as_dict()

        current_count = result_dict['count']

        #arg resource result
        arg_result = self.create_arg_result(result_dict)

        while current_count == page_size:

            skip += current_count

            argQueryOptions = arg.models.QueryRequestOptions(top= page_size, skip = skip, result_format="objectArray")

            # Create query
            argQuery = arg.models.QueryRequest(subscriptions=az_sub_ids, query=arg_query, options=argQueryOptions)

            query_response = argClient.resources(argQuery)

            #result as dictionary
            result_dict = query_response.as_dict()

            current_count = result_dict['count']

            temp_result = self.create_arg_result(result_dict)

            #merge result
            arg_result.arg_resources = arg_result.arg_resources + temp_result.arg_resources

        return arg_result

    def create_arg_result(self, result_dict):

        arg_result = ARGResult(result_dict['total_records'])

        for rsc in result_dict['data']:

            argrsc = ARGResource(rsc['id'], rsc['name'], rsc['type'], rsc['tenantId'], rsc['kind']
            , rsc['location'], rsc['resourceGroup'], rsc['subscriptionId'],
             rsc['managedBy'], rsc['sku'], rsc['plan'], rsc['properties'], rsc['tags'])

            arg_result.arg_resources.append(argrsc)

        return arg_result


class ARGResult:
    def __init__(self, total_records) -> None:
        self.total_records = total_records
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

class AzureSubscription:

    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id


