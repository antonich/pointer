from django.test import TestCase

from point.models import Pointer
from users.models import User
from members.models import Member

class TestPointer(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='testing@gmail.com', \
            username='testing123')

    def create_pointer(self):
        return Pointer.objects.create_pointer(author=self.user1, title="party", \
            desc='party hard')

    def test_point_is_created_correctly(self):
        point = self.create_pointer()
        self.assertTrue(Pointer.objects.all(), 1)

    def test_pointer_missing_some_value(self):
        # without author
        with self.assertRaises(ValueError):
            point = Pointer.objects.create_pointer(title="party", \
                desc='party hard')

        # without title
        with self.assertRaises(ValueError):
            point = Pointer.objects.create_pointer(author=self.user1, \
                desc='party hard')

    def test_two_and_more_pointer_with_the_same_name_for_one_user_not_allowed(self):
        with self.assertRaises(ValueError):
            point1 = self.create_pointer()
            point2 = self.create_pointer()

    def test_pointer_signal_sent(self):
        point = self.create_pointer()
        self.assertEqual(Member.objects.all().count(), 1)
