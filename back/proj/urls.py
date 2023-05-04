from django.contrib import admin
from django.urls import path, include, re_path

from bot.views import AccountAPIUpdate

# from bot.views import UserAPICreate, UserAPIGet
# from rest_framework import routers


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', AccountAPIUpdate.as_view()),
    # path('api/v1/user/', UserAPICreate.as_view()),
    # path('api/v1/income/', IncomeAPIList.as_view()),
    # path('api/v1/income/<int:pk>/', IncomeAPIUpdate.as_view()),
    # path('api/v1/income_delete/<int:pk>/', IncomeAPIDestroy.as_view()),
    # path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
