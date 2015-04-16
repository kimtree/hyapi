# -*- coding: utf-8 -*-

import urllib

import requests
from error import HYAuthError


class HYAuthHandler(object):
    '''OAuth authentication handler'''
    OAUTH_HOST = 'api.hanyang.ac.kr'
    OAUTH_ROOT = '/oauth/'

    def __init__(self, client_id, client_secret, scope=None, callback=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.code = None
        self.access_token = None
        self.callback = callback

    def _get_oauth_url(self, endpoint):
        return 'https://' + self.OAUTH_HOST + self.OAUTH_ROOT + endpoint

    def set_access_token(self, access_token):
        self.access_token = access_token

    def set_code(self, code):
        self.code = code

    def get_code_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.callback,
            'scope': self.scope
        }

        url = self._get_oauth_url('authorize') + '?' + urllib.urlencode(params)

        return url

    def get_access_token(self):
        url = self._get_oauth_url('token')

        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self.code,
            'scope': self.scope,
            'redirect_uri': self.callback,
            'grant_type': 'authorization_code'
        }
        r = requests.get(url, params=params)
        result = r.json()

        if result.get('access_token'):
            self.access_token = result['access_token']
            return self.access_token
        else:
            raise HYAuthError(result.get('error_description'))
