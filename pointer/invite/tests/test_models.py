from django.test import TestCase
from django.utils import timezone

from datetime import datetime, timedelta

from invite.models import Invite
from users.models import User
from point.models import PrivatePointer
from invite.exceptions import *

class TestInvite(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='testing@gmail.com', \
            username='testing123')
        self.point = PrivatePointer.objects.create_pointer(author=self.user1, title="party hard", \
            desc="we are partying hard today", pdate=datetime.now(timezone.utc)+timedelta(days=1))

    def test_creating_invite(self):
        invite = Invite.objects.create_invite(self.user1, self.point)

        self.assertEqual(Invite.objects.all().count(), 1)

    def test_creating_the_same_invite(self):
        with self.assertRaises(AlreadyExistsError):
            invite1 = Invite.objects.create_invite(self.user1, self.point)
            invite2 = Invite.objects.create_invite(self.user1, self.point)

    
