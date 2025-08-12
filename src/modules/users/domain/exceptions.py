class UserDomainError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class LogoutError(Exception):
    pass


class WishlistDomainError(Exception):
    pass


class WishlistItemNotFoundError(Exception):
    pass


class WishlistItemAlreadyExistsError(Exception):
    pass
