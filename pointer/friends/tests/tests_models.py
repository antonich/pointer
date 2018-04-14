from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.test import TestCase
from django.db.models import Q

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
        # check if user1 one have the same request as user2, who recieved the request
        self.assertEqual(Request.objects.filter(to_user=self.user2)[0], Request.objects.filter(from_user=self.user1)[0])

    def test_request_with_the_same_user(self):
        with self.assertRaises(ValidationError):
            Request.objects.send_request(from_user=self.user1, to_user=self.user1)

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
        self.assertTrue(self.user3 and self.user2 in Request.objects.users_sent_requests(self.user1))
        self.assertFalse(self.user4 in Request.objects.users_sent_requests(self.user1))

    def test_user_request_recieved_list(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.send_request(from_user=self.user3, to_user=self.user2)
        self.assertTrue(self.user3 and self.user1 in Request.objects.users_received_requests(self.user2))
        self.assertFalse(self.user4 in Request.objects.users_received_requests(self.user2))

    # def test_users_friendship_is_not_created_until_accepted(self):
    #     request = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
    #     self.assertFalse(Friendship.objects.are_friends(self.user1, self.user2))

    def test_request_is_declined(self):
        request = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request.decline()
        # check if request is deleted
        with self.assertRaises(ObjectDoesNotExist):
            Request.objects.get(from_user=self.user1, to_user=self.user2)
        # self.assertFalse(Friendship.objects.are_friends(user1=self.user1, user2=self.user2))


class TestFriendship(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", email="email1")
        self.user2 = User.objects.create_user(username="User2", email="email2")
        self.user3 = User.objects.create_user(username="User3", email="email3")
        self.user4 = User.objects.create_user(username="User5", email="email4")

    def test_friendship_with_the_same_user(self):
        with self.assertRaises(ValidationError):
            fs = Friendship.objects.create_friendship(self.user1, self.user1)

    def test_friendship_with_friend(self):
        fs = Friendship.objects.create_friendship(self.user1, self.user2)
        with self.assertRaises(AlreadyFriendsError):
            Friendship.objects.create_friendship(self.user1, self.user2)

    def test_friendship_with_friend_reverced(self):
        fs = Friendship.objects.create_friendship(self.user1, self.user2)
        with self.assertRaises(AlreadyFriendsError):
            Friendship.objects.create_friendship(self.user2, self.user1)


    def test_right_friendslist_returned(self):
        request1 = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request2 = Request.objects.send_request(from_user=self.user1, to_user=self.user3)
        request1.accept()
        request2.accept()
        self.assertTrue(self.user2 and self.user3 in Friendship.objects.friends_list(self.user1))


    def test_if_request_is_deleted_after_friendship_is_created(self):
        request1 = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request1.accept()
        # request is delete after friendship created
        with self.assertRaises(ObjectDoesNotExist):
            Request.objects.get(from_user=self.user1, to_user=self.user2)

    def test_request_is_acccepted_and_friendship_is_created(self):
        request = Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request.accept()
        self.assertTrue(Friendship.objects.are_friends(self.user1, self.user2))


    def test_are_friends_is_working(self):
        fs = Friendship.objects.create_friendship(self.user1, self.user2)
        self.assertTrue(Friendship.objects.are_friends(self.user1, self.user2))
        self.assertFalse(Friendship.objects.are_friends(self.user1, self.user3))

    def test_friendship_deleted(self):
        fs = Friendship.objects.create_friendship(self.user1, self.user2)
        # if they are friends
        self.assertTrue(Friendship.objects.are_friends(self.user1, self.user2))
        friends = Friendship.objects.get_friendship(self.user1, self.user2)
        friends.delete()
        # Friendship.objects.remove_friendship(self.user1, self.user2)
        self.assertFalse(Friendship.objects.are_friends(self.user1, self.user2))

    def test_uncreated_friendship(self):
        with self.assertRaises(FriendshipNotFoundError):
            Friendship.objects.get_friendship(self.user1, self.user2)

    def test_friendship_list(self):
        fs1 = Friendship.objects.create_friendship(self.user1, self.user2)
        fs2 = Friendship.objects.create_friendship(self.user1, self.user3)
        self.assertTrue(Friendship.objects.filter(Q(from_user=self.user1) | Q(to_user=self.user1)).count(), 2)
        self.assertTrue(self.user2 and self.user3 in Friendship.objects.friends_list(self.user1))
