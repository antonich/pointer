from django.core.exceptions import ValidationError
from django.test import TestCase
from users.models import User
from events.models import *
from friends.models import Request, Friendship


class TestEvents(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", email="email1")
        self.user2 = User.objects.create_user(username="User2", email="email2")


    def test_creating_of_public_pointer(self):
        pointer = Pointer.objects.create_pointer(creator=self.user1,
                                                name='Test pointer',
                                                date=datetime.datetime.now()+datetime.timedelta(days=1),
                                                description="This is a test pointer",
                                                is_private=False)
        self.assertEqual(Pointer.objects.count(), 1)

    def test_joining_public_pointer(self):
        pointer = Pointer.objects.create_pointer(creator=self.user1,
                                                name='Test pointer',
                                                date=datetime.datetime.now()+datetime.timedelta(days=1),
                                                description="This is a test pointer",
                                                is_private=False)

        pointer.join(user=self.user2)
        self.assertEqual(Member.objects.all().count(), 2)

    def test_creating_private_pointer(self):
        self.user3 = User.objects.create_user(username="User3", email="email3")

        pointer = Pointer.objects.create_pointer(creator=self.user1,
                                                name='Test pointer',
                                                date=datetime.datetime.now() + datetime.timedelta(days=1),
                                                description="This is a test pointer",
                                                is_private=True,
                                                invited_people=[self.user2, self.user3])

        self.assertEqual(Pointer.objects.all().count(), 1)
        self.assertEqual(Member.objects.all().count(), 3)

    def test_get_member_list(self):
        self.user3 = User.objects.create_user(username="User3", email="email3")
        pointer = Pointer.objects.create_pointer(creator=self.user1,
                                                name='Test pointer',
                                                date=datetime.datetime.now() + datetime.timedelta(days=1),
                                                description="This is a test pointer",
                                                is_private=True,
                                                invited_people=[self.user2, self.user3] )
        members = pointer.get_memberslist()
        self.assertEqual(len(members), 3)

        self.assertTrue(self.user3 in members)
        self.assertTrue(self.user2 in members)
        self.assertTrue(self.user1 in members)

    def test_check_if_creator_is_member(self):
        pointer1 = Pointer.objects.create_pointer(creator=self.user1,
                                                  name='Test pointer',
                                                  date=datetime.datetime.now() + datetime.timedelta(days=1),
                                                  description="This is a test pointer",
                                                  is_private=True)

        pointer2 = Pointer.objects.create_pointer(creator=self.user1,
                                                  name='Test pointer2',
                                                  date=datetime.datetime.now() + datetime.timedelta(days=2),
                                                  description="This is a test pointer",
                                                  is_private=True)
        self.assertTrue(Member.objects.filter(user=self.user1).all().count(), 2)


    def test_get_planned_poinetrlist(self):
        pointer1 = Pointer.objects.create_pointer(creator=self.user1,
                                                name='Test pointer',
                                                date=datetime.datetime.now() + datetime.timedelta(days=1),
                                                description="This is a test pointer",
                                                is_private=False )

        pointer2 = Pointer.objects.create_pointer(creator=self.user1,
                                                name='Test pointer2',
                                                date=datetime.datetime.now() + datetime.timedelta(days=2),
                                                description="This is a test pointer",
                                                is_private=False)
        pointers = Pointer.objects.get_planned_pointerslist(member=self.user1)
        self.assertEqual(len(pointers), 2)
        self.assertTrue(pointer1 in pointers)
        self.assertTrue(pointer2 in pointers)

    def test_get_suggested_pointerlist(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.filter(from_user=self.user1)[0].accept()
        self.user3 = User.objects.create_user(username="User3", email="email3")
        Request.objects.send_request(from_user=self.user1, to_user=self.user3)
        Request.objects.filter(from_user=self.user1)[0].accept()

        pointer1 = Pointer.objects.create_pointer(creator=self.user2,
                                                 name='Test pointer2',
                                                 date=datetime.datetime.now() + datetime.timedelta(days=1),
                                                 description="This is a test pointer",
                                                 is_private=False)
        Member.objects.create_member(user=self.user3,
                                     pointer=pointer1,
                                     is_accepted=True)
        pointer2 = Pointer.objects.create_pointer(creator=self.user3,
                                                  name='Test pointer3',
                                                  date=datetime.datetime.now() + datetime.timedelta(days=1),
                                                  description="This is a test pointer",
                                                  is_private=False)
        Member.objects.create_member(user=self.user2,
                                     pointer=pointer2,
                                     is_accepted=True)


        pointers = Pointer.objects.get_suggested_pointerlist(user=self.user1)
        print(pointers)

    def test_cant_invite_same_user(self):
        pointer1 = Pointer.objects.create_pointer(creator=self.user1,
                                                  name='Test pointer1',
                                                  date=datetime.datetime.now() + datetime.timedelta(days=1),
                                                  description="This is a test pointer",
                                                  is_private=False)
        pointer1.invite(self.user2)
        with self.assertRaises(ValueError):
            pointer1.invite(self.user2)

