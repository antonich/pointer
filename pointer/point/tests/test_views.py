from django.test import TestCase
from django.utils import timezone

from rest_framework import status

from datetime import datetime, timedelta

from users.models import User
from point.models import Pointer, PublicPointer
from members.models import Member
from members.choices import *

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

    def test_create_pointer(self):
        pointer_request = self.client.post('/point/create_pointer/', {
            'author': self.user1.pk, 'title': 'hard party na hatie', \
                'description': 'party', 'pointer_date':datetime.now(timezone.utc)+timedelta(days=1)
        })
        self.assertEqual(pointer_request.status_code, 201)
        self.assertEqual(Pointer.objects.filter(author=self.user1, title='hard party na hatie').count(), 1)

    def test_create_pointer_without_field(self):
        pointer_request = self.client.post('/point/create_pointer/', {
            'title': 'hard party na hatie', \
                'description': 'party', 'pointer_date':datetime.now(timezone.utc)+timedelta(days=1)
        })
        self.assertEqual(pointer_request.status_code, 400)

    def test_pointer_list(self):
        self.create_pointer()
        self.create_pointer(title="party hard2")
        pointer_request = self.client.get('/point/author_pointer_list/')
        self.assertEqual(Pointer.objects.filter(author=self.user1).count(), 2)

class TestPublicPointer(TestCase):
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

    def create_ppointer(self, title='party'):
        return PublicPointer.objects.create_pointer(author=self.user2, title=title, \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def test_join_existing_pointer(self):
        # user2 creates pointer
        pointer = self.create_ppointer()
        pointer_request = self.client.get('/point/join_pointer/'+str(pointer.pk)+'/')
        self.assertEqual(Member.objects.filter(user=self.user1, pointer=pointer).count(), 1)
        self.assertEqual(pointer_request.status_code, 201)

    def test_join_non_existing_pointer(self):
        # user2 creates pointer
        pointer = self.create_ppointer()
        pointer_request = self.client.get('/point/join_pointer/'+str(pointer.pk+100)+'/')
        self.assertEqual(Member.objects.filter(user=self.user1, pointer=pointer).count(), 0)
        self.assertEqual(pointer_request.status_code, 404)
