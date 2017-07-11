from django.test import TestCase
from users.models import User
from friends.models import *


class FriendsViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", email="email1")
        self.user2 = User.objects.create_user(username="User2", email="email2")
        self.user3 = User.objects.create_user(username="User3", email="email3")
        self.user4 = User.objects.create_user(username="User5", email="email4")

    def createFriendships(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.filter(from_user=self.user1)[0].accept()
        Request.objects.send_request(from_user=self.user1, to_user=self.user3)
        Request.objects.filter(from_user=self.user1)[0].accept()
        Request.objects.send_request(from_user=self.user1, to_user=self.user4)
        Request.objects.filter(from_user=self.user1)[0].accept()

    def test_proper_list_of_friends_is_displayed(self):
        self.createFriendships()
        friendslist = self.client.post('/friends/friendslist/', {'username': 'User1'})
        print("Hi!")
        print(friendslist)

