from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase

from users.models import User
from friends.models import Request, Friendship
from friends.exceptions import *

class TestRequest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", email="email1")
        self.user2 = User.objects.create_user(username="User2", email="email2")
        self.user3 = User.objects.create_user(username="User3", email="email3")
        self.user4 = User.objects.create_user(username="User5", email="email4")

    def test_correct_request_sent(self):
        request = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        self.assertEqual(Request.objects.all().count(), 1)

    def test_request_with_the_same_user(self):
        with self.assertRaises(ValidationError):
            Request.objects.send_request(from_user=self.user1, to_user=self.user1)

    def test_user_sends_request_to_himself(self):
        with self.assertRaises(ValidationError):
            Request.objects.send_request(from_user=self.user1, to_user=self.user1)

    def test_users_already_friends(self):
        # make friendship
        request = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request.accept()

        # check if friendship is created
        self.assertTrue(Friendship.objects.are_friends(user1=self.user1, user2=self.user2))

        with self.assertRaises(AlreadyFriendsError):
            Request.objects.send_request(from_user=self.user1, to_user=self.user2)

    def test_request_is_already_sent(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        with self.assertRaises(AlreadyExistsError):
            Request.objects.send_request(from_user=self.user1, to_user=self.user2)

    def test_request_cant_be_sent_if_another_user_have_already_sent_to_you(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        with self.assertRaises(AlreadyExistsError):
            Request.objects.send_request(self.user2, self.user1)

    def test_user_request_sent_list(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.send_request(from_user=self.user1, to_user=self.user3)
        self.assertTrue(self.user3 and self.user2 in Request.objects.users_sent_request(self.user1))
        self.assertFalse(self.user4 in Request.objects.users_sent_request(self.user1))

    def test_user_request_recieved_list(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.send_request(from_user=self.user3, to_user=self.user2)
        self.assertTrue(self.user3 and self.user1 in Request.objects.users_received_requests(self.user2))
        self.assertFalse(self.user4 in Request.objects.users_received_requests(self.user2))

    def test_users_friendship_is_not_created_until_accepted(self):
        request = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        self.assertFalse(Friendship.objects.are_friends(self.user1, self.user2))

    def test_request_is_declined(self):
        request = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request.decline()
        # check if request is deleted
        with self.assertRaises(ObjectDoesNotExist):
            Request.objects.get(from_user=self.user1, to_user=self.user2)
        self.assertFalse(Friendship.objects.are_friends(user1=self.user1, user2=self.user2))


class TestFriendship(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", email="email1")
        self.user2 = User.objects.create_user(username="User2", email="email2")
        self.user3 = User.objects.create_user(username="User3", email="email3")
        self.user4 = User.objects.create_user(username="User5", email="email4")

    def test_right_friendslist_returned(self):
        request1 = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request2 = Request.objects.send_request(from_user=self.user1, to_user=self.user3)
        request1.accept()
        request2.accept()
        self.assertTrue(self.user2 and self.user3 in Friendship.objects.friends_list(self.user1))

    def test_request_is_acccepted_and_friendship_is_created(self):
        request = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request.accept()
        self.assertTrue(Friendship.objects.are_friends(user1=self.user1, user2=self.user2))
        self.assertTrue(Friendship.objects.are_friends(self.user1, self.user2))


    def test_are_friends_is_working(self):
        request = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request.accept()
        self.assertTrue(Friendship.objects.are_friends(self.user1, self.user2))
        self.assertFalse(Friendship.objects.are_friends(self.user1, self.user3))

    def test_friendship_deleted(self):
        request = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request.accept()
        self.assertTrue(Friendship.objects.are_friends(self.user1, self.user2))
        friends = Friendship.objects.get_friendship(self.user1, self.user2)
        friends.delete()
        # Friendship.objects.remove_friendship(self.user1, self.user2)
        self.assertFalse(Friendship.objects.are_friends(self.user1, self.user2))

    def test_uncreated_friendship(self):
        with self.assertRaises(FriendshipNotFoundError):
            Friendship.objects.get_friendship(self.user1, self.user2)
