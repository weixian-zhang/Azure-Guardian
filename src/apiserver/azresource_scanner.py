from typing import Any
import azure.mgmt.resourcegraph as arg
import json

from azure.mgmt.resource import SubscriptionClient
from azure.identity import DefaultAzureCredential, VisualStudioCodeCredential

class AzResourceScanner:

    def __init__(self) -> None:
        self.resources_dict = {}

    

    def get_all_resources(self, az_sub_ids) -> 'ARGResult':

        azcred = DefaultAzureCredential()

        argClient = arg.ResourceGraphClient(azcred)

        arg_result = self.get_resources_handle_pagination(argClient, az_sub_ids)

        return arg_result


    def get_all_subscriptions_by_azidenity(self):

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

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

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

    def toJson(self):
        json.dumps(self, default=lambda o: o.__dict__)

class AzureSubscription:

    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id


# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

# Adapt credentials from azure-identity to be compatible with SDK that needs msrestazure or azure.common.credentials
# Need msrest >= 0.6.0
# See also https://pypi.org/project/azure-identity/
# https://github.com/Azure/azure-sdk-for-python/issues/15330

from msrest.authentication import BasicTokenAuthentication
from azure.core.pipeline.policies import BearerTokenCredentialPolicy
from azure.core.pipeline import PipelineRequest, PipelineContext
from azure.core.pipeline.transport import HttpRequest

from azure.identity import DefaultAzureCredential

class AzureIdentityCredentialAdapter(BasicTokenAuthentication):
    def __init__(self, credential=None, resource_id="https://management.azure.com/.default", **kwargs):
        """Adapt any azure-identity credential to work with SDK that needs azure.common.credentials or msrestazure.

        Default resource is ARM (syntax of endpoint v2)

        :param credential: Any azure-identity credential (DefaultAzureCredential by default)
        :param str resource_id: The scope to use to get the token (default ARM)
        """
        super(AzureIdentityCredentialAdapter, self).__init__(None)
        if credential is None:
            credential = DefaultAzureCredential()
        self._policy = BearerTokenCredentialPolicy(credential, resource_id, **kwargs)

    def _make_request(self):
        return PipelineRequest(
            HttpRequest(
                "AzureIdentityCredentialAdapter",
                "https://fakeurl"
            ),
            PipelineContext(None)
        )

    def set_token(self):
        """Ask the azure-core BearerTokenCredentialPolicy policy to get a token.

        Using the policy gives us for free the caching system of azure-core.
        We could make this code simpler by using private method, but by definition
        I can't assure they will be there forever, so mocking a fake call to the policy
        to extract the token, using 100% public API."""
        request = self._make_request()
        self._policy.on_request(request)
        # Read Authorization, and get the second part after Bearer
        token = request.http_request.headers["Authorization"].split(" ", 1)[1]
        self.token = {"access_token": token}

    def get_token(self):
        return self.token

    def signed_session(self, session=None):
        self.set_token()
        return super(AzureIdentityCredentialAdapter, self).signed_session(session)


