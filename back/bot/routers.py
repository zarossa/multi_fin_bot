from rest_framework import routers

from bot.views import CategoryIncomeViewSet, IncomeViewSet

category_income = routers.SimpleRouter()
category_income.register(r'category_income', CategoryIncomeViewSet, basename='category_income')

income = routers.SimpleRouter()
income.register(r'income', IncomeViewSet, basename='income')
