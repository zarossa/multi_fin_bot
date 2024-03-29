from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Account, Currency, CategoryIncome, Income, CategoryExpense, Expense, AccountCurrency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'rate']


@admin.register(AccountCurrency)
class AccountCurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'currency']


@admin.register(CategoryIncome)
class CategoryIncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name']


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'currency', 'category', 'converted_amount', 'created_at']


@admin.register(CategoryExpense)
class CategoryExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'currency', 'category', 'converted_amount', 'created_at']


class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name = 'Account'
    verbose_name_plural = 'Accounts'


class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )


admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
