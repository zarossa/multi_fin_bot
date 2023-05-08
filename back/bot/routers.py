from rest_framework import routers

from bot.views import CategoryIncomeViewSet

category_income = routers.SimpleRouter()
category_income.register(r'category_income', CategoryIncomeViewSet, basename='category_income')
