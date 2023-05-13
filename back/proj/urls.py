from django.contrib import admin
from django.urls import path, include, re_path

from bot.routers import category_income, income, category_expense, expense, account, currency
from bot.views import CurrencyAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/income/', include(category_income.urls)),
    path('api/v1/', include(income.urls)),
    path('api/v1/expense/', include(category_expense.urls)),
    path('api/v1/', include(expense.urls)),
    path('api/v1/', include(account.urls)),
    path('api/v1/currency/all/', CurrencyAPI.as_view()),
    path('api/v1/', include(currency.urls)),
]
