from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Filter, OperatorCode, Tag

Client = get_user_model()


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone_number',
        'operator_code',
        'tag',
        'time_zone',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(OperatorCode)
class OperatorCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', )


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'operator_code',)
