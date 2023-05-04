import random

from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from rest_framework import status, mixins
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseNotFound

from .models import Account, get_or_none, Currency
from .serializers import AccountSerializer


class AccountAPIUpdate(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        account, _ = Account.objects.get_or_create(user=user)
        currency_code = self.request.data.get('currency_code')
        account.currency = get_object_or_404(Currency, code=currency_code)
        return account

# class UserAPIGet(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'username'
#
#
# class UserAPICreate(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
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
