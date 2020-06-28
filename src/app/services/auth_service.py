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
