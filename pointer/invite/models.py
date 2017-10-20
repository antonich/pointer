from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from users.models import User
from point.models import Pointer
from invite.exceptions import *

class InviteManager(models.Manager):
    def create_invite(self, user, pointer):
        if not user or not pointer:
            raise EmptyFieldError

        if Invite.objects.filter(to_user=user, pointer=pointer):
            raise AlreadyExistsError


        invitation = self.model(
            to_user=user,
            pointer=pointer,
            date = timezone.now()
        )

        invitation.save()
        return invitation


class Invite(models.Model):
    to_user = models.ForeignKey(
        User,
        related_name='invite_user'
    )

    pointer = models.ForeignKey(
        Pointer,
        related_name='event_for_invite'
    )
    date = models.DateTimeField()

    objects = InviteManager()

    class Meta:
        ordering = ['pointer']

    def __unicode__(self):
        return "Invitation to %s pointer %s" % (self.to_user, self.pointer)
