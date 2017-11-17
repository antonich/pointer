from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User
from point.models import Pointer, PublicPointer, PrivatePointer
from members.models import Member
from members.views import MemberListView

from datetime import datetime, timedelta
from django.utils import timezone

class MemberTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", \
            password="password123", email="email1@gmail.com")
        self.user2 = User.objects.create_user(username="test", \
            password="password123", email="testing@gmail.com")
        token = Token.objects.create(user=self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=self.user1)

        self.point = PublicPointer.objects.create_pointer(author=self.user1, title='party hard', \
            desc='party hard very very hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def tearDown(self):
        self.client.logout()

    def test_member_list_view(self):
        request = self.client.get('/members/members_list/'+str(self.point.pk)+'/')

        self.assertEqual(request.status_code, 200)

    def test_going_member_list(self):
        self.point.join(self.user2)
        request = self.client.get('/members/going_members/'+str(self.point.pk)+'/')

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data[1]['id'], self.user2.id)
        self.assertEqual(len(request.data), 2)

    def test_decline_member_list(self):
        self.point.join(self.user2)
        self.point.decline(self.user2)
        request = self.client.get('/members/decline_members/'+str(self.point.pk)+'/')

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data[0]['id'], self.user2.id)
        self.assertEqual(len(request.data), 1)

    def test_member_list_view(self):
        request = self.client.get('/members/members_list/'+str(self.point.pk+100)+'/')

        self.assertEqual(request.status_code, 404)
