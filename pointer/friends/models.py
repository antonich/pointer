from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from users.models import User

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Create your models here.


class FriendshipManager(models.Manager):

    def friends_list(self, user):
        friendships = Friendship.objects.filter(Q(userid1=user) | Q(userid2=user)).all()
        people = list()
        for fs in friendships:
            if fs.userid1 == user:
                people.append(fs.userid2)
            else:
                people.append(fs.userid1)
        return people


    def request_received_list(self, user):
        """Returns list of people who sent requests recieved by user"""
        requests = Request.objects.filter(to_user=user) #get array of requests sent to user
        people = list()
        for r in requests:
            people.append(r.from_user)
        return people

    def request_sent_list(self, user):
        """Returns a list of people received requests sent by user"""
        requests = Request.objects.filter(from_user=user)  # get array of requests sent by user
        people = list()
        for r in requests:
            people.append(r.to_user)
        return people

    def send_request(self, from_user, to_user):
        """Creates a friendship request"""
        if from_user is to_user:
            raise ValidationError("Users cannot be friends with themselves")

        if self.are_friends(from_user, to_user):
            raise ValidationError("Users are already friends")

        Request.objects.create(from_user=from_user, to_user=to_user)

    def are_friends(self, user1, user2):
        if user1 in self.friends_list(user2):
            return True
        else:
            return False


class Friendship(models.Model):
    """Model to represent friendship between two people"""
    userid1 = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user1',
    )
    userid2 = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user2',
    )
    created = models.DateTimeField(default=timezone.now)

    objects = FriendshipManager()

    def __unicode__(self):
        return "User #%s is friends with #%s" % (self.userid1, self.userid2)


class Request(models.Model):
    """Model represents friend request"""
    from_user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='requests_sent'
    )
    to_user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='requests_received'
    )

    objects = FriendshipManager()

    def accept(self):
        Friendship.objects.create(userid1=self.from_user,
                                  userid2=self.to_user)
        self.delete()

    def decline(self):
        self.delete()

    created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "User #%s requested friendship to user #%s" % (self.from_user, self.to_user)
