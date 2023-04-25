from rest_framework import serializers
from .models import User, Currency, Income, CategoryIncome, Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['pk', 'gender', 'word']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'telegram_id', 'name', 'preferred_currency')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('pk', 'code', 'name')


class CategoryIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryIncome
        fields = ('pk', 'user', 'name')


class IncomeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    currency = CurrencySerializer()
    category = CategoryIncomeSerializer()

    class Meta:
        model = Income
        fields = ('pk', 'user', 'amount', 'currency', 'category', 'created_at')
