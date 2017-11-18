from django.test import TestCase
from django.utils import timezone

from datetime import datetime, timedelta

from users.models import User
from invite.models import Invite
from invite.serializers import InviteSerializer
from friends.models import Friendship
from point.models import Pointer

class TestInviteSerializer(TestCase):
    def test_invite(self):
        user1 = User.objects.create_user(username="User1", \
            password="password123", email="email1@gmail.com")
        user2 = User.objects.create_user(username="User2", \
            password="password123", email="email1231@gmail.com")
        point = Pointer.objects.create_pointer(author=user1, title='party', \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))
        Friendship.objects.create_friendship(user1, user2)
        invite = Invite.objects.create_invite(user2, point)

        serial = InviteSerializer(invite)
        self.assertEqual(serial.data['pointer'], point.pk)

class TestInviteCreation(TestCase):
    def test_create_invite(self):
        user1 = User.objects.create_user(username="User1", \
            password="password123", email="email1@gmail.com")
        user2 = User.objects.create_user(username="User2", \
            password="password123", email="email1231@gmail.com")
        point = Pointer.objects.create_pointer(author=user1, title='party', \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))
        Friendship.objects.create_friendship(user1, user2)
        invite = InviteSerializer(data={'to_user': user2.pk, 'pointer': point.pk})
        invite.is_valid()
        invite.save()
        self.assertEqual(Invite.objects.all().count(), 1)
