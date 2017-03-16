# -*- coding: utf-8 -*-

import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disabling https warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class StepicAPILogin:
    def __init__(self, client_id, client_secret):
        self.client = requests.Session()

        self.token = self.client.post(
            'https://stepik.org/oauth2/token/',
            data={'grant_type': 'client_credentials'},
            auth=(client_id, client_secret),
            verify=False
        ).json().get('access_token', None)
        if not self.token:
            raise RuntimeError('Unable to authorize with provided credentials')
        self.client.headers.update({
            'Authorization': 'Bearer ' + self.token
        })
        self.user_id = self.client.get('https://stepik.org/api/stepics/1').json()['profiles'][0]['id']
