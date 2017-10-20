from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

import random, string

NO_TOKEN = "This user doesn't have token."

'''
    Manager for user below
    Test are in tests/test_models.py
'''

def generate_entry():
    """Generate a random alphanumeric string between 8 and 16 characters long."""
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(random.randint(8,16)))

class UserManager(BaseUserManager):

    def create_user(self, username, email, description='', name='', password=None):
        # Checks if email is empty
        if not email:
            raise ValueError('Users must have an email.')

        #Checks if username is empty
        if not username:
            raise ValueError("User must have an username.")

        # Checks for description length
        if len(description) > 100:
            raise ValidationError("Description length must be less than 100 chars")

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            name = name,
            description = description,
            activation_key = generate_entry()
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password='', description='', name=''):
        user = self.create_user(username, email, description, name, password=password)
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_user_token(self, user):
        try:
            return Token.objects.get(user=user)
        except:
            raise ValidationError(NO_TOKEN)

    def is_already_in_use(self, email, username):
        try:
            user = self.create_user(email=email, username=username)
            return 0
        except IntegrityError: # Error for already in use email or username
            raise ValidationError('This user is already in user')

'''
    Model to represent User
'''
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=40, unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    #Editable stuff
    name = models.CharField(max_length=130, blank=True, default='')
    description = models.CharField(max_length=100, blank=True, default='')
    #avatar = models.ImageField(upload_to='images')
    activation_key = models.CharField(max_length=17, unique=True)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.name if self.name else self.email

    def is_user_active(self):
        return self.is_active

    def get_short_name(self):
        return self.username

    def Is_superuser(self):
        return self.is_superuser

    def __unicode__(self):
        return self.username

    ''' Add mail send !!! '''
    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        return self.is_admin

