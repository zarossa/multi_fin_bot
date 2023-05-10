from rest_framework import routers

from bot.views import CategoryIncomeViewSet, IncomeViewSet, CategoryExpenseViewSet, ExpenseViewSet

category_income = routers.SimpleRouter()
category_income.register(r'category_income', CategoryIncomeViewSet, basename='category_income')

income = routers.SimpleRouter()
income.register(r'income', IncomeViewSet, basename='income')

category_expense = routers.SimpleRouter()
category_expense.register(r'category_expense', CategoryExpenseViewSet, basename='category_expense')

expense = routers.SimpleRouter()
expense.register(r'expense', ExpenseViewSet, basename='expense')
