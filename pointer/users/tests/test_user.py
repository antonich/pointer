from django.test import TestCase
from rest_framework import serializers
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser

from users.models import User

class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='antonich', \
            password='testing123', email='testcase@gmail.com')

        self.user.is_active = True
        self.user.save()

    def setData(self, username, password):
        return {'username': username, 'password': password}

    def test_user_is_authentication(self):
        data = self.setData('antonich', 'testing123')
        user = authenticate(username=data['username'], password=data['password'])
        self.assertTrue(user.is_authenticated)

    def test_user_authentication_fails(self):
        data = self.setData('antonich', 'testio')
        user1 = authenticate(username=data['username'], password=data['password'])
        self.assertEqual(user1, None)

        user2 = self.client.login(username=data['username'], \
            password=data['password'])
        self.assertFalse(user2)


    def test_user_is_logged_in(self):
        data = self.setData('antonich', 'testing123')
        user = authenticate(username=data['username'], password=data['password'])
        self.assertTrue(user.is_authenticated)

        self.client.login(username=data['username'], \
        password=data['password'])

        # Checks if user is created
        user = auth.get_user(self.client)
        self.assertEqual(user, self.user)

        # Checks if user was logged out
        self.client.logout()
        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())
