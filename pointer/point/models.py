from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from point.exceptions import *
from members.choices import GOING, DECLINE, WAITING
from friends.models import Friendship
from members.exceptions import MemberDoesnotExists

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

    def get_planned_pointerslist(self, user):
        """
            Returns list of planned public pointers.
        """
        from members.models import Member
        pointers = list()
        for i in Member.objects.filter(user=user, status=GOING):
            # if not i.pointer.is_private: # also add prive pointers which author is invited
            pointers.append(i.pointer)
        return pointers

    def get_suggested_pointerlist(self, user):
        """
            Returns all public pointers that friends are going to visit.
        """
        friendslist = Friendship.objects.friends_list(user)
        pointers = list()
        for user in friendslist: # for each friend
            user_pointers = Pointer.objects.get_planned_pointerslist(user)
        # getting its pointers
        #     for friends_pointer in user_pointers:# for each friend's pointer
        #         found_flag = False
        #         for el in pointers: #try to add it to suggested list but check if it is already there
        #             if el["pointer"].id == friends_pointer.id:
        #                 el["count"] = el["count"]+1
        #                 found_flag = True#don't have to add it to list
        #                 break
        #         if not found_flag:#if we didn't found it we add it to list
        #             pointers.append({"pointer": friends_pointer, "count": 1})
        # #now we have list of pointers
        # sorted_pointers = sorted(pointers, key=lambda k: k['count'])
            for friends_pointer in user_pointers:
                if not (friends_pointer in pointers):
                    pointers.append(friends_pointer)
        return pointers


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

    def __str__(self):
        return "Pointer is %s" % (self.title)

    def is_author(self, user):
        return True if user == self.author else False


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
