from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, userid, password, **extra_fields):
        if userid is None:
            raise TypeError('Users must have a userid.')

        if password is None:
            raise TypeError('Users must have a password.')

        user = self.model(
            userid=userid,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, userid, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(userid, password, **extra_fields)


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default='ACTIVE')
    USERNAME_FIELD = 'username'

    objects = UserManager()