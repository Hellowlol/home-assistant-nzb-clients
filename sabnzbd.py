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

    def refresh_queue(self):
        try:
            api_args = {}
            api_args['apikey'] = self.api_key
            api_args['mode'] = 'queue'
            api_args['start'] = '0'
            api_args['limit'] = '10'
            api_args['output'] = 'json'

            url = self.BASE_URL + 'api'
            response = self.session.get(url, params=api_args)

            self.queue = response.json().get('queue')
        except RequestException:
            raise SabnzbdApiException(
                "Failed to communicate with SABnzbd API.")

    def check_available(self):
        try:
            api_args = {}
            api_args['apikey'] = self.api_key
            api_args['mode'] = 'queue'
            api_args['output'] = 'json'

            url = self.BASE_URL + 'api'
            response = self.session.get(url, params=api_args, timeout=5)
            json_obj = response.json()
                raise SabnzbdApiException(
                    json_obj.get('error',
                                 'Failed to communicate with SABnzbd API.'))
        except RequestException:
            raise SabnzbdApiException(
                "Failed to communicate with SABnzbd API.")

        return True


class SabnzbdApiException(Exception):
    pass
