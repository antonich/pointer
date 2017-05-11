from django.test import TestCase
from rest_framework import serializers

from users.serializers import UserCreationSerializer
from users.models import User

class UserCreationSerializerTest(TestCase):
    def set_data(self, usern='test123', email='test123@gmail.com', passw='testcase123', name=''):
        return {'username': usern, 'email': email, 'password': passw, 'name': name}

    def test_create_user_with_correct_data(self):
        self.data = self.set_data()
        serial = UserCreationSerializer(data=self.data)
        self.assertTrue(serial.is_valid())

        serial.save()
        self.assertEqual(User.objects.all().filter(username=self.data['username']).count(), 1)

    def test_already_registered_user(self):
        self.data = self.set_data()
        user1 = User.objects.create_user(username=self.data['username'], \
            email=self.data['email'], password=self.data['password'])

        with self.assertRaises(serializers.ValidationError):
            serial = UserCreationSerializer(data=self.data)
            self.assertFalse(serial.is_valid(raise_exception=True))

    def test_username_is_required(self):
        self.data = self.set_data(usern='')

        with self.assertRaises(serializers.ValidationError):
            serial = UserCreationSerializer(data=self.data)
            self.assertFalse(serial.is_valid(raise_exception=True))

    def test_email_is_required(self):
        self.data = self.set_data(email='')

        with self.assertRaises(serializers.ValidationError):
            serial = UserCreationSerializer(data=self.data)
            self.assertFalse(serial.is_valid(raise_exception=True))

    def test_password_is_required(self):
        self.data = self.set_data(passw='')

        with self.assertRaises(serializers.ValidationError):
            serial = UserCreationSerializer(data=self.data)
            self.assertFalse(serial.is_valid(raise_exception=True))

    def test_user_with_no_name_is_spoko(self):
        self.data = self.set_data(name='')
        serial = UserCreationSerializer(data=self.data)
        self.assertTrue(serial.is_valid())
