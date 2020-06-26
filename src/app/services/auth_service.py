import os

import requests
from flask import Response


class AuthService:
    @staticmethod
    def check_admin_token(token):
        auth_url = os.environ.get('AUTH_BASE_URL', "") + '/connect/access_token_validation'
        r = requests.get(auth_url, headers={'authorization': token})

        if r.status_code != 200:
            return Response({}, 502)

        return Response({}, 200)
