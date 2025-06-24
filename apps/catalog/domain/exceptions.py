"""Exceptions for the catalog domain"""


class DomainError(Exception):
    pass


class ProductOutOfStock(DomainError):
    pass
