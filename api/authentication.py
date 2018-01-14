import codecs
import hashlib
import os
import yaml


class Authentication:
    def __init__(self, request):
        self.request = request
        self.identity = None
        self.error = None

    def authenticate(self):
        if not self._identify_request():
            self.error = "Unauthorized_access_Invalid_Identity"
            return False
        if not self._check_auth():
            self.error = "Unauthorized_access_Invalid_Authorization_header."
            return False
        return True


    def _identify_request(self):
        if 'Identity' not in self.request.headers:
            return False
        identity_key = self.request.headers['Identity']
        path = os.path.join(os.path.dirname(__file__), 'auth.yml')
        with open(path) as file:
            identities = yaml.load(file)
            if identity_key in identities:
                self.identity = identities[identity_key]
                return True


    def _check_auth(self):
        if "Authorization" in self.request.headers:
            received_key = self.request.headers['Authorization']
            url = self.request.url
            private_key = self.identity['secret']
            expected_key = self._get_auth_string(url, private_key)
            if received_key == expected_key:
                return True

    @staticmethod
    def _get_auth_string(url, private_key):
        return hashlib.sha1(codecs.encode(url + '|' + private_key)).hexdigest()
