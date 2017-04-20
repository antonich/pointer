from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.db.models import Q

from users.models import User

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Create your models here.

class FriendshipManager(models.Manager):

    def friends_list(self, user):
        friends = Friendship.objects.filter(Q(userid1=user)|Q(userid2=user)).all()

        return friends

#////////////////////////////////////////////////////////////////////////////////

class Friendship(models.Model):
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

    objects = FriendshipManager()

    def __unicode__(self):
        return "User #%s is friends with #%s" % (self.userid1, self.userid2)
