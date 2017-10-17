from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

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

    def test_user_is_deleted(self):
        u = self.createUser(self.username, self.email, '')
        u.save()

        self.assertEqual(User.objects.get(username=self.username), u)

        #delete this user
        u.delete()
        self.assertEqual(User.objects.all().count(), 0)

    def testUserFailsWithoutEmail(self):
        with self.assertRaises(ValueError):
            user = self.createUser(email="", username=self.username, password=self.password)

    def testUserFailsWithoutUsername(self):
        with self.assertRaises(ValueError):
            user = self.createUser(email=self.email, username="", password=self.password)

    def testUserWithDescMoreThan100(self):
        with self.assertRaises(ValidationError):
            user = self.createUser(email=self.email, username=self.username, password=self.password, desc='sandoiasndoia\
                sdofndsonfodsinfosidnfosdnfodnsoifnwoifnpwemf-wejf-wefnw-eofnweoinfoiwenfoiwenoifnweoifnwoeifoiwnefoinwoifnw')

    ''' Not necessary '''
    def testUserWithAlreadyUsedEmailOrUsername(self):
        user = self.createUser(self.username, self.email, self.password)
        # Checks if user is in use with used username or email
        with self.assertRaises(ValidationError):
            User.objects.is_already_in_use(self.email, self.username)

    def testUserWithAlreadyUsedEmailOrUsernameWithoutUserObject(self):
        user = self.createUser(self.username, self.email, self.password)

        try:
            user1 = self.createUser(self.username, self.email, self.password)
            user1.save()
        except IntegrityError:
            pass
