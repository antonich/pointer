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
            people.remove(author)

        group = self.model(
            name=name,
            author=author
        )
        group.save()
        for p in people:
            group.add(p)
        group.save()
        return group

    def create_group_from_pointer(self, name, author, pointer):
        from members.models import Member
        people = [member.user for member in Member.objects.going_members(pointer=pointer)]
        return self.create_group(name=name, author=author, people=people)

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
