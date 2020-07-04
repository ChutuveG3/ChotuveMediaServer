class Version:
    MAJOR = 3
    MINOR = 0
    PATCH = 0

    @staticmethod
    def get():
        return f'{Version.MAJOR}.{Version.MINOR}.{Version.PATCH}'
