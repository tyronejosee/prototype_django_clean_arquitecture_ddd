from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class Wishlist:
    id: UUID
    user_id: UUID
    product_id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
