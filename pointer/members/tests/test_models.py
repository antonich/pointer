from django.test import TestCase
from django.utils import timezone

from datetime import datetime, timedelta

from point.models import Pointer, PublicPointer, PrivatePointer
from users.models import User
from members.models import Member
from members.exceptions import *

class TestMember(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="testing", email="test@gmail.com", \
            password='testing123')
        self.user2 = User.objects.create_user(username="testing1", email="test123@gmail.com", \
            password='testing123')
        self.point = Pointer.objects.create_pointer(author=self.user2, title="party hard", \
            desc="we are partying hard today", pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def test_create_member_for_pointer(self):
        member = Member.objects.create_member(user=self.user1, pointer=self.point)

        self.assertEqual(Member.objects.filter(user=self.user1, pointer=self.point).count(), 1)
        # with the author
        self.assertEqual(Member.objects.filter(pointer=self.point).count(), 2)

    def test_create_member_with_more_pointers_fails(self):
        member = Member.objects.create_member(user=self.user1, pointer=self.point)
        with self.assertRaises(MemberAlreadyExistsError):
            member1 = Member.objects.create_member(user=self.user1, pointer=self.point)

    def test_create_member_for_pointer_twice(self):
        member1 = Member.objects.create_member(user=self.user1, pointer=self.point)
        with self.assertRaises(MemberAlreadyExistsError):
            member2 = Member.objects.create_member(user=self.user1, pointer=self.point)

    def test_create_member_can_have_more_pointers(self):
        point1 = Pointer.objects.create_pointer(author=self.user1, title="my bd", \
            desc="we are partying hard today", pdate=datetime.now(timezone.utc)+timedelta(days=1))
        member1 = Member.objects.create_member(user=self.user1, pointer=self.point)
        member2 = Member.objects.create_member(user=self.user2, pointer=point1)

    def test_author_is_also_member(self):
        with self.assertRaises(MemberAlreadyExistsError):
            member1 = Member.objects.create_member(user=self.user2, pointer=self.point)

    def test_members_pointer_list(self):
        point1 = Pointer.objects.create_pointer(author=self.user2, title="my bd", \
            desc="we are partying hard today", pdate=datetime.now(timezone.utc)+timedelta(days=1))

        member1 = Member.objects.create_member(user=self.user1, pointer=self.point)
        member2 = Member.objects.create_member(user=self.user1, pointer=point1)

        self.assertEqual(len(Member.objects.users_pointer_list(self.user1)), 2)

    def test_members_going_list_without_author(self):
        point1 = Pointer.objects.create_pointer(author=self.user2, title="my bd", \
            desc="we are partying hard today", pdate=datetime.now(timezone.utc)+timedelta(days=1))
        Member.objects.create_member(self.user1, point1)
        self.assertEqual(len(Member.objects.going_members(point1)), 1)
