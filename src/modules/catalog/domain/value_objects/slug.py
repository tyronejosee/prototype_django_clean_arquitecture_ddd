import re
import unicodedata
from dataclasses import dataclass

from src.modules.catalog.domain.exceptions import CatalogDomainError


@dataclass(frozen=True)
class Slug:
    value: str

    # Messages
    SLUG_REQUIRED_MSG: str = "Slug is required."

    def __str__(self) -> str:
        return self.value

    def __post_init__(self) -> None:
        # Normalize the value
        object.__setattr__(self, "value", self.value.strip() if self.value else "")
        self._validate()

    def _validate(self) -> None:
        if not self.value:
            raise CatalogDomainError(self.SLUG_REQUIRED_MSG)

    @staticmethod
    def from_name(name: str) -> "Slug":
        slug = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
        slug = slug.lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
        return Slug(slug)
