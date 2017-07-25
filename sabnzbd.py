__author__ = 'jamespcole'

import requests
from requests.exceptions import RequestException


class SabnzbdApi(object):
    def __init__(self, base_url, api_key, session=None):
        if not base_url.endswith('/'):
            base_url = base_url + '/'
        if session is None:
            session = requests.Session()

        self.BASE_URL = base_url
        self.api_key = api_key
        self.queue = {}
        self.session = session
        self.API_URL = self.BASE_URL + 'api'
        self._default_params = {'apikey': self.api_key or '',
                                'mode': 'queue',
                                'output': 'json'
                                }

    def params(self, **kwargs):
        if kwargs:
            kw = self._default_params.copy()
            kw.update(kwargs)
            return kw

        return self._default_params

    def refresh_queue(self):
        try:
            api_args = self.params(start=0, limit=10)
            response = self.session.get(self.API_URL, params=api_args)

            self.queue = response.json().get('queue')
        except RequestException:
            raise SabnzbdApiException(
                "Failed to communicate with SABnzbd API.")

    def check_available(self):
        try:
            response = self.session.get(self.API_URL,
                                        params=self.params(),
                                        timeout=5)
            json_obj = response.json()
            if not json_obj.get('queue'):
                raise SabnzbdApiException(
                    json_obj.get('error',
                                 'Failed to communicate with SABnzbd API.'))
        except RequestException:
            raise SabnzbdApiException(
                "Failed to communicate with SABnzbd API.")

        return True


class SabnzbdApiException(Exception):
    pass
