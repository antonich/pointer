from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

# from friends.models import Friendship

class UserManager(BaseUserManager):
    def create_user(self, username, email, description, name='', password=None):
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            name = name,
            description = description
        )

        user.set_password(password)
        user.save(using = self._db)
        return user


    def create_superuser(self, username, email, password='', description='', name=''):
        user = self.create_user(username, email, description, name, password=password)
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using = self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=130, blank=True, default='')
    description = models.CharField(max_length=100, blank=True, default='')
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.name if self.name else self.email

    def is_user_active(self):
        return self.is_active

    def get_short_name(self):
        return self.email

    def Is_superuser(self):
        return self.is_superuser

    def __unicode__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
