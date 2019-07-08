import os
import sys
import logging
import tarfile
from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    TMP_DUMP_PATH = 'dumpall.tmp.json'

    help = 'Load dump from make_dump command'

    def add_arguments(self, parser):
        parser.add_argument('file', help='tar.gz file to open')
        parser.add_argument(
            '--without-media', action='store_true', dest='without_media',
            help='Do not import media files',
        )
        parser.add_argument(
            '--without-data', action='store_true', dest='without_data',
            help='Do not import database data',
        )

    def handle(self, *args, **options):

        if not settings.DEBUG:
            logger.error('Can’t run generate in production mode')
            sys.exit(1)

        f = options.get('file')
        without_media = options.get('without_media')
        without_data = options.get('without_data')

        if without_media and without_data:
            self.stderr.write('nothing to do')
            return

        with tarfile.open(f, 'r') as tar:
            if not without_data:
                self.stdout.write('Loading data')
                if os.path.exists(self.TMP_DUMP_PATH):
                    os.remove(self.TMP_DUMP_PATH)
                tar.extract(tar.getmember(self.TMP_DUMP_PATH))

                management.call_command(
                    "loaddata", self.TMP_DUMP_PATH, format='json',
                    verbosity=options.get('verbosity')
                )
                os.remove(self.TMP_DUMP_PATH)
                self.stdout.write('Done!')

            if not without_media:
                self.stdout.write('Extracting media')

                tar.extractall(settings.MEDIA_ROOT+'/..', members=self.media_files(tar))

                self.stdout.write('Done!')

    def media_files(self, members):
        for tarinfo in members:
            if tarinfo.name.startswith('media/'):
                yield tarinfo
