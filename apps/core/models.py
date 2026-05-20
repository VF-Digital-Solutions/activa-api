import uuid
from django.db import models


# Create your models here.
class UUIDModel(models.Model):
    """Provee un UUID como primary key"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(UUIDModel):
    """Provee timestamos de creacion y modificacion"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(TimeStampedModel):
    """Provee soft delete mediante is_active"""

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
