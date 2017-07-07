from django.test import TestCase
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser

from users.models import User
from users.views import UserCreationView

BLANK_FIELD = 'This field may not be blank.'
REG_USERNAME = 'user with this username already exists.'
REG_EMAIL = 'user with this email already exists.'

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

        request = self.client.post('/users/login/', {
            'username': data['username'], 'password': data['password']
        })
        self.assertEqual(request.status_code, 200)
