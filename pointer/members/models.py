from __future__ import unicode_literals

from django.db import models

from users.models import User
from point.models import Pointer
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

EMPTY_FIELD = "This field cant be empty."
ALREADY_EXISTS_ERROR = "Already exists with the same value."

class MemberManager(models.Manager):
    def create_member(self, user, pointer):
        if not user or not pointer:
            raise ValueError(EMPTY_FIELD)

        if Member.objects.filter(pointer=pointer):
            raise ValueError(ALREADY_EXISTS_ERROR)

        member = self.model(
            user=user,
            pointer=pointer
        )

        member.save()

        return member

class Member(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL
    )
    pointer = models.ForeignKey(
        Pointer
    )

    objects = MemberManager()

    def __unicode__(self):
        return "User '%s' for '%s'" % (self.user, self.pointer)
