from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from timezone_field import TimeZoneField

from core.utils import parse_operator_code
from core.validators import validate_phone_number


class Filter(models.Model):
    tag = models.ForeignKey(
        'users.Tag',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Tag')
    )
    operator_code = models.ForeignKey(
        'users.OperatorCode',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Operator code')
    )

    class Meta:
        db_table = 'filter'

    def __str__(self):
        return f'{self.tag} {self.operator_code}'


class Tag(models.Model):
    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name


class OperatorCode(models.Model):
    code = models.CharField(_('Code'), max_length=10)

    class Meta:
        db_table = 'operator_code'

    def __str__(self):
        return f'{self.code}'


class ClientManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given phone number and password.
        Parses operator code from phone number.
        """
        if not phone_number:
            raise ValueError('The given phone number must be set')
        operator_code = parse_operator_code(phone_number)
        current_operator_code, _ = OperatorCode.objects.get_or_create(
            code=operator_code
        )
        user = self.model(
            phone_number=phone_number,
            operator_code=current_operator_code,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        """
        Creates and saves a superuser with the given phone number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone_number, password, **extra_fields)


class Client(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_phone_number],
    )
    operator_code = models.ForeignKey(
        OperatorCode,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    time_zone = TimeZoneField(
        default='Europe/Moscow',
        use_pytz=True,
        blank=True
    )
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = ClientManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.phone_number
