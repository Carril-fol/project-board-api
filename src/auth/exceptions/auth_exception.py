class InvalidCredentialsException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class InvalidTokenExceptions(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)