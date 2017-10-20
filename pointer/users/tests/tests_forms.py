from django.test import TestCase

from users.models import User
from users.forms import UserCreationForm

'''
    MORE TESTS!!!
'''

class UserCreationFormTest(TestCase):
    def setData(self, username, email, password1, pass2):
        return {'username': username, 'email': email, 'password1': password1, 'password2': pass2}

    def setUp(self):
        self.data = self.setData(username='antonich', email='antonich@gmail.com', password1='test123', pass2='test123')

    def test_form_with_valid_data(self):
        form = UserCreationForm(self.data)
        self.assertTrue(form.is_valid())

        form.save()
        self.assertEqual(User.objects.all().filter(email=self.data['email']).count(), 1)
