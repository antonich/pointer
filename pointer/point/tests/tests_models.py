from django.test import TestCase
from django.utils import timezone

from datetime import datetime, timedelta

from point.models import Pointer, PublicPointer, PrivatePointer
from users.models import User
from members.models import Member
from members.choices import *
from point.exceptions import *
from invite.models import Invite
from friends.models import Friendship
from invite import exceptions

class TestPointer(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='testing@gmail.com', \
            username='testing123')

    def create_pointer(self):
        return Pointer.objects.create_pointer(author=self.user1, title="party", \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def test_point_is_created_correctly(self):
        point = self.create_pointer()
        self.assertTrue(Pointer.objects.all(), 1)

    def test_pointer_missing_some_value(self):
        # without author
        with self.assertRaises(EmptyFieldError):
            point = Pointer.objects.create_pointer(title="party", \
                desc='party hard')

        # without title
        with self.assertRaises(EmptyFieldError):
            point = Pointer.objects.create_pointer(author=self.user1, \
                desc='party hard')

    def test_two_and_more_pointer_with_the_same_name_for_one_user_not_allowed(self):
        with self.assertRaises(AlreadyExistsError):
            point1 = self.create_pointer()
            point2 = self.create_pointer()

    def test_pointer_signal_sent(self):
        point = self.create_pointer()
        self.assertEqual(Member.objects.all().count(), 1)


class TestPublicPointer(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='testing@gmail.com', \
            username='testing123')
        self.user2 = User.objects.create_user(email='test@gmail.com', \
            username='testing')

    def create_ppointer(self):
        return PublicPointer.objects.create_pointer(author=self.user1, title="party", \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def test_ppoint_is_created_correctly(self):
        point = self.create_ppointer()
        self.assertTrue(PublicPointer.objects.all(), 1)

    def test_join_public_pointer(self):
        point = self.create_ppointer()

        point.join(self.user2)
        self.assertEqual(Member.objects.going_members(point)[0], Member.objects.get(user=self.user1, \
            pointer=point))

    def test_decline_pointer(self):
        point = self.create_ppointer()
        point.join(self.user2)
        # with user
        self.assertEqual(len(Member.objects.going_members(point)), 2)

        point.decline(self.user2)
        # only user
        self.assertEqual(len(Member.objects.going_members(point)), 1)

    def test_not_member_cant_decline(self):
        with self.assertRaises(MemberDoesnotExists):
            point = self.create_ppointer()
            point.decline(self.user2)


class TestPrivatePointer(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='testing1@gmail.com', \
            username='testing1')
        self.user2 = User.objects.create_user(email='testing2@gmail.com', \
            username='testing2')
        self.user3 = User.objects.create_user(email='testing3@gmail.com', \
            username='testing3')

        Friendship.objects.create_friendship(self.user1, self.user2)

    def create_prpointer(self):
        return PrivatePointer.objects.create_pointer(author=self.user1, title="party", \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def test_prpoint_is_created_correctly(self):
        point = self.create_prpointer()
        self.assertTrue(PrivatePointer.objects.all(), 1)

    def test_invite_not_friend(self):
        point = self.create_prpointer()
        with self.assertRaises(exceptions.InviteOnlyFriendsError):
            invite = point.send_invitation(self.user3)

    def test_send_invitation_to_user(self):
        point = self.create_prpointer()

        invite = point.send_invitation(self.user2)
        self.assertEqual(invite, Invite.objects.get(to_user=self.user2, pointer=point))
        self.assertEqual(len(point.waiting_members()), 1)

    def test_invite_creates_user_with_status_waiting(self):
        point = self.create_prpointer()

        invite = point.send_invitation(self.user2)
        self.assertEqual(Member.objects.get(user=self.user2, pointer=point).status, \
            WAITING)
