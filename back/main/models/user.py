import uuid
import hashlib
import string
import logging
from pytz import utc
from datetime import datetime
from base64 import b32encode
from binascii import unhexlify
from pyotp import TOTP
from pyotp.utils import strings_equal
from secrets import choice, token_hex
from urllib.parse import quote, urlencode
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from timezone_field import TimeZoneField


logger = logging.getLogger(__name__)


def uuid4_hex():
    return uuid.uuid4().hex


class GroupExtras(models.Model):
    group = models.OneToOneField(Group, unique=True, related_name='extras', on_delete=CASCADE)
    # тут список дополнительных полей для групп
    # ...

    def __str__(self):
        return self.group.name


class UserModelManager(UserManager):
    """
    Регистронезависимый поиск и валидация юзера (username и email)
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

    @property
    def otp_device(self):
        """
        Возвращает валидный OTP-девайс пользователя
        """
        try:
            return OTPDevice.objects.get(user_id=self.pk, is_active=True, is_confirmed=True)
        except OTPDevice.DoesNotExist:
            return None

    @property
    def otp_enabled_at(self):
        otp_device = self.otp_device
        if otp_device:
            return otp_device.created_at
        else:
            return None

    def set_password(self, *args, **kwargs):
        """
        Фиксация момента смены пароля.
        """
        super().set_password(*args, **kwargs)
        self.password_changed_at = datetime.now().astimezone(utc)

    class Meta:
        permissions = (
            # всякие кастомные права
            ("can_view_dashboard", "Can view dashboard"),
        )


def default_key():
    return token_hex(20)


def key_validator(value):
    return hex_validator()(value)


def hex_validator(length=0):
    """
    Returns a function to be used as a model validator for a hex-encoded CharField.
    """
    def _validator(value):
        try:
            if isinstance(value, str):
                value = value.encode()

            unhexlify(value)
        except Exception:
            raise ValidationError('{0} is not valid hex-encoded data.'.format(value))

        if (length > 0) and (len(value) != length * 2):
            raise ValidationError('{0} does not represent exactly {1} bytes.'.format(value, length))

    return _validator


class OTPDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='otp_devices')
    name = models.CharField(max_length=100, default='device')
    created_at = models.DateTimeField(auto_now_add=True)
    secret = models.CharField(max_length=100, default=default_key, validators=[key_validator])  # зашифровать SECRET_KEY
    is_confirmed = models.BooleanField(default=False, help_text='Is this device ready for use?')
    is_active = models.BooleanField(default=True, help_text='Is this device active?')  # всё, что не было удалено

    @property
    def enabled(self):
        return self.is_confirmed and self.is_active

    @property
    def config_url(self):
        """
        A URL for configuring Google Authenticator or similar.

        See https://github.com/google/google-authenticator/wiki/Key-Uri-Format.
        The issuer is taken from :setting:`OTP_TOTP_ISSUER`, if available.

        The secret parameter is an arbitrary key value encoded in Base32 according to RFC 3548.
        The padding specified in RFC 3548 section 2.2 is not required and should be omitted.
        """
        label = str(self.user)
        params = {
            'secret': self.encoded_secret,
            'algorithm': 'SHA1',
            'digits': 6,
            'period': 30,
        }

        issuer = getattr(settings, 'OTP_TOTP_ISSUER', None)
        if isinstance(issuer, str) and (issuer != ''):
            issuer = issuer.replace(':', '')
            params['issuer'] = issuer
            label = '{}: {}'.format(issuer, label)

        url = 'otpauth://totp/{}?{}'.format(quote(label), urlencode(params))

        return url

    @property
    def encoded_secret(self):
        return b32encode(unhexlify(self.secret))

    def validate_token(self, token):
        totp = TOTP(self.encoded_secret)
        return totp.verify(token, valid_window=1)

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['-id']


class OTPStaticCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='otp_static_codes')
    created_at = models.DateTimeField(auto_now_add=True)
    code_hash = models.CharField(max_length=100)
    used_code = models.CharField(max_length=10, help_text='Shows only used code', null=True, default=None)
    used_at = models.DateTimeField(null=True, default=None)
    is_active = models.BooleanField(default=True)  # всё, что не было удалено

    @staticmethod
    def code_to_hash(code):
        to_hash = '%s_%s_%s' % (settings.SECRET_KEY, code, settings.OTP_SECRET)
        return hashlib.sha256(to_hash.encode('utf8')).hexdigest()

    def check_reserve_code(self, reserve_code):
        reserve_code = str(reserve_code).lower()
        testing_code_hash = self.code_to_hash(reserve_code)
        if len(reserve_code) == 10 and testing_code_hash and len(testing_code_hash) > 10:
            return strings_equal(testing_code_hash, self.code_hash)
        return False

    def generate_code(self):
        alphabet = string.ascii_lowercase + string.digits
        code = ''.join(choice(alphabet) for i in range(10))
        self.code_hash = self.code_to_hash(code)
        return code

    @classmethod
    def use_reserve_code(cls, user, reserve_code):
        """
        Проверяет валидность резервного кода.
        Если валидный — отмечает момент использования и возвращает True.
        """
        codes = cls.objects.filter(user=user, is_active=True, used_at__isnull=True).order_by('id')
        for code in codes:
            if code.check_reserve_code(reserve_code):
                reserve_code = str(reserve_code).lower()
                code.used_at = datetime.utcnow().replace(tzinfo=utc)
                code.used_code = reserve_code
                code.save()

                return True
        return False

    @classmethod
    def cnt_recovery_codes(cls, user):
        return cls.objects.filter(user=user, is_active=True, used_at__isnull=True).count()

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['-id']
