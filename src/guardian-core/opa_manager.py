import requests
from urllib.parse import urljoin

class OpaManager:

    def __init__(self) -> None:

        self.opa_policies_url = "http://localhost:8181/v1/policies/"

        self.opa_query_url = "http://localhost:8181/v1/data/"

    def add_policy(self, policy, package_name):

        url = urljoin(self.opa_policies_url, "test")

        putResp = requests.put(url, data=policy)

    
    def eval_policy(self, input, policy_package_name):

        url = urljoin(self.opa_query_url, "test")

        resp = requests.post(url, input)

        print(resp.text)

    def packagename_to_urlpath(package_name):

        urlpath = package_name.replace(".", "/")
        return urlpath
