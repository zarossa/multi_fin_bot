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
        incomes = Income.objects.all()
        return Response({'incomes': IncomeSerializer(incomes, many=True).data})

    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is None:
            return Response({'error': 'Method PUT not allowed'})
        try:
            instance = Income.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exists'})

        serializer = IncomeSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is None:
            return Response({'error': 'Method DELETE not allowed'})
        try:
            Income.objects.get(pk=pk).delete()
        except:
            return Response({'error': 'Object does not exists'})

        return Response({'post': f'delete post {pk}'})


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
