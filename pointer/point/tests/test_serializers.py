from django.test import TestCase
from django.utils import timezone

from datetime import datetime, timedelta

from users.models import User
from point.models import Pointer
from point.serializers import PointerSerializer

class TestPointerSerializer(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", \
            password="password123", email="email1@gmail.com")
        self.point = Pointer.objects.create_pointer(author=self.user1, title='party', \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def set_data(self, author, title='party', desc='party hard'):
        return {'author': author.pk, 'title': title, 'desc': desc, 'pdate': datetime.now(timezone.utc)+timedelta(days=1)}

    def test_pointer(self):
        point = Pointer.objects.filter(author=self.user1)
        serializer = PointerSerializer(point, many=True)
        self.assertEqual(serializer.data[0]['title'], self.point.title)

class TestPointerCreation(TestCase):
    pass
