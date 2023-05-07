from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Account, Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name = 'Account'
    verbose_name_plural = 'Accounts'


class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )


admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
