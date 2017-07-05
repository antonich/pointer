from django.test import TestCase
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser

from users.models import User
from users.views import UserCreationView

class UserCreationSerializerViewTest(TestCase):
    # def setUp(self):
    #     self.user = User.objects.create_user(username='antonich', \
    #         password='testing123', email='testcase@gmail.com')
    #
    #     self.user.is_active = True
    #     self.user.save()

    def setData(self, username, password, email):
        return {'username': username, 'password': password, 'email': email}

    def test_user_with_corret_data(self):
        data = self.setData('antonio', 'testing123', \
            'testcase123@gmail.com')

        # create user with valid data
        response = self.client.post('/users/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Anton Ziniewicz'})
        self.assertEqual(response.status_code, 201)

        self.assertEqual(User.objects.all().filter(username=data['username']).count(), 1)


    def test_user_with_incorrect_email(self):
        data = self.setData('antonio', 'testing123', \
            'testcase123@l.com')

        # create user with valid data
        response = self.client.post('/users/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Anton Ziniewicz'})
        self.assertEqual(response.status_code, 400)
