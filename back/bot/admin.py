from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Currency  # , CategoryIncome, Income


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
#
#
# @admin.register(CategoryIncome)
# class CategoryIncomeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'name']
#
#
# @admin.register(Income)
# class IncomeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'amount', 'currency', 'category', 'created_at']
