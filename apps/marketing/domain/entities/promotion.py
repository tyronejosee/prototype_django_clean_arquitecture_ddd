from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(kw_only=True, slots=True)
class Promotion:
    id: UUID
    name: str
    description: str
    is_active: bool
    starts_at: datetime
    ends_at: datetime

    def is_valid(self, now: datetime) -> bool:
        return self.is_active and self.starts_at <= now <= self.ends_at
