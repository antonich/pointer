from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from users.models import User
from point.models import Pointer
from members.exceptions import *
from members.choices import *

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class MemberManager(models.Manager):
    def create_member(self, user, pointer, status=GOING):
        if not user or not pointer or not status:
            raise EmptyFieldError

        if Member.objects.filter(user=user, pointer=pointer):
            raise AlreadyExistsError

        member = self.model(
            user=user,
            pointer=pointer,
            status=status
        )

        member.save()

        return member

    def members_pointer_list(self, user):
        return [member.pointer for member in Member.objects.filter(user=user)]

    def going_members(self, pointer):
        return Member.objects.filter(pointer=pointer, status=GOING)

    def decline_members(self, pointer):
        return Member.objects.filter(pointer=pointer, status=DECLINE)

class Member(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="member"
    )
    pointer = models.ForeignKey(
        Pointer,
        related_name="event_for_member"
    )
    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        default=GOING,
    )

    objects = MemberManager()

    class Meta:
        ordering = ['user']

    def __unicode__(self):
        return "Member %s for pointer %s" % (self.user, self.pointer)
