from django.test import TestCase
from django.utils import timezone

from datetime import datetime, timedelta

from users.models import User
from point.models import Pointer
from members.models import Member
from members.serializers import MemberSerializer

class MemberTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", \
            password="password123", email="email1@gmail.com")
        self.point = Pointer.objects.create_pointer(author=self.user1, title='party', \
            desc='party hard', pdate=datetime.now(timezone.utc)+timedelta(days=1))
        self.user2 = User.objects.create_user(username="User123", \
            password="password123", email="testin1@gmail.com")

    def set_data(self, user, pointer):
        return {'user': user.pk, 'pointer': pointer.pk}

    def test_member(self):
        member = Member.objects.filter(user=self.user1)
        serializer = MemberSerializer(member, many=True)
        self.assertEqual(serializer.data[0]['pointer'], self.point.pk)

    def test_member_is_created(self):
        serial = MemberSerializer(data={'user': self.user2.pk, 'pointer': self.point.pk})
        self.assertTrue(serial.is_valid())

        serial.save()
        # 2 plus pointer author
        self.assertEqual(Member.objects.all().count(), 2)
