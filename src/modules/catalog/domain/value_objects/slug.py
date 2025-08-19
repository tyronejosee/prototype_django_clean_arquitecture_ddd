import re
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class Slug:
    value: str

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def from_name(name: str) -> "Slug":
        slug = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
        slug = slug.lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
        return Slug(slug)
