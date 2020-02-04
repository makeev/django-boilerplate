import logging
import random
import sys
from io import BytesIO
from urllib.error import HTTPError
from urllib.parse import quote

import requests
from django.conf import settings
from django.core import management
from django.core.files import File
from django.core.management.base import BaseCommand

from main.models import User

logger = logging.getLogger(__name__)


def get_file(path=None, allow_download=False, file_type=None):
    """
    Create or download sample file, depends on allow_download
    """
    if file_type is None:
        file_type = 'image'

    if path and path[:4] == 'http' and allow_download:
        path = quote(path, safe=':/?*=\'')
        logger.debug('Loading: %s' % path)
        try:
            u = requests.get(path)
            f = BytesIO()
            f.write(u.content)
            return File(f)
        except HTTPError:
            logger.error('HTTPError for file: %s' % path)
            return File(BytesIO())

    # if file_type == 'image':
    #     image_file = generate_random_image(random.randint(200, 300), random.randint(300, 400))
    #     blob = BytesIO()
    #     image_file.save(blob, 'PNG')
    #     return File(blob)
    elif file_type == 'pdf':
        # @TODO any local dummy file instead
        path = 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'
        u = requests.get(path)
        f = BytesIO()
        f.write(u.content)
        return File(f)
    else:
        raise Exception('unknown file_type')


class Command(BaseCommand):
    help = 'Generate initial and test data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--allow-download', action='store_true', dest='allow_download', default=False,
            help='Download files and images from http sources',
        )

    def handle(self, allow_download, *args, **options):

        if not settings.DEBUG:
            logger.error('Can’t run generate in production mode')
            sys.exit(1)

        admin_email = 'admin@localhost'
        # create superuser
        if not User.objects.filter(email=admin_email).exists():
            u1 = User.objects.create_user(
                username=admin_email,
                email=admin_email,
                password='123',
                first_name='Admin',
                last_name='Adminovitch',
                is_superuser=True,
                is_staff=True,
                is_active=True,
                is_email_verified=True,
            )
            u1.save()

            logger.info('admin@localhost created')


        # management.call_command('loaddata', 'nutrions', format='json', verbosity=0)

        logger.info('All Done')
