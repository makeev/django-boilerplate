import logging
from django.dispatch import receiver
from django.db.models.signals import pre_save
from main.models import User


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=User)
def username_fix(sender, instance, **kwargs):
    """
    Фикс на всякий случай для совместимости со всякими 3rd party штуками
    по умолчанию используем email для логина и всего остального
    """
    # email всегда равен username, чтобы не сломалась обратная совместимость
    # при создании из админки наоборот надо email = username
    if instance.username and not instance.email:
        instance.email = instance.username
    else:
        instance.username = instance.email
