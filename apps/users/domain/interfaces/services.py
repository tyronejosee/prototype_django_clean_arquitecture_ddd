from abc import ABC, abstractmethod


class PasswordServiceInterface(ABC):
    @abstractmethod
    def hash_password(self, raw_password: str | None) -> str:
        pass

    @abstractmethod
    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        pass
