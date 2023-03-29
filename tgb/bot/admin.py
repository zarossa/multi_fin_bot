from django.contrib import admin

from .models import User, Currency


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'name', 'preferred_currency']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
