from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Account, Currency, AccountCurrency, CategoryIncome, Income, CategoryExpense, Expense
from .serializers import AccountSerializer, AccountCurrencySerializer, CategoryIncomeSerializer, IncomeSerializer, \
    CategoryExpenseSerializer, ExpenseSerializer, CurrencySerializer


class AuthViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BaseViewSet(AuthViewSet,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin):
    pass


class TransactionViewSet(BaseViewSet):
    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        transact = serializer.save(user=user)

        account = user.account
        account.amount += self.get_amount_change(transact)
        account.save()

    def get_amount_change(self, transact):
        raise NotImplementedError("Subclasses must implement this method")


class AccountViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     AuthViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_object(self):
        return get_object_or_404(self.get_queryset())

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        currency = request.data.get('currency')
        data = {'user': request.user.pk,
                'currency': currency}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = request.user
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrencyAPI(APIView):
    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)


class AccountCurrencyViewSet(BaseViewSet):
    queryset = AccountCurrency.objects.all()
    serializer_class = AccountCurrencySerializer


class CategoryIncomeViewSet(BaseViewSet):
    queryset = CategoryIncome.objects.all()
    serializer_class = CategoryIncomeSerializer


class IncomeViewSet(TransactionViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def get_amount_change(self, income):
        return income.converted_amount


class CategoryExpenseViewSet(BaseViewSet):
    queryset = CategoryExpense.objects.all()
    serializer_class = CategoryExpenseSerializer


class ExpenseViewSet(TransactionViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_amount_change(self, expense):
        return -expense.converted_amount
