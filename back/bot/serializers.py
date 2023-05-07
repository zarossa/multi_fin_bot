from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import Currency, Account


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
#
#
# class CategoryIncomeSerializer(serializers.ModelSerializer):
#     # user = UserSerializer()
#
#     class Meta:
#         model = CategoryIncome
#         fields = '__all__'
#
#
# class IncomeSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=CurrentUser())
#     category = serializers.PrimaryKeyRelatedField(queryset=CategoryIncome.objects.filter(user=User().get_user()))
#
#     # currency = CurrencySerializer()
#     # category = CategoryIncomeSerializer()
#
#     class Meta:
#         model = Income
#         fields = ('pk', 'user', 'amount', 'currency', 'category', 'created_at')
