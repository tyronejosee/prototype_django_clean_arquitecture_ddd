from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class ProductDTO:
    id: UUID
    price: Decimal
    stock: int
