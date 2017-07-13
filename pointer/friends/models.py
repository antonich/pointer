from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from friends.exceptions import *
from users.models import User

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Create your models here.


class FriendshipManager(models.Manager):

    def friends_list(self, user):
        friendships = Friendship.objects.filter(Q(from_user=user) | Q(to_user=user)).all()
        people = list()
        for fs in friendships:
            if fs.from_user == user:
                people.append(fs.to_user)
            else:
                people.append(fs.from_user)
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
        if from_user == to_user:
            raise ValidationError("Users cannot be friends with themselves")

        if self.are_friends(from_user, to_user):
            raise AlreadyFriendsError("Users are already friends")

        if Request.objects.filter(from_user=from_user, to_user=to_user):
            raise AlreadyExistsError("Friendship already requested")

        Request.objects.create(from_user=from_user, to_user=to_user)

    def remove_friendship(self, from_user, to_user):
        """deletes a friendship """
        friendship = Friendship.objects.get(from_user=from_user, to_user=to_user)
        if not friendship:  # try to find friendship vice-versa
            friendship = Friendship.objects.get(from_user=to_user, to_user=from_user)
        if friendship:
            friendship.delete()
        else:
            raise FriendshipNotFoundError

    def are_friends(self, user1, user2):
        if user1 in self.friends_list(user2):
            return True
        else:
            return False


class Friendship(models.Model):
    """Model to represent friendship between two people"""
    from_user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user1',
    )
    to_user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user2',
    )
    created = models.DateTimeField(default=timezone.now)

    objects = FriendshipManager()

    def __unicode__(self):
        return "User #%s is friends with #%s" % (self.from_user, self.to_user)


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
        Friendship.objects.create(from_user=self.from_user,
                                  to_user=self.to_user)
        self.delete()

    def decline(self):
        self.delete()

    created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "User #%s requested friendship to user #%s" % (self.from_user, self.to_user)
