from django.contrib import admin

from .models import Word, User, Currency, CategoryIncome, Income


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['id', 'gender', 'word']
    list_editable = ['gender', 'word']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'name', 'preferred_currency']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']


@admin.register(CategoryIncome)
class CategoryIncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name']


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'currency', 'category', 'created_at']
