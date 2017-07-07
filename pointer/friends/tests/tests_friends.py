from django.core.exceptions import ValidationError
from django.test import TestCase
from users.models import User
from friends.models import Request, Friendship


class TestFriends(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", email="email1")
        self.user2 = User.objects.create_user(username="User2", email="email2")
        self.user3 = User.objects.create_user(username="User3", email="email3")
        self.user4 = User.objects.create_user(username="User5", email="email4")

    def test_request_sent(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        self.assertEqual(Request.objects.all().count(), 1)

    def test_wrong_request_to_self(self):
        with self.assertRaises(ValidationError):
            Request.objects.send_request(from_user=self.user1, to_user=self.user1)

    def test_user_see_sent_requests(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.send_request(from_user=self.user1, to_user=self.user3)
        self.assertTrue(self.user3 in Request.objects.request_sent_list(self.user1) and
                        self.user2 in Request.objects.request_sent_list(self.user1))
        self.assertFalse(self.user4 in Request.objects.request_sent_list(self.user1))

    def test_user_see_recieved_requests(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.send_request(from_user=self.user3, to_user=self.user2)
        self.assertTrue( self.user3 in Request.objects.request_received_list(self.user2) and
                         self.user1 in Request.objects.request_received_list(self.user2))
        self.assertFalse(self.user4 in Request.objects.request_sent_list(self.user2))

    def test_request_is_acccepted(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.filter(from_user=self.user1)[0].accept()
        self.assertTrue(Friendship.objects.all().count(), 1)

    def test_are_frriends_is_working(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.filter(from_user=self.user1)[0].accept()
        self.assertTrue(Request.objects.are_friends(self.user1, self.user2))
        self.assertFalse(Request.objects.are_friends(self.user1, self.user3))

    def test_send_wrond_request_to_friend(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.filter(from_user=self.user1)[0].accept()
        with self.assertRaises(ValidationError):
            Request.objects.send_request(from_user=self.user1, to_user=self.user2)

    def test_right_friendslist_returned(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.send_request(from_user=self.user1, to_user=self.user3)
        requests = Request.objects.filter(from_user=self.user1)
        requests[0].accept()
        requests[0].accept()
        self.assertTrue(self.user2 in Request.objects.friends_list(self.user1) and
                        self.user3 in Request.objects.friends_list(self.user1))

    def test_request_is_declined(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.filter(to_user=self.user2)[0].decline()
        self.assertEqual(Request.objects.all().count(), 0)

    def test_friendship_deleted(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.filter(from_user=self.user1)[0].accept()
        self.assertTrue(Request.objects.are_friends(self.user1, self.user2))
        Friendship.objects.remove_friendship(self.user1, self.user2)
        self.assertFalse(Request.objects.are_friends(self.user1, self.user2))

