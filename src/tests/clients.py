from flask import testing
from werkzeug.datastructures import Headers


class AppServerTestClient(testing.FlaskClient):
    APP_SERVER_AUTH_KEY = 'x_api_key'
    TEST_API_KEY = 'fake_api_key'

    def open(self, *args, **kwargs):
        auth_headers = Headers({
            self.APP_SERVER_AUTH_KEY: self.TEST_API_KEY
        })
        headers = kwargs.pop('headers', Headers())
        headers.extend(auth_headers)
        kwargs['headers'] = headers
        return super().open(*args, **kwargs)


class WebAdminTestClient(testing.FlaskClient):
    WEB_ADMIN_AUTH_KEY = 'authorization'
    TEST_TOKEN = 'fake_token'

    def open(self, *args, **kwargs):
        auth_headers = Headers({
            self.WEB_ADMIN_AUTH_KEY: self.TEST_TOKEN
        })
        headers = kwargs.pop('headers', Headers())
        headers.extend(auth_headers)
        kwargs['headers'] = headers
        return super().open(*args, **kwargs)
