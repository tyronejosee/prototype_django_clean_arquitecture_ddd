from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.modules.catalog.domain.value_objects.category_name import CategoryName
from src.modules.catalog.domain.value_objects.slug import Slug


@dataclass(kw_only=True, slots=True)
class Category:
    id: UUID
    name: CategoryName
    slug: Slug
    description: str = ""
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
