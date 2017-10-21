from django.test import TestCase
from django.utils import timezone

from rest_framework import status

from datetime import datetime, timedelta

from users.models import User
from point.models import Pointer
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
        return Pointer.objects.create_pointer(author=self.user2, title=title, \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def test_empty_pointer_list(self):
        pointer_request = self.client.get('/point/pointer_list/')

        self.assertEqual(pointer_request.status_code, 200)
        self.assertEqual(len(pointer_request.data), 0)

    def test_2_item_pointer_list(self):
        pass
        # point1 = self.create_pointer('party hard 1')
        # point2 = self.create_pointer('party2')
        # mem1 = Member.objects.create_member(user=self.user1, pointer=point1)
        # mem1 = Member.objects.create_member(user=self.user1, pointer=point2)
        #
        # pointer_request = self.client.get('/point/pointer_list/')
        # self.assertEqual(pointer_request.status_code, 200)
        # self.assertEqual(len(pointer_request.data), 2)
