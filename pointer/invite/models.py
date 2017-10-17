from __future__ import unicode_literals

from django.db import models

from members.models import Member
from point.models import Pointer

# Create your models here.

class Invite(models.Model):
    to_member = models.ForeignKey(
        Member,
        related_name='invite_member'
    )

    pointer = models.ForeignKey(
        Pointer,
        related_name='event'
    )
    
