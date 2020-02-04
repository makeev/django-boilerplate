import uuid
import hashlib
import logging
from pytz import utc
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from timezone_field import TimeZoneField


logger = logging.getLogger(__name__)


def uuid4_hex():
    """
    UUID for username field can be useful is some case when we wont show real id or email
    """
    return uuid.uuid4().hex


class GroupExtras(models.Model):
    group = models.OneToOneField(Group, unique=True, related_name='extras', on_delete=CASCADE)
    # extra fields for groups will be here
    # ...

    def __str__(self):
        return self.group.name


class UserModelManager(UserManager):
    """
    Case unsensetive search for username and email
    """
    def filter(self, **kwargs):
        if 'username' in kwargs:
            kwargs['username__iexact'] = kwargs['username']
            del kwargs['username']
        if 'email' in kwargs:
            kwargs['email__iexact'] = kwargs['email']
            del kwargs['email']
        return super(UserModelManager, self).filter(**kwargs)

    def get(self, **kwargs):
        if 'username' in kwargs:
            kwargs['username__iexact'] = kwargs['username']
            del kwargs['username']
        if 'email' in kwargs:
            kwargs['email__iexact'] = kwargs['email']
            del kwargs['email']
        return super(UserModelManager, self).get(**kwargs)

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=False,
        blank=False,
        default=uuid4_hex,
        help_text=_('Required.'),
        error_messages={
            'unique': _("A user with that UID already exists."),
        }
    )
    password_changed_at = models.DateTimeField(null=True, blank=True)
    timezone = TimeZoneField(default='UTC')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserModelManager()

    def __str__(self):
        return self.email

    def get_signed_hash(self):
        signed_str = '%d_%s' % (self.id, hashlib.md5(settings.SECRET_KEY.encode('utf-8')).hexdigest())
        return hashlib.sha256(signed_str.encode('utf-8')).hexdigest()[:16]

    def set_password(self, *args, **kwargs):
        """
        Password change datetime
        """
        super().set_password(*args, **kwargs)
        self.password_changed_at = datetime.now().astimezone(utc)

    class Meta:
        permissions = (
            # some custom permissions for user
            ("can_view_dashboard", "Can view dashboard"),
        )
