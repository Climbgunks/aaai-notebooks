#!/usr/bin/env python3

# IBM COPYRIGHT STATEMENT BELOW, DO NOT ALTER OR REMOVE
_copyright = """
Automated Decision Optimization version 1.0.0
IBM Confidential
Copyright IBM Corp. 2022
"""
# IBM COPYRIGHT STATEMENT ABOVE, DO NOT ALTER OR REMOVE

import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class AutodoClient:
    def __init__(self, server_url, email, client_id=None, client_secret=None, ignore_ssl_warnings=False):
        self.url = server_url
        while self.url.endswith("/"):
            self.url = self.url[:-1]
        self.autodo_url = f"{self.url}/autodo"
        self.email = email
        self.client_id = client_id
        self.client_secret = client_secret
        self.ssl_verify = not ignore_ssl_warnings
        if ignore_ssl_warnings:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        if (client_id is not None and client_secret is None) or (client_id is None and client_secret is not None):
            raise Exception("credentials must include BOTH client_id and client_secret")

        self.json_headers = {"Content-type": "application/json"}
        self.credentials = None
        if client_id:
            self.credentials = {"X-IBM-Client-Id": client_id, "X-IBM-Client-Secret": client_secret}
            self.json_headers.update(self.credentials)

    def health_check(self):
        req = requests.get(f"{self.autodo_url}/health-check", headers=self.credentials, verify=self.ssl_verify)
        return req.json()

    def get_agents(self):
        req = requests.get(f"{self.autodo_url}/agents", headers=self.credentials, verify=self.ssl_verify)
        return req.json()

    def get_submissions(self):
        req = requests.get(f"{self.autodo_url}/submissions?email={self.email}", headers=self.credentials, verify=self.ssl_verify)
        return req.json()

    def create_submission(self, params):
        params["email"] = self.email
        req = requests.post(f"{self.autodo_url}/submissions", headers=self.json_headers, data=json.dumps(params), verify=self.ssl_verify)
        return req.json()

    def get_submission_info(self, submission_uuid):
        req = requests.get(f"{self.autodo_url}/submissions/{submission_uuid}", headers=self.credentials, verify=self.ssl_verify)
        return req.json()

    def get_submission_results_file(self, submission_uuid, filepath):
        req = requests.get(f"{self.autodo_url}/submissions/{submission_uuid}/results", headers=self.credentials, verify=self.ssl_verify)
        # TBD:: complete
        return None

    def get_submission_results_url(self, submission_uuid):
        req = requests.get(f"{self.autodo_url}/submissions/{submission_uuid}/results", headers=self.credentials, verify=self.ssl_verify)
        return req.json()

    def delete_submission(self, submission_uuid):
        req = requests.delete(f"{self.autodo_url}/submissions/{submission_uuid}", headers=self.credentials, verify=self.ssl_verify)
        return req.json()

    def create_code_submission(self, params, codepath):
        params["email"] = self.email
        multipart_form_data = {"env": ("env", open(codepath, "rb")), "params": (None, json.dumps(params))}
        req = requests.post(f"{self.autodo_url}/code_submissions", files=multipart_form_data, headers=self.credentials, verify=self.ssl_verify)
        return req.json()
