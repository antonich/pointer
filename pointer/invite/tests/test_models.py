from django.test import TestCase
from django.utils import timezone

from datetime import datetime, timedelta

from invite.models import Invite
from users.models import User
from point.models import PrivatePointer
from invite.exceptions import *
from members.models import Member
from members.choices import *
from friends.models import Friendship

class TestInvite(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='testing@gmail.com', \
            username='testing123')
        self.user2 = User.objects.create_user(email='testing123@gmail.com', \
            username='testing')
        self.point = PrivatePointer.objects.create_pointer(author=self.user2, title="party hard", \
            desc="we are partying hard today", pdate=datetime.now(timezone.utc)+timedelta(days=1))

        Friendship.objects.create_friendship(self.user1, self.user2)

    def test_creating_invite(self):
        invite = Invite.objects.create_invite(self.user1, self.point)

        self.assertEqual(Invite.objects.all().count(), 1)

    def test_creating_the_same_invite(self):
        invite1 = Invite.objects.create_invite(self.user1, self.point)
        with self.assertRaises(InviteAlreadyExistsError):
            invite2 = Invite.objects.create_invite(self.user1, self.point)

    def test_after_invite_member_is_created(self):
        invite = Invite.objects.create_invite(self.user1, self.point)

        self.assertEqual(Member.objects.get(user=self.user1, pointer=self.point).status, WAITING)

    def test_accept_invite(self):
        invite = Invite.objects.create_invite(self.user1, self.point)
        invite.accept()
        self.assertEqual(len(Member.objects.going_members(self.point)), 1)
        # invite is deleted
        self.assertEqual(Invite.objects.all().count(), 0)

    def test_decline_invite(self):
        invite = Invite.objects.create_invite(self.user1, self.point)
        invite.decline()
        self.assertEqual(len(Member.objects.decline_members(self.point)), 1)
        # invite is deleted
        self.assertEqual(Invite.objects.all().count(), 0)

    def test_cant_invite_author(self):
        with self.assertRaises(InviteOnlyFriendsError):
            invite = Invite.objects.create_invite(self.user2, self.point)

    def test_cant_invite_member(self):
        invite = Invite.objects.create_invite(self.user1, self.point)
        invite.accept()
        with self.assertRaises(AlreadyMemberOfThisPointer):
            invite = Invite.objects.create_invite(self.user1, self.point)

    def test_cant_invite_myself(self):
        with self.assertRaises(InviteOnlyFriendsError):
            invite = Invite.objects.create_invite(self.user2, self.point)
