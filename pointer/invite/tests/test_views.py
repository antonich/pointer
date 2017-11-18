from django.test import TestCase
from django.utils import timezone

from datetime import datetime, timedelta

from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User
from invite.models import Invite
from invite.serializers import InviteSerializer
from friends.models import Friendship
from point.models import PrivatePointer
from members.models import Member
from members.choices import *

class InviteViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", \
            password="password123", email="email1@gmail.com")
        self.user2 = User.objects.create_user(username="User2", \
            password="password123", email="email1231@gmail.com")
        self.point = PrivatePointer.objects.create_pointer(author=self.user1, title='party', \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

        token = Token.objects.create(user=self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=self.user1)

    def test_correct_invite_created(self):
        Friendship.objects.create_friendship(self.user1, self.user2)
        request = self.client.put('/invite/create_invite/'+str(self.user2.pk)+'/'+str(self.point.pk)+'/')

        self.assertEqual(request.status_code, 201)
        self.assertEqual(Invite.objects.filter(to_user=self.user2).count(), 1)
        self.assertEqual(Member.objects.get(user=self.user2).status, WAITING)

    def test_invite_to_unknown_user(self):
        Friendship.objects.create_friendship(self.user1, self.user2)
        request = self.client.put('/invite/create_invite/'+str(self.user2.pk+100)+'/'+str(self.point.pk)+'/')

        self.assertEqual(request.status_code, 404)

    def test_invite_to_unknown_pointer(self):
        Friendship.objects.create_friendship(self.user1, self.user2)
        request = self.client.put('/invite/create_invite/'+str(self.user2.pk)+'/'+str(self.point.pk+100)+'/')

        self.assertEqual(request.status_code, 404)

    def test_invite_to_not_friend(self):
        request = self.client.put('/invite/create_invite/'+str(self.user2.pk)+'/'+str(self.point.pk+100)+'/')

        self.assertEqual(request.status_code, 404)

    def test_accept_invite(self):
        Friendship.objects.create_friendship(self.user1, self.user2)
        user2_point = PrivatePointer.objects.create_pointer(author=self.user2, title='party123', \
            desc='party hard123', pdate=datetime.now(timezone.utc)+timedelta(days=1))
        invite = Invite.objects.create_invite(self.user1, user2_point)
        request = self.client.put('/invite/accept_invite/'+str(invite.pk)+'/')

        self.assertEqual(request.status_code, 202)
        self.assertEqual(len(Member.objects.going_members(user2_point)), 2)
        self.assertEqual(Invite.objects.all().count(), 0)

    def test_decline_invite(self):
        Friendship.objects.create_friendship(self.user1, self.user2)
        user2_point = PrivatePointer.objects.create_pointer(author=self.user2, title='party123', \
            desc='party hard123', pdate=datetime.now(timezone.utc)+timedelta(days=1))
        invite = Invite.objects.create_invite(self.user1, user2_point)
        request = self.client.put('/invite/decline_invite/'+str(invite.pk)+'/')

        self.assertEqual(len(Member.objects.decline_members(user2_point)), 1)
        self.assertEqual(request.status_code, 202)
        self.assertEqual(Invite.objects.all().count(), 0)

    def test_invite_view_list(self):
        Friendship.objects.create_friendship(self.user1, self.user2)
        point = PrivatePointer.objects.create_pointer(author=self.user2, title='party123', \
            desc='party ha12213rd', pdate=datetime.now(timezone.utc)+timedelta(days=1))
        invite = Invite.objects.create_invite(self.user1, point)
        request = self.client.get('/invite/invite_list/')

        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.data), 1)
