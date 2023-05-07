from django.contrib import admin
from django.urls import path, include, re_path

from bot.views import AccountAPIUpdate

# from bot.views import UserAPICreate, UserAPIGet
# from rest_framework import routers


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', AccountAPICreate.as_view()),
    path('api/v1/user/delete/', AccountAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
