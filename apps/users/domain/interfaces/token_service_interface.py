from abc import ABC, abstractmethod


class TokenServiceInterface(ABC):
    @abstractmethod
    def blacklist(self, refresh_token: str) -> None: ...
