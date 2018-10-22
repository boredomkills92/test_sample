from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

from .views import DweetViewSet
from .views import ReactionViewSet
from .views import ReDweetViewSet

router = DefaultRouter()

router.register('dweet',DweetViewSet, base_name="dweet")
router.register('react', ReactionViewSet,  base_name="react" )
router.register('redweet', ReDweetViewSet,  base_name="redweet" )

urlpatterns = [
    path('', include(router.urls)),
]

