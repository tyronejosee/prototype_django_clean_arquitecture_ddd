"""Exceptions for the users domain"""


class DomainError(Exception):
    pass


class UserNotFound(DomainError):
    pass


class UserAlreadyExists(DomainError):
    pass
