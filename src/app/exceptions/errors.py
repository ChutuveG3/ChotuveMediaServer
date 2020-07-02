class MediaError(Exception):
    DEFAULT_MESSAGE = 'default message'

    def __init__(self, message=DEFAULT_MESSAGE):
        self.message = message


class AuthServerError(MediaError):
    def __init__(self, message="default message"):
        super().__init__(message)


class InvalidParamsError(MediaError):
    def __init__(self, message="default message"):
        super().__init__(message)


class VideoNotFoundError(MediaError):
    def __init__(self, message="default message"):
        super().__init__(message)


class AuthorizationError(AuthServerError):
    def __init__(self, message="default message"):
        super().__init__(message)


class AuthenticationError(AuthServerError):
    def __init__(self, message="default message"):
        super().__init__(message)

