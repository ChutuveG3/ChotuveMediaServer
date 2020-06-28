import os

import requests
from flask import Response
from ..exceptions import AuthenticationError, AuthorizationError


class AuthService:
    @staticmethod
    def validate_admin_token(token):
        url = os.environ.get('AUTH_BASE_URL', "") + '/connect/access_token_validation'
        r = requests.get(url, headers={'authorization': token})
        content = r.json()

        if r.status_code != 200:
            raise AuthenticationError()

        if not content.get("privilege"):
            raise AuthorizationError()

        return Response({}, 200)

    @staticmethod
    def validate_app_server(api_key):
        url = os.environ.get('AUTH_BASE_URL', "") + '/connect/api_key_validation'
        r = requests.get(url, headers={'x_api_key': api_key})

        if r.status_code != 200:
            raise AuthenticationError()

        return Response({}, 200)
