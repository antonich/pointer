from django.test import TestCase

from point.models import Pointer
from users.models import User
from members.models import Member

class TestMember(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="testing", email="test@gmail.com", \
            password='testing123')
        self.user2 = User.objects.create_user(username="testing1", email="test123@gmail.com", \
            password='testing123')
        self.point = Pointer.objects.create_pointer(author=self.user2, title="party hard", \
            desc="we are partying hard today")

    def test_create_member_for_pointer(self):
        member = Member.objects.create_member(user=self.user1, pointer=self.point)

        self.assertEqual(Member.objects.all().count(), 1)

    def test_create_member_for_pointer_twice(self):
        with self.assertRaises(ValueError):
            member1 = Member.objects.create_member(user=self.user1, pointer=self.point)
            member2 = Member.objects.create_member(user=self.user1, pointer=self.point)

    def test_create_member_can_have_more_pointers(self):
        point1 = Pointer.objects.create_pointer(author=self.user1, title="my bd", \
            desc="we are partying hard today")
        member1 = Member.objects.create_member(user=self.user1, pointer=self.point)
        member2 = Member.objects.create_member(user=self.user1, pointer=point1)

    def test_author_cant_be_member(self):
        pass
