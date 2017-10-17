from django.db import models
from django.conf import settings
from django.utils import timezone

from users.models import User


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

EMPTY_FIELD = "This field cant be empty."
ALREADY_EXISTS_ERROR = "Already exists with the same value."

class PointerManager(models.Manager):
    def create_pointer(self, author=None, title='', desc='', dcreated=timezone.now, pdate=timezone.now):
        if not title or not author or not desc:
            raise ValueError(EMPTY_FIELD)

        if title in Pointer.objects.filter(author=author).values_list('title', flat=True):
            raise ValueError(ALREADY_EXISTS_ERROR)

        pointer = self.model(
            title=title,
            description=desc,
            author=author
        )

        pointer.save()

        return pointer

class Pointer(models.Model):
    title = models.CharField(max_length=40, blank=True, default='')
    description = models.CharField(max_length=100, blank=True, default='')
    author = models.ForeignKey(
        AUTH_USER_MODEL
    )
    date_created = models.DateTimeField(default=timezone.now)
    pointer_date = models.DateTimeField(default=timezone.now)
    # is_active =

    REQUIRED_FIELDS = ['title', 'author', 'date_created', 'pointer_date']

    objects = PointerManager()

    class Meta:
        ordering = ['pointer_date']

    def __unicode__(self):
        return "Pointer %s" % (self.title)
