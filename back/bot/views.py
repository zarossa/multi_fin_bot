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


class AccountAPICreate(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        currency_code = self.request.data.get('currency_code')
        currency = get_object_or_404(Currency, code=currency_code)
        data = {'user': request.user.pk,
                'currency': currency.pk}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountAPIDestroy(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = self.queryset.get(pk=self.request.user.pk)
        return obj

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
