from django.dispatch import receiver
from django.db.models.signals import post_save

from point.models import Pointer
from members.models import Member
from members.choices import *
from invite.models import Invite

@receiver(post_save, sender=Pointer, dispatch_uid="pointer_postsave")
def create_author_member_and_group(sender, **kwargs):
    inst = kwargs['instance']
    Member.objects.create_member(user=inst.author, pointer=inst, status=GOING)


@receiver(post_save, sender=Invite, dispatch_uid="invite_postsave")
def create_member_when_invitation_is_sent(sender, **kwargs):
    inst = kwargs['instance']
    Member.objects.create_member(user=inst.to_user, pointer=inst.pointer, status=WAITING)
