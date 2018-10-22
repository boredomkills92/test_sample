"""
This class provide readonly api for feed for users
"""
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from dweetfeed.dweets.serializers import DweetSerializer

from dweetfeed.dweets.models import Dweet

from .permissions import OnlySafeMethods
from userprofile.models import UserProfile

class FeedAsService(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List:
    Return Feed only for loggedin user.

    """
    
    authentication_classes = (TokenAuthentication, )
    permission_classes = (OnlySafeMethods, IsAuthenticated, )       

    serializer_class = DweetSerializer    

    def get_queryset(self):
        """
        Return QuerySet for current user following Dweets
        """        
        following = self.request.user.following.all()
        return Dweet.objects.filter(dweeted_user__in = following).order_by('-id',)  