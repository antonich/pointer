from django.test import TestCase
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser

from users.models import User
from rest_framework.authtoken.models import Token
from users.views import UserCreationView

BLANK_FIELD = 'This field may not be blank.'
REG_USERNAME = 'user with this username already exists.'
REG_EMAIL = 'user with this email already exists.'
WRONG_PASSWORD = 'The password is wrong.'
UNAUTH_USER = 'This user is not authenticated.'

class UserCreationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testin', \
            password="testcase123", email="testing123@gmail.com")
        self.user.is_active = True
        self.user.save()


    def setData(self, username, password, email):
        return {'username': username, 'password': password, 'email': email}

    def test_get_request(self):
        response = self.client.get("/users/register/")
        self.assertEqual(response.status_code, 405)

    def test_user_is_created_with_corret_data(self):
        data = self.setData('antonio', 'testing123', \
            'testcase123@gmail.com')

        # create user with valid data
        response = self.client.post('/users/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Anton Ziniewicz'})
        self.assertEqual(response.status_code, 201)

        self.assertEqual(User.objects.all().filter(username=data['username']).count(), 1)


    def test_fails_user_creation_with_incorrect_email(self):
        data = self.setData('antonio', 'testing123', \
            'testcase123')

        # create user with valid data
        response = self.client.post('/users/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Anton Ziniewicz'})
        self.assertEqual(response.status_code, 400)

    def test_fails_user_creation_without_username(self):
        data = self.setData('', 'testing123', \
            'testcase123@gmaik.com')

        # create user without username
        request = self.client.post('/users/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Anton Ziniewicz'})
        self.assertTrue(BLANK_FIELD in request.data['username'])

        # and code equal 400
        self.assertEqual(request.status_code, 400)

    def test_fails_user_creation_without_password(self):
        data = self.setData('antonio', '', \
            'testcase123@gmaik.com')

        # create user without username
        request = self.client.post('/users/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Anton Ziniewicz'})
        self.assertTrue(BLANK_FIELD in request.data['password'])

        # and code equal 400
        self.assertEqual(request.status_code, 400)

    def test_fails_user_creation_without_email(self):
        data = self.setData('', 'testing123', \
            '')

        # create user without username
        request = self.client.post('/users/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Anton Ziniewicz'})
        self.assertTrue(BLANK_FIELD in request.data['email'])

        # and code equal 400
        self.assertEqual(request.status_code, 400)

    def test_fails_with_already_regis_username(self):
        data = self.setData('testin', 'testing123', \
            'testcase123@gmail.com')

        # create user without username
        request = self.client.post('/users/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Anton Ziniewicz'})

        self.assertTrue(REG_USERNAME in request.data['username'])

        # and code equal 400
        self.assertEqual(request.status_code, 400)

    def test_fails_with_already_regis_email(self):
        data = self.setData('testing', 'testing123', \
            'testing123@gmail.com')

        # create user without username
        request = self.client.post('/users/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email'], 'name': 'Anton Ziniewicz'})

        self.assertTrue(REG_EMAIL in request.data['email'])

        # and code equal 400
        self.assertEqual(request.status_code, 400)


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testin', \
            password="testcase123", email="testing123@gmail.com")
        self.user.is_active = True
        self.user.save()


    def setData(self, username, password):
        return {'username': username, 'password': password}

    def test_user_login_with_correct_data(self):
        data = self.setData(self.user.username, \
            'testcase123')
        # logout before login
        self.client.logout()

        # send request to login
        request = self.client.post('/users/login/', {
            'username': data['username'], 'password': data['password']
        })
        # get current user
        user = auth.get_user(self.client)
        self.assertEqual(user, self.user)

        # check if loged user gets the same token
        token = User.objects.get_user_token(user)
        self.assertEqual(request.data['token'], token.key)

        # logout and check if user is anonymous
        self.client.logout()
        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())

    def test_unauth_user(self):
        request = self.client.post('/users/login/', {
            'username': self.user.username, 'password': '123123'
        })

        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())

        self.assertEqual(request.status_code, 401)
        self.assertEqual(UNAUTH_USER, request.data['errors'])

    def test_auth_user_cant_get_access_to_this_page(self):
        # first login
        user = self.client.login(username=self.user.username, \
            password='testcase123')

        # then post a request
        request = self.client.post('/users/login/', {
            'username': self.user.username, 'password': 'testcase123'
        })

        user = auth.get_user(self.client)
        self.assertFalse(user.is_anonymous())

        self.assertEqual(request.status_code, 400)

    def test_registered_user_doesnt_have_access_if_not_active(self):
        user = User.objects.create_user(username='antonich', \
            email="antonio123@gmail.com", password="testing123123")
        user.save()

        request = self.client.post('/users/login/', {
            'username': user.username, 'password': 'testing123123'
        })
        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())

        self.assertTrue(request.status_code, 401)
