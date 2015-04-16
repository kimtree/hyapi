# -*- coding: utf-8 -*-

import unittest

from hyapi.auth import HYAuthHandler


class HYAuthHandlerTests(unittest.TestCase):

    def test_get_code_url(self):
        auth = HYAuthHandler('a', 'b', 'c', 'd')
        self.assertEqual('https://api.hanyang.ac.kr/oauth/authorize?scope=c&redirect_uri=d&response_type=code&client_id=a', auth.get_code_url())  # noqa
