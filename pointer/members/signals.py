from django.dispatch import receiver
from django.db.models.signals import post_save

from point.models import Pointer
from members.models import Member


@receiver(post_save, sender=Pointer, dispatch_uid="pointer_postsave")
def create_author_member_and_group(sender, **kwargs):
    inst = kwargs['instance']
    Member.objects.create_member(user=inst.author, pointer=inst)
