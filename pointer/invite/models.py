from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from users.models import User
from point.models import Pointer, PrivatePointer
from invite.exceptions import *
from members.models import Member
from members.exceptions import *
from members.choices import *
from friends.models import Friendship
from point.exceptions import *

class InviteManager(models.Manager):
    def create_invite(self, user, pointer):
        if not user or not pointer:
            raise EmptyFieldError

        if Invite.objects.filter(to_user=user, pointer=pointer):
            raise InviteAlreadyExistsError

        if not Friendship.objects.are_friends(pointer.author, user):
            raise InviteOnlyFriendsError

        if Member.objects.filter(user=user, pointer=pointer):
            raise AlreadyMemberOfThisPointer

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
    date = models.DateTimeField(default=timezone.now)

    objects = InviteManager()

    class Meta:
        ordering = ['pointer']

    def __unicode__(self):
        return "Invitation to %s pointer %s" % (self.to_user, self.pointer)

    def accept(self):
        member = Member.objects.get(user=self.to_user, \
            pointer=self.pointer)
        member.status = GOING
        member.save()

        self.delete()

    def decline(self):
        member = Member.objects.get(user=self.to_user, \
            pointer=self.pointer)
        member.status = DECLINE
        member.save()

        self.delete()
