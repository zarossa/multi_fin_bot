from rest_framework import routers

from bot.views import AccountViewSet, AccountCurrencyViewSet, CategoryIncomeViewSet, IncomeViewSet, \
    CategoryExpenseViewSet, ExpenseViewSet


class AccountRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'delete': 'destroy',
                'post': 'create',
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        )
    ]


account = AccountRouter()
account.register(r'account', AccountViewSet, basename='account')

currency = routers.SimpleRouter()
currency.register(r'currency', AccountCurrencyViewSet, basename='currency')

category_income = routers.SimpleRouter()
category_income.register(r'category', CategoryIncomeViewSet, basename='category_income')

income = routers.SimpleRouter()
income.register(r'income', IncomeViewSet, basename='income')

category_expense = routers.SimpleRouter()
category_expense.register(r'category', CategoryExpenseViewSet, basename='category_expense')

expense = routers.SimpleRouter()
expense.register(r'expense', ExpenseViewSet, basename='expense')
