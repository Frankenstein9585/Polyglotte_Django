from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, UserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid


# Create your models here.


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
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


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """The User model contains all the user's information"""
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=128, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)
    picture = models.CharField(max_length=128, default='default.jpg')
    bio = models.TextField(null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

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
    content = RichTextField()
    subheading = models.TextField(blank=True, null=True)
    picture = models.CharField(max_length=256, default='default_post.jpg')
    category = models.CharField(max_length=50, default='Miscellaneous')

    class Meta:
        db_table = 'blog_post'

    def __str__(self):
        """Returns a string representation of the blog post"""
        return f'{self.title} by {self.user.username}'
