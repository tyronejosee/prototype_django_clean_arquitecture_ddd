from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.modules.catalog.domain.value_objects.brand_name import BrandName


@dataclass(kw_only=True, slots=True)
class Brand:
    id: UUID
    name: BrandName
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
