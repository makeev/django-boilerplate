import logging
from django.dispatch import receiver
from django.db.models.signals import pre_save
from main.models import User


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=User)
def username_fix(sender, instance, **kwargs):
    """
    Fix for 3rd party packages
    username = email for our custom model
    """
    if instance.username and not instance.email:
        instance.email = instance.username
    else:
        instance.username = instance.email
