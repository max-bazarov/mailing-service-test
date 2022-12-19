from django.contrib import admin

from .models import Mailing, Message


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'start_at', 'end_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'client', 'sent_at', 'status')
