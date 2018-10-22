from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

from .views import LoginService

router = DefaultRouter()

router.register('login',LoginService, base_name="login")

urlpatterns = [
    path('', include(router.urls)),
]

