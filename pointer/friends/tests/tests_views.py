from django.test import TestCase
from users.models import User
from friends.models import *
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from rest_framework import status



class FriendsViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", password="password123", email="email1")
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user(username="User2", email="email2")
        self.user3 = User.objects.create_user(username="User3", email="email3")
        self.user4 = User.objects.create_user(username="User4", email="email4")
        self.user = authenticate(username="User1", password="password123")
        self.client.login(username="User1", password="password123")

    def tearDown(self):
        self.client.logout()

    def createRequests(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.send_request(from_user=self.user1, to_user=self.user3)
        Request.objects.send_request(from_user=self.user1, to_user=self.user4)

    def createFriendships(self):
        self.createRequests()
        while Request.objects.filter(from_user=self.user1):
            Request.objects.filter(from_user=self.user1)[0].accept()

    def test_list_of_received_requests_is_displayed(self):
        Request.objects.send_request(from_user=self.user2, to_user=self.user1)
        Request.objects.send_request(from_user=self.user3, to_user=self.user1)
        Request.objects.send_request(from_user=self.user4, to_user=self.user1)
        requestslist = self.client.get('/friends/received_requests_list/')
        requestslist.render()
        print("Received requests list")
        print(requestslist.content)
        self.assertEqual(requestslist.status_code, 200)

    def test_list_of_sent_requests_is_displayed(self):
        self.createRequests()
        requestslist = self.client.get('/friends/sent_requests_list/')
        requestslist.render()
        print("Sent requests:")
        print(requestslist.content)
        self.assertEqual(requestslist.status_code, 200)

    def test_list_of_friends_is_displayed(self):
        self.createFriendships()
        friendslist = self.client.get("/friends/friends_list/")
        friendslist.render()
        print("Friends:")
        print(friendslist.content)
        self.assertEqual(friendslist.status_code, 200)

    def test_send_new_request(self):
        response = self.client.post("/friends/send_request/User2/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Request.objects.all().count(), 1)\

    def test_send_new_request_to_itself(self):
        response = self.client.post("/friends/send_request/User1/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Request.objects.all().count(), 0)

    def test_accept_request(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request = Request.objects.get(from_user=self.user1, to_user=self.user2)
        response = self.client.post("/friends/accept_request/%d/" % request.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Friendship.objects.all().count(), 1)

    def test_anonymous_user_unable_to_see_stuff(self):
        self.client.logout()
        self.createRequests()
        response = self.client.get('/friends/sent_requests_list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        Request.objects.send_request(from_user=self.user2, to_user=self.user1)
        Request.objects.send_request(from_user=self.user3, to_user=self.user1)
        Request.objects.send_request(from_user=self.user4, to_user=self.user1)
        response = self.client.get('/friends/received_requests_list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        while Request.objects.filter(from_user=self.user1):  # accept requests
            Request.objects.filter(from_user=self.user1)[0].accept()
        response = self.client.get("/friends/friends_list/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_unable_to_do_stuff(self):
        self.client.logout()
        response = self.client.post("/friends/send_request/User2/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        request = Request.objects.get(from_user=self.user1, to_user=self.user2)
        response = self.client.post("/friends/accept_request/%d/" % request.id)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_accept_nonexistent_request(self):
        response = self.client.post("/friends/accept_request/1/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_decline_request(self):
        Request.objects.send_request(from_user=self.user2, to_user=self.user1)
        request = Request.objects.get(from_user=self.user2, to_user=self.user1)
        response = self.client.post("/friends/decline_request/%d/" % request.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Request.objects.all().count(), 0)

    def test_user_can_decline_only_its_requests(self):
        Request.objects.send_request(from_user=self.user3, to_user=self.user2)
        request = Request.objects.get(from_user=self.user3, to_user=self.user2)
        response = self.client.post("/friends/decline_request/%d/" % request.id)
        self.assertEqual(Request.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_friendship(self):
        Request.objects.send_request(from_user=self.user1, to_user=self.user2)
        Request.objects.filter(from_user=self.user1)[0].accept()
        friendship = Friendship.objects.get(from_user=self.user1, to_user=self.user2)
        response = self.client.post("/friends/remove_friendship/%d/" % friendship.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Friendship.objects.all().count(), 0)

    def test_user_cant_remove_not_itself_friendship(self):
        Request.objects.send_request(from_user=self.user3, to_user=self.user2)
        Request.objects.filter(from_user=self.user3)[0].accept()
        friendship = Friendship.objects.get(from_user=self.user3, to_user=self.user2)
        response = self.client.post("/friends/remove_friendship/%d/" % friendship.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Friendship.objects.all().count(), 1)

