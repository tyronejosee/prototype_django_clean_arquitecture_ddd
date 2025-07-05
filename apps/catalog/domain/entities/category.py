from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from apps.catalog.domain.value_objects.category_name import CategoryName


@dataclass(kw_only=True, slots=True)
class Category:
    id: UUID
    name: CategoryName
    description: str = ""
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
