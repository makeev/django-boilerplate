import sys
import random
import logging
from datetime import timedelta

from io import BytesIO

from urllib.error import HTTPError
from urllib.parse import quote

import requests

from django.utils import timezone
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from main.models import User
from news.models import Post
from project.helpers.random_data import (
    generate_full_name,
    generate_random_blog_post,
    generate_random_email,
    generate_random_image,
    generate_username,
    get_random_date,
)

logger = logging.getLogger(__name__)


def get_file(path=None, allow_download=False, file_type=None):
    """
    Создает или скачивает файл для объекта модели,
    зависит от allow_download
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

    if file_type == 'image':
        image_file = generate_random_image(random.randint(200, 300), random.randint(300, 400))
        blob = BytesIO()
        image_file.save(blob, 'PNG')
        return File(blob)
    elif file_type == 'pdf':
        # @TODO можно заменить на какой-то локальный рандомный файл
        path = 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'
        u = requests.get(path)
        f = BytesIO()
        f.write(u.content)
        return File(f)
    else:
        raise Exception('unknown file_type')


class Command(BaseCommand):
    help = 'Создание тестовых данных в базе'

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
        # генерим админа
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

            logger.info('admin@online-logic.com created')

        # генерим еще каких-то рандомных пользователей
        for i in range(0, random.randint(15, 30)):
            full_name = generate_full_name()
            first_name, last_name = full_name.split(' ')
            username = generate_username(full_name)
            email = generate_random_email(username)

            u2 = User.objects.create_user(
                username=username,
                email=email,
                password='123',
                first_name=first_name,
                last_name=last_name,
                is_superuser=False,
                is_staff=True,
                is_active=True,
                is_email_verified=True,
            )
            u2.save()

            logger.info('%s created' % email)

        # генерим фейк ньюс
        users = User.objects.all()
        counter = 0
        now = timezone.now()
        for n in range(40):
            ru_data = generate_random_blog_post('ru_RU')
            en_data = generate_random_blog_post('en_US')
            post = Post(
                title_en=en_data['title'],
                title_ru=ru_data['title'],
                slug=en_data['slug'],
                annotation_en=en_data['annotation'],
                annotation_ru=ru_data['annotation'],
                content_en=en_data['text'],
                content_ru=ru_data['text']
            )
            post.user = random.choice(users)
            post.image.save('post_img.jpg', get_file(allow_download=allow_download))
            post.is_published = random.choice([True, False])
            if post.is_published:
                post.published_at = get_random_date(now - timedelta(days=30), now)
            post.save()
            counter += 1

        logger.info('%d posts created' % counter)
        logger.info('All Done')
