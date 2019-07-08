import logging
from constance import config


logger = logging.getLogger(__name__)


def saved(instance):
    return instance.pk is not None
