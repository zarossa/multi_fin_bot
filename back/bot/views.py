import random

from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import status, mixins
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseNotFound

from .serializers import UserSerializer  # , IncomeSerializer
from .models import User


class UserAPIGet(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class UserAPICreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class IncomeAPIList(generics.ListCreateAPIView):
#     queryset = Income.objects.all()
#     serializer_class = IncomeSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly, )
#
#
# class IncomeAPIUpdate(generics.UpdateAPIView):
#     queryset = Income.objects.all()
#     serializer_class = IncomeSerializer
#
#
# class IncomeAPIDestroy(generics.RetrieveDestroyAPIView):
#     queryset = Income.objects.all()
#     serializer_class = IncomeSerializer
#     permission_classes = (IsAdminUser, )
