from django.test import TestCase


class TestPointer(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="User1", password="password123", email="email1@gmail.com")
        self.user1.save()
        user = self.client.login(username=self.user1.username, \
            password='password123')

    def tearDown(self):
        self.client.logout()

    def test_pointer_list(self):
        pass
