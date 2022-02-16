from importlib.resources import Package
from urllib import request
import requests
from urllib.parse import urljoin
import re

class Opa:

    PackageKeyword = "package"

    def __init__(self) -> None:

        self.opa_health_url = 'http://localhost:8181/health'

        self.opa_policies_url = 'http://localhost:8181/v1/policies/'

        self.opa_query_url = 'http://localhost:8181/v1/data/'

    def is_server_ready(self):
        resp = requests.get(self.opa_health_url)
        if resp.status_code == '200':
            return True
        return False

    def add_update_policy(self, rego) -> bool:

        ok, packageName = self.get_package_name(rego)

        if not ok:
            return False, 'Not able to read package name. Package name has to be unique'

        url = urljoin(self.opa_policies_url, packageName)

        try:

            putResp = requests.put(url, data=rego)
            return True, ''
        except (Exception) as e:
            return False, e

    def delete_policy(self, packageName):

        url = urljoin(self.opa_policies_url, packageName)
        resp = requests.delete(url)

        if resp.status_code == '200':
            return True

        return False

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

    def get_package_name(self, rego: str):

        regexPattern = r"package\s.*"

        matches =  re.search(regexPattern, rego)

        packageLine = matches.group(0)

        if len(packageLine) == 0:
            return False, "Package name not found"

        splittedLine = packageLine.split(' ')
        packageName = splittedLine[1]

        return True, packageName

    def validate_package_name(self, name: str) -> bool:
        for c in name:
            if c.isdigit():
                return False

        return True

    def packagename_to_urlpath(self, package_name):

        urlpath = package_name.replace(".", "/")
        return urlpath
