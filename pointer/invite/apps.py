from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

class InviteConfig(AppConfig):
    name = 'invite'
    verbose_name = _('Invitation')

    def ready(self):
        from members import signals
