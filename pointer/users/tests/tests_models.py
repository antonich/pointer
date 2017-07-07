from django.test import TestCase
from django.utils.html import escape
from django.contrib.auth.models import *
from django.core.exceptions import ValidationError
from django.db.models import Q

from users.models import User


class UserTest(TestCase):
    def setUp(self):
        self.password = 'test123'
        self.email, self.username = 'antonich@gmail.com', 'antonich'

    def createUser(self, username, email, password, desc=""):
        return User.objects.create_user(email=email, username=username, password=password, description=desc)

    def testUserCreatesWithCorrectData(self):
        user = self.createUser(username=self.username, email=self.email, password=self.password)
        user.save()

        self.assertEqual(User.objects.all().filter(email=self.email).count(), 1)

    def testUserFailsWithoutEmail(self):
        with self.assertRaises(ValueError):
            self.createUser(email="", username=self.username, password=self.password)

    def testUserFailsWithoutUsername(self):
        with self.assertRaises(ValueError):
            user = self.createUser(email=self.email, username="", password=self.password)

    def testUserWithDescMoreThan100(self):
        with self.assertRaises(ValidationError):
            user = self.createUser(email=self.email, username=self.username, password=self.password, desc='sandoiasndoia\
                sdofndsonfodsinfosidnfosdnfodnsoifnwoifnpwemf-wejf-wefnw-eofnweoinfoiwenfoiwenoifnweoifnwoeifoiwnefoinwoifnw')

