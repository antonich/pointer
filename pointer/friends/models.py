from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from friends.exceptions import *
from users.models import User
from django.core.exceptions import ObjectDoesNotExist

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# request errors
SAME_USER_ERROR = "The same user."
ALREADY_FRIENDS_ERROR = "Users are already friends."
ALREADY_EXISTS_ERROR = "Request already exists."

# friendship errors

# Create your models here.


class FriendshipManager(models.Manager):
    def create_friendship(self, from_user, to_user):
        '''
            Creates friendship.
        '''
        # checks if request is not send to the same user
        if from_user == to_user:
            raise ValidationError(SAME_USER_ERROR)

        fs = []
        try:
            fs.append(Friendship.objects.get(Q(from_user=from_user, to_user=to_user) \
                | Q(from_user=to_user, to_user=from_user)))
        except:
            pass

        if fs:
            raise AlreadyFriendsError(ALREADY_FRIENDS_ERROR)

        friendship = self.model(
            from_user=from_user,
            to_user=to_user
        )
        friendship.save()

        return friendship



    def get_friendship(self, user1, user2):
        '''
            Returns friendships with the user.
        '''
        try:
            friendship = Friendship.objects.get(Q(from_user=user1, to_user=user2) | \
                Q(from_user=user2, to_user=user1))
        except ObjectDoesNotExist:
            raise FriendshipNotFoundError

        return friendship


    def friends_list(self, user):
        '''
            Returns user's friends list.
        '''
        friendships = Friendship.objects.filter(Q(from_user=user) | Q(to_user=user)).all()
        people = []
        for fs in friendships:
            if fs.from_user == user:
                people.append(fs.to_user)
            else:
                people.append(fs.from_user)
        return people


    def remove_friendship(self, from_user, to_user):
        """
            Deletes a friendship.
        """
        try:
            friendship = Friendship.objects.get(from_user=from_user, to_user=to_user)
        except ObjectDoesNotExist:
            try:# try to find request vice-versa
                friendship = Friendship.objects.get(from_user=to_user, to_user=from_user)
            except ObjectDoesNotExist:
                raise FriendshipNotFoundError

        if friendship:
            friendship.delete()

        return friendship

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

    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['from_user']

    def __unicode__(self):
        return "User #%s is friends with #%s" % (self.from_user, self.to_user)


class RequestManager(models.Manager):
    def send_request(self, from_user, to_user):
        """
            Creates a friendship request.
        """
        # checks if request is not send to the same user
        if from_user == to_user:
            raise ValidationError(SAME_USER_ERROR)

        # checks if users arent already friend
        if Friendship.objects.are_friends(from_user, to_user):
            raise AlreadyFriendsError(ALREADY_FRIENDS_ERROR)

        # checks if request hasnt been already sent and reverse one too
        if Request.objects.filter(from_user=from_user, to_user=to_user) or Request.objects.filter(from_user=to_user, to_user=from_user):
            raise AlreadyExistsError(ALREADY_EXISTS_ERROR)

        # request = Request.objects.create(from_user=from_user, to_user=to_user)
        request = self.model(
            from_user=from_user,
            to_user=to_user
        )
        request.save()

        return request

    def remove_request(self, from_user, to_user):
        """
            Deletes a friendship request.
        """
        try:
            request = Request.objects.get(from_user=from_user, to_user=to_user)
        except ObjectDoesNotExist:
            try:# try to find request vice-versa
                request = Request.objects.get(from_user=to_user, to_user=from_user)
            except ObjectDoesNotExist:
                raise RequestNotFoundError
        if request:
            request.delete()

    def users_received_requests(self, user):
        """
            Returns a list of users who received request from user.
        """
        return [ i.from_user for i in Request.objects.filter(to_user=user)]

    def users_sent_requests(self, user):
        """
            Returns a list of people to whom user sent request.
        """
        return [ i.to_user for i in Request.objects.filter(from_user=user)]



class Request(models.Model):
    """
        Model represents friend request.
    """
    from_user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='requests_sent'
    )
    to_user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='requests_received'
    )
    created = models.DateTimeField(default=timezone.now)


    objects = RequestManager()

    def accept(self):
        try:
            fs = Friendship.objects.create_friendship(from_user=self.from_user, \
                to_user=self.to_user)
        except:
            raise AlreadyExistsError("Friendship already exists.")
        self.delete()

    def decline(self):
        self.delete()


    def __unicode__(self):
        return "@%s request to @%s" % (self.from_user, self.to_user)
