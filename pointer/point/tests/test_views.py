from django.test import TestCase
from django.utils import timezone
from django.contrib import auth

from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIClient

from datetime import datetime, timedelta

from users.models import User
from point.models import Pointer, PublicPointer, PrivatePointer
from members.models import Member
from members.choices import *
from point.serializers import PointerSerializer
from friends.models import Friendship

class TestPointer(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", \
            password="password123", email="email1@gmail.com")
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create_user(username="test", \
            password="password123", email="testing@gmail.com")
        user = self.client.login(username=self.user1.username, \
            password='password123')

    def tearDown(self):
        self.client.logout()

    def create_pointer(self, title='party'):
        return Pointer.objects.create_pointer(author=self.user1, title=title, \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def create_pointer_with_user(self, u, title='party'):
        return Pointer.objects.create_pointer(author=u, title=title, \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def test_pointer_list(self):
        self.create_pointer()
        self.create_pointer(title="party hard2")
        pointer_request = self.client.get('/point/author_pointer_list/')
        self.assertEqual(Pointer.objects.filter(author=self.user1).count(), 2)

    def test_token_auth(self):
        self.client.logout()
        token = Token(user=self.user1)
        token.save()
        request = self.client.get('/point/author_pointer_list/', HTTP_AUTHORIZATION="Token {}".format(token))

    def test_with_point_list(self):
        self.client.logout()
        self.create_pointer(title="party1")
        self.create_pointer(title="party2")
        token = Token(user=self.user1)
        token.save()
        request = self.client.get('/point/author_pointer_list/', HTTP_AUTHORIZATION="Token {}".format(token))

        self.assertEqual(len(request.data), 2)

    def test_user_pointer_story(self):
        self.client.logout()
        user2 = User.objects.create_user(username="2", \
            password="pass2", email="email2")
        user3 = User.objects.create_user(username="3", \
            password="pass3", email="email3")
        user4 = User.objects.create_user(username="4", \
            password="pass4", email="email4")
        self.create_pointer_with_user(user2, 'party1')
        self.create_pointer_with_user(user3, 'party2')
        self.create_pointer_with_user(user4, 'party3')
        self.create_pointer_with_user(user2, 'party123')

        fr1 = Friendship.objects.create_friendship(self.user1, user2)
        Friendship.objects.create_friendship(self.user1, user3)
        Friendship.objects.create_friendship(self.user1, user4)
        # not friends with self.user5

        token = Token(user=self.user1)
        token.save()
        request = self.client.get('/point/user_story_list/', HTTP_AUTHORIZATION="Token {}".format(token))
        self.assertEqual(len(request.data), 4)

        # if self.user1 not friends with user2 then only 2 pointer in story
        fr1.delete()
        request = self.client.get('/point/user_story_list/', HTTP_AUTHORIZATION="Token {}".format(token))
        self.assertEqual(len(request.data), 2)

class TestPublicPointer(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", \
            password="password123", email="email1@gmail.com")
        self.user2 = User.objects.create_user(username="test", \
            password="password123", email="testing@gmail.com")
        token = Token.objects.create(user=self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=self.user1)

    def tearDown(self):
        self.client.logout()

    def create_ppointer(self, title='party'):
        return PublicPointer.objects.create_pointer(author=self.user2, title=title, \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def test_create_ppointer(self):
        pointer_request = self.client.post('/point/create_public_pointer/', {
            'author': self.user1.pk, 'title': 'hard party na hatie', \
                'description': 'party', 'pointer_date':datetime.now(timezone.utc)+timedelta(days=1)
        })
        self.assertEqual(pointer_request.status_code, 201)
        self.assertEqual(Pointer.objects.filter(author=self.user1, title='hard party na hatie').count(), 1)

    def test_create_pointer_without_field(self):
        pointer_request = self.client.post('/point/create_public_pointer/', {
            'title': 'hard party na hatie', \
                'description': 'party', 'pointer_date':datetime.now(timezone.utc)+timedelta(days=1)
        })
        # self.assertpointer_request.data['author']
        self.assertEqual(pointer_request.status_code, 400)

    def test_create_pointer_with_unknown_user(self):
        pointer_request = self.client.post('/point/create_public_pointer/', {
            'author': self.user1.pk+100, 'title': 'hard party na hatie', \
                'description': 'party', 'pointer_date':datetime.now(timezone.utc)+timedelta(days=1)
        })
        self.assertEqual(pointer_request.status_code, 400)

    def test_delete_ppointer(self):
        pointer_request = self.client.post('/point/create_public_pointer/', {
            'author': self.user1.pk, 'title': 'hard party na hatie', \
                'description': 'party', 'pointer_date':datetime.now(timezone.utc)+timedelta(days=1)
        })
        self.assertEqual(pointer_request.status_code, 201)
        # delete this pointer
        point2 = Pointer.objects.get(author=self.user1, title='hard party na hatie')
        pointer_request = self.client.delete('/point/delete_pointer/' + str(point2.pk) +'/')

        self.assertEqual(pointer_request.status_code, 202)

    def test_delete_non_existed_ppointer(self):
        pointer_request = self.client.delete('/point/delete_pointer/' + str(10) + '/')

        self.assertEqual(pointer_request.status_code, 404)

    def test_join_existing_pointer(self):
        # user2 creates pointer
        pointer = self.create_ppointer()
        pointer_request = self.client.put('/point/join_pointer/'+str(pointer.pk)+'/')
        self.assertEqual(Member.objects.filter(user=self.user1, pointer=pointer).count(), 1)
        self.assertEqual(pointer_request.status_code, 201)

    def test_join_non_existing_pointer(self):
        # user2 creates pointer
        pointer = self.create_ppointer()
        pointer_request = self.client.put('/point/join_pointer/'+str(pointer.pk+100)+'/')
        self.assertEqual(Member.objects.filter(user=self.user1, pointer=pointer).count(), 0)
        self.assertEqual(pointer_request.status_code, 404)

class TestPrivatePointer(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", \
            password="password123", email="email1@gmail.com")
        self.user2 = User.objects.create_user(username="test", \
            password="password123", email="testing@gmail.com")
        token = Token.objects.create(user=self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=self.user1)

    def tearDown(self):
        self.client.logout()

    def create_prpointer(self, title='party'):
        return PrivatePointer.objects.create_pointer(author=self.user2, title=title, \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def test_create_ppointer(self):
        pointer_request = self.client.post('/point/create_private_pointer/', {
            'author': self.user1.pk, 'title': 'hard party na hatie', \
                'description': 'party', 'pointer_date':datetime.now(timezone.utc)+timedelta(days=1)
        })
        self.assertEqual(pointer_request.status_code, 201)
        self.assertEqual(Pointer.objects.filter(author=self.user1, title='hard party na hatie').count(), 1)

    def test_create_prointer_without_field(self):
        pointer_request = self.client.post('/point/create_private_pointer/', {
            'title': 'hard party na hatie', \
                'description': 'party', 'pointer_date':datetime.now(timezone.utc)+timedelta(days=1)
        })
        # self.assertpointer_request.data['author']
        self.assertEqual(pointer_request.status_code, 400)
