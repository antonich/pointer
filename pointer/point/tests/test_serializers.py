from django.test import TestCase
from django.utils import timezone

from datetime import datetime, timedelta

from users.models import User
from point.models import Pointer
from point.serializers import PointerSerializer, PointerSerializerData, FeedItemSerializer
from members.models import Member

class TestPointerSerializer(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", \
            password="password123", email="email1@gmail.com")
        self.point = Pointer.objects.create_pointer(author=self.user1, title='party', \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def set_data(self, author, title='party', desc='party hard'):
        return {'author': author.pk, 'title': title, 'desc': desc, \
            'pdate': datetime.now(timezone.utc)+timedelta(days=1)}

    def test_pointer(self):
        point = Pointer.objects.filter(author=self.user1)
        serializer = PointerSerializer(point, many=True)
        self.assertEqual(serializer.data[0]['title'], self.point.title)

    def test_serial_with_user(self):
        serial = PointerSerializerData(self.point)
        self.assertEqual(serial.data['id'], self.point.id)

    def test_pointer_list_serial_with_user(self):
        Pointer.objects.create_pointer(author=self.user1, title='party123', \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))
        pointer_list = Pointer.objects.filter(author=self.user1)
        serial = PointerSerializerData(pointer_list, many=True)
        self.assertEqual(len(serial.data), 2)

    def test_point_feedserial(self):
        user2 = User.objects.create_user(username="User2", \
            password="password123", email="email2@gmail.com")
        user3 = User.objects.create_user(username="User3", \
            password="password123", email="email3@gmail.com")
        Member.objects.create_member(user2, self.point)
        Member.objects.create_member(user3, self.point)
        pointer_list = Pointer.objects.filter(author=self.user1)
        serial = FeedItemSerializer(pointer_list, context={'user': user3}, many=True)

class TestPointerCreation(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", \
            password="password123", email="email1@gmail.com")

    def test_create_pointer(self):
        serial = PointerSerializer(data={'author': self.user1.pk, \
            'title': 'party hard', 'description': 'going to party', \
                'pointer_date': datetime.now(timezone.utc)+timedelta(days=1)
        })
        serial.is_valid()

        serial.save()
        self.assertEqual(Pointer.objects.filter(author=self.user1).count(), 1)
