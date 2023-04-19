import random

from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseNotFound

from .models import Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['pk', 'gender', 'word']


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
