from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
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


class User(BaseModel, AbstractBaseUser):
    """The User model contains all the user's information"""
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=128, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    picture = models.CharField(max_length=128, default='default.jpg')
    bio = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'users'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class BlogPost(BaseModel):
    """Blog Post class for all blog posts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    subheading = models.TextField(blank=True, null=True)
    picture = models.CharField(max_length=256, default='default_post.jpg')
    category = models.CharField(max_length=50, default='Miscellaneous')

    class Meta:
        db_table = 'blog_post'

    def __str__(self):
        """Returns a string representation of the blog post"""
        return f'{self.title} by {self.user.username}'
