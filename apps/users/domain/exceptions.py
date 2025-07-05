class UserDomainError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class LogoutError(Exception):
    pass
