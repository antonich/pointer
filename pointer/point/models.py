from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from point.exceptions import *
from members.choices import *

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class PointerManager(models.Manager):
    def create_pointer(self, author=None, title='', desc='', dcreated=timezone.now(), pdate=timezone.now()):
        if not title or not author or not desc:
            raise EmptyFieldError

        if title in Pointer.objects.filter(author=author).values_list('title', flat=True):
            raise AlreadyExistsError

        if pdate < timezone.now():
            raise PointerIsOutOfDateError

        pointer = self.model(
            title=title,
            description=desc,
            author=author
        )

        pointer.save()

        return pointer

    def author_pointer_list(self, auth):
        return Pointer.objects.filter(author=auth)


class Pointer(models.Model):
    title = models.CharField(max_length=40, blank=True, default='')
    description = models.CharField(max_length=100, blank=True, default='')
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='user'
    )
    date_created = models.DateTimeField(default=timezone.now)
    pointer_date = models.DateTimeField(default=timezone.now)

    # REQUIRED_FIELDS = ['title', 'author', 'date_created', 'pointer_date']

    objects = PointerManager()

    class Meta:
        ordering = ['pointer_date']

    def __unicode__(self):
        return "Pointer %s" % (self.title)


class PublicPointerManager(models.Manager):
    pass

class PublicPointer(Pointer):
    is_private = models.BooleanField(default=False)

    objects = PointerManager()
    public_pointer = PublicPointerManager()

    def join(self, user):
        from members.models import Member
        Member.objects.create_member(user=user, pointer=self, status=GOING)

    def decline(self, user):
        from members.models import Member
        try:
            member = Member.objects.get(user=user, pointer=self)
            member.status = DECLINE
            member.save()
        except:# DoesNotExist:
            raise MemberDoesnotExists


class PrivatePointerManager(models.Manager):
    pass

class PrivatePointer(Pointer):
    is_private = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = PointerManager()
    private_pointer = PrivatePointerManager()

    def send_invitation(self, user):
        from invite.models import Invite
        return Invite.objects.create_invite(user, self)
