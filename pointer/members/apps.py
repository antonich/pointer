from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

class MembersConfig(AppConfig):
    name = 'members'
    verbose_name = _('Members')

    def ready(self):
        from members import signals
