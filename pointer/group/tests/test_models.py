from django.test import TestCase

from group.models import Group
from users.models import User


class GroupTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', \
            password='testing123', email='testcase@gmail.com')
        self.user2 = User.objects.create_user(username='user2', \
            password='testing123', email='testcase2@gmail.com')
        self.user3 = User.objects.create_user(username='user3', \
                                              password='testing123', email='testcase3@gmail.com')

    def test_create_group(self):
        group = Group.objects.create_group(name="test group", author=self.user1,
                                           people=(self.user2, self.user3))
        self.assertEqual(Group.objects.all().count(), 1)
        self.assertEqual(len(group.get_people_list()), 2)
        self.assertFalse(self.user1 in group.get_people_list())
        self.assertTrue(self.user2 in group.get_people_list())
        self.assertTrue(self.user3 in group.get_people_list())


    def test_adding_person(self):
        group = Group.objects.create_group(name="test group", author=self.user1,
                                           people=(self.user2,))
        group.add(user=self.user3)
        self.assertEqual(len(group.get_people_list()), 2)
        self.assertFalse(self.user1 in group.get_people_list())
        self.assertTrue(self.user2 in group.get_people_list())
        self.assertTrue(self.user3 in group.get_people_list())

    def test_removing_person(self):
        group = Group.objects.create_group(name="test group", author=self.user1,
                                           people=(self.user2, self.user3))
        group.remove(self.user3)
        self.assertEqual(len(group.get_people_list()), 1)
        self.assertFalse(self.user1 in group.get_people_list())
        self.assertTrue(self.user2 in group.get_people_list())
        self.assertFalse(self.user3 in group.get_people_list())

    def test_get_groups(self):
        group1 = Group.objects.create_group(name="test group1", author=self.user1,
                                           people=(self.user2,))
        group2 = Group.objects.create_group(name="test group1", author=self.user1,
                                            people=(self.user3,))
        self.assertEqual(Group.objects.all().count(), 2)
        groups = Group.objects.get_groups(user=self.user1)
        self.assertEqual(len(groups), 2)
        self.assertTrue(group1 in groups)
        self.assertTrue(group2 in groups)

