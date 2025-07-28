import uuid

from django.db import models


class PromotionModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    class Meta:
        db_table: str = "marketing_promotion"
        indexes: list[models.Index] = [models.Index(fields=["is_active"])]
        ordering: list[str] = ["starts_at"]
        verbose_name_plural: str = "promotions"
        verbose_name: str = "promotion"

    def __str__(self) -> str:
        return f"Promotion(name={self.name})"
