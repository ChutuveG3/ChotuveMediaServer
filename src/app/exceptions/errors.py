class MediaError(Exception):
    DEFAULT_MESSAGE = 'unknown exception'

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message


class AuthServerError(MediaError):
    DEFAULT_MESSAGE = "auth server error"

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message


class InvalidParamsError(MediaError):
    DEFAULT_MESSAGE = "invalid params"

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message


class VideoNotFoundError(MediaError):
    DEFAULT_MESSAGE = "video not found"

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message


class AuthorizationError(AuthServerError):
    DEFAULT_MESSAGE = "authorization error"

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message


class AuthenticationError(AuthServerError):
    DEFAULT_MESSAGE = "authentication error"

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message

