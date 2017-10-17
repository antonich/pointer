from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from users.models import User
from point.models import Pointer
from members.exceptions import *
from members.choices import *

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class MemberManager(models.Manager):
    def create_member(self, user, pointer):
        if not user or not pointer:
            raise EmptyFieldError

        if Member.objects.filter(user=user, pointer=pointer):
            raise AlreadyExistsError

        member = self.model(
            user=user,
            pointer=pointer
        )

        member.save()

        return member

    def members_pointer_list(self, user):
        return [member.pointer for member in Member.objects.filter(user=user)]

class Member(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="member"
    )
    pointer = models.ForeignKey(
        Pointer,
        related_name="event"
    )
    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        default=WAITING,
    )

    objects = MemberManager()

    class Meta:
        ordering = ['user']
