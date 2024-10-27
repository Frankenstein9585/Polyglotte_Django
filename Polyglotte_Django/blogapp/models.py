from django.db import models
from django.utils import timezone
import uuid


# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Overrides save method to ensure updated_at is set on save."""
        self.updated_at = timezone.now()
        super(BaseModel, self).save(*args, **kwargs)

    def to_dict(self):
        """Convert instance into dict format for easy serialization."""
        new_dict = {
            "id": str(self.id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "__class__": self.__class__.__name__,
        }
        for field in self._meta.fields:
            field_name = field.name
            if field_name not in new_dict:
                new_dict[field_name] = getattr(self, field_name)
        return new_dict
