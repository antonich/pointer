from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class PointConfig(AppConfig):
    name = 'point'
    verbose_name = _('Pointer')

    def ready(self):
        import point.signals
