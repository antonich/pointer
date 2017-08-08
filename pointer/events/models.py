from django.db import models
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')



class Pointer(models.Model):
    """Model to represent events"""
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    description = models.CharField(max_length=500)


class Member(models.Model):
    """Model to represent a member of event"""
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='member'
    )

    pointer = models.ForeignKey(
        Pointer,
        related_name='event'
    )

