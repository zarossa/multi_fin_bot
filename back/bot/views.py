import random

from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseNotFound

from .serializers import IncomeSerializer, WordSerializer
from .models import Word, Income, User


class CreateIncome(APIView):
    serializer_class = IncomeSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class IncomeAPIView(ListAPIView):
#     queryset = Income.objects.all()
#     serializer_class = IncomeSerializer


class IncomeAPIView(APIView):
    def get(self, request):
        incomes = Income.objects.all().values()
        return Response({'incomes': list(incomes)})

    def post(self, request):
        income_new = Income.objects.create(
            user_id=request.data['user'],  # 1
            amount=request.data['amount'],  # 100
            currency_id=request.data['currency'],  # 1,
            category_id=request.data['category'],  # 1,
        )
        return Response({'income': model_to_dict(income_new)})


class RandomWord(APIView):
    @staticmethod
    def get(*args, **kwargs):
        all_words = Word.objects.all()
        random_word = random.choice(all_words)
        serialized_random_word = WordSerializer(random_word, many=False)
        return Response(serialized_random_word.data)


class NextWord(APIView):
    def get(self, request, pk, format=None):
        word = Word.objects.filter(pk__gt=pk).first()
        if word is None:
            return HttpResponseNotFound()
        serialized_word = WordSerializer(word, many=False)
        return Response(serialized_word.data)
