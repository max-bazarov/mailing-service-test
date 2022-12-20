from django.db import models

MESSAGE_PREVIEW = 10


class Mailing(models.Model):
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    message = models.TextField()
    filter = models.ForeignKey(
        'users.Filter',
        related_name='mailings',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'mailing'

    def __str__(self):
        return (f'{self.message[:MESSAGE_PREVIEW]} '
                f'{self.start_at}-{self.end_at}')


class Message(models.Model):
    class Status(models.TextChoices):
        NOT_SENT = 'not_sent'
        SENT = 'sent'
        FAILED = 'failed'

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    client = models.ForeignKey(
        'users.Client',
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
        return f'{self.mailing} {self.client} {self.status}'
