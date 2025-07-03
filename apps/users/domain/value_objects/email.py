import re

from ..exceptions import UserDomainException


class Email:
    def __init__(self, value: str) -> None:
        if not self._is_valid(value):
            raise UserDomainException("Invalid email format")
        self.value = value

    def _is_valid(self, value: str) -> bool:
        return re.match(r"[^@]+@[^@]+\.[^@]+", value) is not None

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"Email({self.value!r})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Email) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
