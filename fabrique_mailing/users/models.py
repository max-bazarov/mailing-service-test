from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name


class UserTag(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    tag = models.ForeignKey('users.Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_tag'

    def __str__(self):
        return f'{self.user} {self.tag}'


class User(AbstractUser):
    phone_number = PhoneNumberField(blank=True)
    operator_code = models.CharField(max_length=10, blank=True)
    tags = models.ManyToManyField(
        'users.Tag',
        blank=True,
        through='users.UserTag'
    )
    time_zone = models.CharField(max_length=255, blank=True)
