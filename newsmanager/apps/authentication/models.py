from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from news.models import BaseModel

# Create your models here.


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class User(BaseModel, AbstractUser):
    is_admin = models.BooleanField(
        default=False,
        help_text="Admin user who can access the admin panel and perform admin actions",
    )
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_admin:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)
