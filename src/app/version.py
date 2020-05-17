class Version:
    MAJOR = 1
    MINOR = 0
    PATCH = 0

    @staticmethod
    def get():
        return f'{Version.MAJOR}.{Version.MINOR}.{Version.PATCH}'
