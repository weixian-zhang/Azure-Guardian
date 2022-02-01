import requests
from urllib.parse import urljoin

class OpaManager:

    def __init__(self) -> None:

        self.opa_policies_url = "http://localhost:8181/v1/policies/"

        self.opa_query_url = "http://localhost:8181/v1/data/"

    def add_update_policy(self, policyName, package_name):

        url = urljoin(self.opa_policies_url, policyName)

        putResp = requests.put(url, data=policyName)

    def is_policy_exist(self, policyName):

        url = urljoin(self.opa_policies_url, policyName)

        resp = requests.get(url)

        jsonResult = resp.json()

        if jsonResult['code'] == 'resource_not_found':
            return False

        return True
    
    def eval_policy(self, input, policyPackageName):

        packageNameAsUrlPath = self.packagename_to_urlpath(policyPackageName)

        url = urljoin(self.opa_query_url, packageNameAsUrlPath)

        resp = requests.post(url, input)

        print(resp.text)

    def packagename_to_urlpath(self, package_name):

        urlpath = package_name.replace(".", "/")
        return urlpath
