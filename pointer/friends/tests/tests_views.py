from django.test import TestCase
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout

from rest_framework import status
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

from users.models import User
from friends.models import *
from users.serializers import UserSerializer


class RequestViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", password="password123", email="email1@gmail.com")
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user(username="User2", email="email2")
        self.user3 = User.objects.create_user(username="User3", email="email3")
        self.user4 = User.objects.create_user(username="User4", email="email4")
        user = self.client.login(username=self.user1.username, \
            password='password123')


    def tearDown(self):
        self.client.logout()

    def createRequests(self):
        Request.objects.send_request(from_user=self.user2, to_user=self.user1)
        Request.objects.send_request(from_user=self.user2, to_user=self.user3)
        Request.objects.send_request(from_user=self.user1, to_user=self.user4)

    def test_list_of_received_requests_is_displayed(self):
        self.createRequests()
        friends_request = self.client.get('/friends/received_requests_list/')
        # user1 have request from user2
        self.assertEqual(friends_request.status_code, 200)
        self.assertEqual(friends_request.data[0]['username'], 'User2')
        # check for number of requests
        self.assertEqual(len(friends_request.data), 1)

    def test_list_of_received_requests_is_displayed_2(self):
        self.createRequests()
        # add one more request
        Request.objects.send_request(from_user=self.user3, to_user=self.user1)
        friends_request = self.client.get('/friends/received_requests_list/')
        self.assertEqual(len(friends_request.data), 2)


    def test_list_of_sent_requests_is_displayed(self):
        self.createRequests()
        user_requests = self.client.get('/friends/sent_requests_list/')
        self.assertEqual(user_requests.status_code, 200)

        self.assertEqual(user_requests.data[0]['username'], 'User4')
        # check for number of requests
        self.assertEqual(len(user_requests.data), 1)

    def test_list_of_sent_requests_is_displayed_2(self):
        self.createRequests()
        # add one more request from user1
        Request.objects.send_request(from_user=self.user1, to_user=self.user3)

        user_requests = self.client.get('/friends/sent_requests_list/')
        self.assertEqual(user_requests.status_code, 200)

        # check for number of requests
        self.assertEqual(len(user_requests.data), 2)

    def test_send_correct_request(self):
        response = self.client.post("/friends/send_request/" + str(self.user2.pk) + '/')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Request.objects.all().count(), 1)

    def test_send_request_with_unknown_user(self):
        response = self.client.post("/friends/send_request/" + str(15) + '/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Request.objects.all().count(), 0)

    def test_send_request_to_itself(self):
        response = self.client.post("/friends/send_request/" + str(self.user1.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Request.objects.all().count(), 0)
        self.assertEqual(response.data['detail'], SAME_USER_ERROR)

    def test_send_same_request_twice(self):
        response1 = self.client.post("/friends/send_request/" + str(self.user2.pk) + '/')
        response2 = self.client.post("/friends/send_request/" + str(self.user2.pk) + '/')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.data['detail'], ALREADY_EXISTS_ERROR)

    def test_send_request_to_friend(self):
        Friendship.objects.create_friendship(self.user1, self.user2)
        response = self.client.post("/friends/send_request/" + str(self.user2.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Request.objects.all().count(), 0)
        self.assertEqual(response.data['detail'], ALREADY_FRIENDS_ERROR)

    def test_accept_request(self):
        Request.objects.send_request(from_user=self.user2, to_user=self.user1)
        response = self.client.post("/friends/accept_request/" + str(self.user2.pk) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Friendship.objects.are_friends(self.user1, self.user2))

    def test_anonymous_user_unable_to_do_stuff(self):
        self.client.logout()
        response = self.client.post("/friends/send_request/" + str(self.user2.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_decline_request(self):
        Request.objects.send_request(from_user=self.user2, to_user=self.user1)
        response = self.client.post("/friends/decline_request/" + str(self.user2.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Request.objects.all().count(), 0)


class RequestViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", password="password123", email="email1@gmail.com")
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user(username="User2", email="email2")
        self.user3 = User.objects.create_user(username="User3", email="email3")
        self.user4 = User.objects.create_user(username="User4", email="email4")
        user = self.client.login(username=self.user1.username, \
            password='password123')


    def tearDown(self):
        self.client.logout()

    def createRequests(self):
        Request.objects.send_request(from_user=self.user2, to_user=self.user1)
        Request.objects.send_request(from_user=self.user2, to_user=self.user3)
        Request.objects.send_request(from_user=self.user1, to_user=self.user4)

    def createFriendships(self):
        Friendship.objects.create_friendship(from_user=self.user2, to_user=self.user1)
        Friendship.objects.create_friendship(from_user=self.user2, to_user=self.user3)
        Friendship.objects.create_friendship(from_user=self.user1, to_user=self.user4)

    def test_list_of_friends_is_displayed(self):
        self.createFriendships()
        friendslist = self.client.get("/friends/friends_list/")
        self.assertEqual(friendslist.status_code, 200)
        self.assertEqual(len(friendslist.data), len(Friendship.objects.friends_list(self.user1)))

    def test_remove_friendship(self):
        friendship = Friendship.objects.create_friendship(from_user=self.user1, to_user=self.user2)
        response = self.client.post("/friends/remove_friendship/" + str(self.user2.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Friendship.objects.all().count(), 0)

    def test_remove_friendship_with_unfriended(self):
        friendship = Friendship.objects.create_friendship(from_user=self.user1, to_user=self.user2)
        response = self.client.post("/friends/remove_friendship/" + str(self.user3.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Friendship.objects.are_friends(self.user1, self.user3))
