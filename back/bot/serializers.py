from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import Currency, Account, CategoryIncome, Income
from .scripts.currency_exchange import convert


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('user', 'currency', )


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField()

    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'password', 'first_name')


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('pk', 'code', 'name')


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
        amount_currency = data.get('currency').pk
        user_currency = self.context['request'].user.account.currency_id
        data['converted_amount'] = convert(data.get('amount'), user_currency, amount_currency)
        return data
