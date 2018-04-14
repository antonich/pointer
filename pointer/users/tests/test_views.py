from django.test import TestCase
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from users.models import User
from rest_framework.authtoken.models import Token
from users.views import UserCreationView
from users.exceptions import *

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

    def test_fails_user_creation_without_name(self):
        data = self.setData('testin123123', 'testing123', \
            'testcase123@gmail.com')

        # create user without username
        request = self.client.post('/users/register/', { \
            'username': data['username'], 'password': data['password'], \
                'email': data['email']})
        self.assertEqual(request.status_code, 201)

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

    def test_user_login_with_correct_data_gets_token(self):
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
        self.assertEqual(UNAUTH_USER, request.data['detail'])

    def test_auth_user_cant_get_access_to_this_page(self):
        # then post a request
        request = self.client.post('/users/login/', {
            'username': self.user.username, 'password': 'testcase123'
        })

        user = auth.get_user(self.client)
        self.assertFalse(user.is_anonymous())

        self.assertEqual(request.status_code, 200)

# active is now set to true as default
    # def test_registered_user_doesnt_have_access_if_not_active(self):
    #     user = User.objects.create_user(username='antonich', \
    #         email="antonio123@gmail.com", password="testing123123")
    #     user.save()
    #
    #     request = self.client.post('/users/login/', {
    #         'username': user.username, 'password': 'testing123123'
    #     })
    #     user = auth.get_user(self.client)
    #     self.assertTrue(user.is_anonymous())
    #
    #     self.assertTrue(request.status_code, 401)


class UserActivationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testin', \
            password="testcase123", email="testing123@gmail.com")
        self.user.is_active = False
        self.user.save()

    def test_user_cant_login_because_is_not_active(self):
        # through client login
        user = self.client.login(username=self.user.username, \
            password='testcase123')

        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())

        # through post view request
        request = self.client.post('/users/login/', {
            'username': self.user.username, 'password': 'testcase123'
        })

        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())

    def test_user_activate_account(self):
        user = User.objects.create_user(username='antonich123', \
            email='testing@gmail.com', password="testing123")
        user.save()
        request = self.client.post('/users/activate/' + user.activation_key)

        # get user after request
        user1 = User.objects.get(activation_key=user.activation_key)
        self.assertTrue(user1.is_active)

        # now user can login
        self.assertTrue(self.client.login(username=user.username, \
            password="testing123"))

        # check if login user is the same as wanted
        user1 = auth.get_user(self.client)
        self.assertEqual(user1, user)




class UserLogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testin', \
            password="testcase123", email="testing123@gmail.com")
        self.user.is_active = True
        self.user.save()


    def test_token_deletes_after_loging_out(self):
        self.client.logout()
        # to get token for self.user
        request = self.client.post('/users/login/', {
            'username': self.user.username, 'password': 'testcase123'
        })
        self.client.logout()

        token = User.objects.get_user_token(self.user)

        authoriz = 'Token ' + str(token)

        # check token deletes after loging out
        request = self.client.post('/users/logout/', HTTP_AUTHORIZATION="Token {}".format(token))

        # check if not anonymous
        user = auth.get_user(self.client)
        self.assertTrue(user.is_anonymous())

        # Validation error because token was deleted after logout
        with self.assertRaises(NoTokenForUser):
            token = User.objects.get_user_token(self.user)

class SocialUserTest(TestCase):
    def setUp(self):
        self.user_access_token = 'EAACHaTaBVBgBADILNs3vaMP9DRepu75xJzry8rulGvt3Wa2du7rAqDzpRlnj5NGnUb6r4Km9BFmyUm4KO8shujzgvixbQZAhZCwRGWxSZA5eGrFDAKz9LTCVMvwVARR2Pq9sGndHoWZBaZA1xhwt0PxtJKSEeOo8cA5wLbHHjj4vDr7I5ruys9tfNxK2JHAaTx4BsEFJF3yWX2wUzQ7ZALNkdUhuiW8La6vK1BQbzIGlTBOYvBjzr8'

    def test_user_register_with_facebook(self):
        pass
        # request = self.client.post('/users/social/facebook/', {'access_token': self.user_access_token})
        # try:
        #     # User.objects.all()[0].email
        #     User.objects.all()[0].name
        # except:
        #     pass
