import os
import tarfile
from django.conf import settings
from django.db import connection
from django.core import management
from django.core.management.color import no_style
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    TMP_DUMP_PATH = 'dumpall.tmp.json'

    help = 'Bkup tool (db+media)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format', default='json', dest='format',
            help='Specifies the output serialization format for fixtures.',
        )
        parser.add_argument(
            '--indent', default=None, dest='indent', type=int,
            help='Specifies the indent level to use when pretty-printing output.',
        )
        parser.add_argument(
            '-e', '--exclude', dest='exclude', action='append', default=[],
            help='An app_label or app_label.ModelName to exclude '
                 '(use multiple --exclude to exclude multiple apps/models).',
        )
        parser.add_argument(
            '--maxsize',
            action='store',
            dest='maxsize',
            type=int,
            default=5,
            help='Max size for files from media (Mb), default 5'
        )
        parser.add_argument(
            '-ed', '--exclude-dir', dest='exclude_dir', action='append', default=[],
            help='Exlude dir from MEDIA_ROOT (cache, thumbs, tmp)',
        )
        parser.add_argument(
            '-f', '--file-name', default='dump.tar.gz', dest='file_name',
            help='Specifies the archive name',
        )

    def handle(self, *args, **options):
        dump_archive_name = options.get('file_name')
        dump_options = {
            'all': True,
            'natural_foreign': True,
            'natural_primary': True,
            'indent': options.get('indent'),
            'verbosity': options.get('verbosity', 0),
            'exclude': options.get('exclude'),
            'output': self.TMP_DUMP_PATH,
        }

        self.stdout.write('dumping database data')
        management.call_command("dumpdata", **dump_options)
        self.stdout.write('Done!')

        cmd_args = [
            str(settings.MEDIA_ROOT),
        ]

        if options.get('exclude_dir'):
            exclude_args = []
            for d in options.get('exclude_dir'):
                d = '%s/%s' % (settings.MEDIA_ROOT, d.strip('/'))
                exclude_args.append('-path %s' % d)

            cmd_args.append('-type d \( %s \) -prune' % ' -o '.join(exclude_args))
            cmd_args.append('-o -type f -size -%dM -print' % options.get('maxsize'))
        else:
            cmd_args.append('-type f -size -%dM -print' % options.get('maxsize'))

        # find files
        cmd = 'find %s' % ' '.join(cmd_args)

        with tarfile.open(dump_archive_name, 'w:gz') as tar:
            tar.add(self.TMP_DUMP_PATH)
            os.remove(self.TMP_DUMP_PATH)
            for l in os.popen(cmd).read().split('\n'):
                if not l:
                    continue
                filepath = l.replace(settings.MEDIA_ROOT, 'media')
                tar.add(l, arcname=filepath)

        self.stdout.write('Done! %s created' % dump_archive_name)
