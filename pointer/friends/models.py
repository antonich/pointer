from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.db.models import Q, timezone

from users.models import User

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Create your models here.


class FriendshipManager(models.Manager):

    def friends_list(self, user):
        friends = Friendship.objects.filter(Q(user1=user)|Q(user2=user)).all()
        return friends

    def request_recieved_list(self, user):
        """returns list of requests recieved by user"""
        requests = Request.objects.filter(to_user=user)
        return requests

    def send_request(self, from_user, to_user):
        """Creates a friendship request"""
        if from_user is to_user:
            raise ValidationError("Users cannot be friends with themselves")

        if self.are_friends(from_user,to_user):
            raise ValidationError("Users are already friends")

        Request.objects.create(from_user=from_user, to_user=to_user)


    def are_friends(self, user1, user2):
        if user1 in self.friends_list(user2):
            return True
        else:
            return False


class Friendship(models.Model):
    """Model to represent friendship between two people"""
    user1 = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user1',
    )
    user2 = models.ForeignKey(
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
        related_name='Requests sent'
    )
    to_user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='Requests received'
    )

    def accept(self):
        Friendship.objects.create(userid1=self.from_user,
                                  userid2=self.to_user)
        self.delete()

    created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "User #%s requested friendship to user #%s" % (self.userid1, self.userid2)
