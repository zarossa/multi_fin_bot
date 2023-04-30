import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

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


# class IncomeModel:
#     def __init__(self, amount: float):
#         self.amount = amount
#         self.user = 1
#         self.currency = 1
#         self.category = 1


class IncomeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    amount = serializers.FloatField()
    currency_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)



# def encode():
#     model = IncomeModel(250)
#     model_sr = IncomeSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"amount":250.0,"user":1,"currency":1,"category":1}')
#     data = JSONParser().parse(stream)
#     serializer = IncomeSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)

# class IncomeSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     currency = CurrencySerializer()
#     category = CategoryIncomeSerializer()
#
#     class Meta:
#         model = Income
#         fields = ('pk', 'user', 'amount', 'currency', 'category', 'created_at')
