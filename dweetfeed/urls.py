from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

from .views import FeedAsService

router = DefaultRouter()

router.register('feed', FeedAsService, base_name="feed")

urlpatterns = [
    path('', include(router.urls)),
]

