from django.contrib import admin
from django.urls import path, include, re_path

from bot.routers import category_income
from bot.views import AccountAPICreate, AccountAPIDestroy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', AccountAPICreate.as_view()),
    path('api/v1/user/delete/', AccountAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/', include(category_income.urls)),
]
