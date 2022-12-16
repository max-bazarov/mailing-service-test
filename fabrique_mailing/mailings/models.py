from django.db import models


MESSAGE_PREVIEW = 10


class Mailing(models.Model):
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField()
    message = models.TextField()
    tags = models.ManyToManyField(
        'users.Tag',
        related_name='mailings',
        through='mailings.MailingTag'
    )

    class Meta:
        db_table = 'mailing'

    def __str__(self):
        return (f'{self.message[:MESSAGE_PREVIEW]}'
                ' {self.start_at}-{self.end_at}')


class MailingTag(models.Model):
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        'users.Tag',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'mailing_tag'

    def __str__(self):
        return f'{self.mailing} {self.tag}'


class Message(models.Model):
    class Status(models.TextChoices):
        NOT_SENT = 'not_sent'
        SENT = 'sent'
        DELIVERED = 'delivered'
        FAILED = 'failed'

    mailing = models.OneToOneField(
        Mailing,
        on_delete=models.CASCADE,
        related_name='message'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sent_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(
        max_length=255,
        choices=Status.choices,
        default=Status.NOT_SENT
    )

    class Meta:
        db_table = 'message'

    def __str__(self):
        return f'{self.text[:MESSAGE_PREVIEW]}'
