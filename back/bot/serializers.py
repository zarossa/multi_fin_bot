from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import Currency, Account, CategoryIncome, Income, CategoryExpense, Expense, AccountCurrency
from .scripts.currency_exchange import convert


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('user', 'currency', 'amount')
        read_only_fields = ('amount',)


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField()

    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'password', 'first_name')


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('pk', 'code', 'name', 'rate')


class AccountCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountCurrency
        fields = ('pk', 'currency')


class AccountCurrencyFullSerializer(serializers.ModelSerializer):
    currency_pk = serializers.IntegerField(source='currency.pk')
    code = serializers.CharField(source='currency.code')
    name = serializers.CharField(source='currency.name')
    rate = serializers.DecimalField(source='currency.rate', max_digits=20, decimal_places=10)

    class Meta:
        model = AccountCurrency
        fields = ('pk', 'currency_pk', 'code', 'name', 'rate')


class CategoryIncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryIncome
        fields = ('pk', 'name')


class IncomeSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryIncome.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['category'].queryset = CategoryIncome.objects.filter(user=user)

    class Meta:
        model = Income
        fields = ('pk', 'amount', 'currency', 'category', 'converted_amount', 'created_at')
        read_only_fields = ('converted_amount',)

    def validate(self, data):
        amount_currency = data.get('currency').rate
        user_currency = self.context['request'].user.account.currency.rate
        data['converted_amount'] = convert(data.get('amount'), user_currency, amount_currency)
        return data


class CategoryExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryExpense
        fields = ('pk', 'name')


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryExpense.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['category'].queryset = CategoryExpense.objects.filter(user=user)

    class Meta:
        model = Expense
        fields = ('pk', 'amount', 'currency', 'category', 'converted_amount', 'created_at')
        read_only_fields = ('converted_amount',)

    def validate(self, data):
        amount_currency = data.get('currency').rate
        user_currency = self.context['request'].user.account.currency.rate
        data['converted_amount'] = convert(data.get('amount'), user_currency, amount_currency)
        return data
