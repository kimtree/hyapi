# -*- coding: utf-8 -*-

import time
import urllib

import binascii
import requests
from Crypto.Cipher import AES
from error import HYAuthError
from pkcs7 import PKCS7Encoder


class API(object):
    def __init__(self, auth=None, host='https://api.hanyang.ac.kr',
                 api_root='/rs'):
        self.auth = auth
        self.host = host
        self.api_root = api_root

    def login_info(self, result_format='json'):
        return bind_api(
            api=self,
            path='/user/loginInfo.' + result_format,
            method='GET',
            require_auth=True
        )


def bind_api(**config):

    class APIMethod(object):
        api = config['api']
        path = config['path']
        allowed_param = config.get('allowed_param', [])
        method = config.get('method', 'GET')
        require_auth = config.get('require_auth', False)

        def __init__(self, args, kwargs):
            if self.require_auth and not self.api.auth:
                raise HYAuthError('Authentication required!')

            self._get_encrypt_key()

        def _get_encrypt_key(self):
            url = self.api.auth._get_oauth_url('get_param_enc_key')

            payload = {
                'client_id': self.api.auth.client_id,
                'swap_key': int(time.time())
            }
            r = requests.post(url, data=payload)

            result = r.json()

            self.key = result['body']['key']
            self.iv = result['body']['iv']
            self.swap_key = result['body']['swapKey']

        def execute(self):
            url = self.api.host + self.api.api_root + self.path

            params = {
                'client_id': self.api.auth.client_id,
                'access_token': self.api.auth.access_token,
                'swap_key': self.swap_key
            }

            aes = AES.new(key=self.key, mode=AES.MODE_CBC, IV=self.iv)
            encoder = PKCS7Encoder()

            # pad the plain text according to PKCS7
            pad_text = encoder.encode(urllib.urlencode(params))

            # encrypt the padding text
            cipher = aes.encrypt(pad_text)

            # transform cipher text for transport
            enc = binascii.hexlify(bytearray(cipher)).decode('utf-8')

            r = requests.get(url + '?enc=' + enc, headers=params)

            return r.content

    def _call(*args, **kwargs):
        method = APIMethod(args, kwargs)
        return method.execute()

    return _call()
