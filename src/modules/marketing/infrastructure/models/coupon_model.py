import uuid

from django.db import models


class CouponModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    user_id = models.UUIDField(null=True, blank=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table: str = "marketing_coupon"
        indexes: list[models.Index] = [models.Index(fields=["code"]), models.Index(fields=["is_active"])]
        ordering: list[str] = ["discount_percent"]
        verbose_name_plural: str = "coupons"
        verbose_name: str = "coupon"

    def __str__(self) -> str:
        return f"Coupon(code={self.code}, discount_percent={self.discount_percent})"
