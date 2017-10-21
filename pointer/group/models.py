from django.db import models
from users.models import User
from django.conf import settings

# Create your models here.

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class GroupsManager(models.Manager):
    def create_group(self, name, author, people):
        if not name:
            raise ValueError("Group has to have a name.")

        if author \
                in people:
            raise ValueError("You can't add yourself in group.")
        group = self.model(
            name=name,
            author=author
        )
        group.save()
        group.people = people
        # for p in people:
        #     group.add(p)
        group.save()
        return group

    def get_groups(self, user):
        return Group.objects.filter(author=user)


class Group(models.Model):
    name = models.CharField(max_length=40, blank=False)
    people = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name="members_of_group")
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="owner_of_group")

    objects = GroupsManager()

    def get_people_list(self):
        return self.people.all()

    def add(self, user):
        self.people.add(user)
    #add to point create group from pointer members
    #---          invite group

    def remove(self, user):
        self.people.remove(user)




