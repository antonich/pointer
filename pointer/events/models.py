from django.db import models
from django.conf import settings
from friends.models import Friendship
import datetime

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class PointerManager(models.Manager):
    def create_pointer(self, creator, name, date, description, is_private, invited_people=None):
        if date < datetime.datetime.now():
            raise ValueError

        pointer = self.create(
            name=name,
            date=date,
            description=description,
            is_private=is_private
        )
        #creates admin
        Member.objects.create_member(user=creator, pointer=pointer, is_accepted=True, is_admin=True)
        if is_private:#inviting another people
            if invited_people:
                for user in invited_people:
                    Member.objects.create_member(user=user, pointer=pointer, is_accepted=False, is_admin=False)
        pointer.save(using=self._db)
        return pointer

    def get_planned_pointerslist(self, member):
        """returns list of planned public pointers"""
        pointers = list()
        for i in Member.objects.filter(user=member):
            if not i.pointer.is_private:
                pointers.append(i.pointer)
        return pointers

    def get_suggested_pointerlist(self, user):
        """returns all public pointers that friends are going to visit"""
        friendslist = Friendship.objects.friends_list(user)
        pointers = list()
        for user in friendslist:# for each friend
            user_pointers = Pointer.objects.get_planned_pointerslist(user)# getting its pointers
            for friends_pointer in user_pointers:# for each friend's pointer
                found_flag = False
                for el in pointers:#try to add it to suggested list but check if it is already there
                    if el["pointer"].id == friends_pointer.id:
                        el["count"] = el["count"]+1
                        found_flag = True#don't have to add it to list
                        break
                if not found_flag:#if we didn't found it we add it to list
                    pointers.append({"pointer": friends_pointer, "count": 1})
        #now we have list of pointers
        sorted_pointers = sorted(pointers, key=lambda k: k['count'])
        return sorted_pointers

class Pointer(models.Model):
    """Model to represent events"""
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.CharField(max_length=500)
    is_private = models.BooleanField(default=False)
    objects = PointerManager()

class MembersManager(models.Manager):
    def create_member(self, user, pointer, is_accepted, is_admin=False):
        """invite someone"""
        if user in Member.objects.get_memberslist(pointer=pointer):
            raise ValueError("User is already invited.")
        member = self.create(
            user=user,
            pointer=pointer,
            is_accepted=is_accepted,
            is_admin=is_admin
        )
        member.save(using=self._db)
        return member

    def get_memberslist(self, pointer):
        """returns memberlist for certain pointer"""
        return [i.user for i in Member.objects.filter(pointer=pointer)]


class Member(models.Model):
    """Model to represent a member of event"""
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='member'
    )

    pointer = models.ForeignKey(
        Pointer,
        related_name='event'
    )
    is_accepted = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = MembersManager()

    def accept_membership(self):
        self.is_accepted = True




