from functools import wraps
from flask import request
from ..services import AuthService
from ..exceptions import AuthenticationError

ADMIN_AUTH_KEY = "authorization"
APP_SERVER_AUTH_KEY = "x_api_key"


def admin_authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get(ADMIN_AUTH_KEY)

        if AuthService.validate_admin_token(token):
            return func(*args, **kwargs)

        raise AuthenticationError('admin authenticate error')

    return wrapper


def app_server_authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get(APP_SERVER_AUTH_KEY)

        if AuthService.validate_app_server(api_key):
            return func(*args, **kwargs)

        raise AuthenticationError('app server authentication')

    return wrapper


def server_or_admin_authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get(APP_SERVER_AUTH_KEY)
        token = request.headers.get(ADMIN_AUTH_KEY)
        if AuthService.validate_app_server(api_key) or \
                AuthService.validate_admin_token(token):
            return func(*args, **kwargs)

        raise AuthenticationError()

    return wrapper
