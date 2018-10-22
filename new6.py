from django.shortcuts import render
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from .serializers import DweetSerializer
from .serializers import CommentSerializer


from .models import Dweet
from .models import DweetRelation
from .models import Comments
from .permissions import PostOwnDweet

from userprofile.models import UserProfile

# Create your views here.

class DweetViewSet(viewsets.ModelViewSet):
    """
    provides crude rest api calls for Dweet
    """
    
    authentication_classes = (TokenAuthentication, )
    permission_classes = (PostOwnDweet, IsAuthenticated, )

    serializer_class = DweetSerializer
    queryset = Dweet.objects.all().order_by('-id',)
    
    filter_backends = (filters.SearchFilter, )
    search_fields = ('dweet_text',)

    """
    provides crude rest api calls for Comments
    """
    def perform_create(self, serializer):            
        serializer.save()

class CommentViewSet(viewsets.ViewSet):
    """
    provides crude rest api calls for Comments
    """

    authentication_classes = (TokenAuthentication, )
    permission_classes = (PostOwnDweet, IsAuthenticated, )

    def list(slef, request):
        comments = Comments.objects.all()

        my_dweets = []
        for comment in comments:
            cmt = {}       
            cmt['id'] = comment.id
            cmt['username'] = comment.commented_user.username        
            cmt['comment'] = comment.comment 
            cmt['commented_at'] = comment.commented_at           
            
            my_dweets.append(cmt)

        return Response(my_dweets)

    def create(self, request):
        """
        Creates new dweet for the user
        """

        comment = request.data
        serializer = CommentSerializer(comment)

        if serializer.is_valid:     
             
            dweet_id = serializer.data.get('dweet_id')
            comment = serializer.data.get('comment')

            dweet_qs = Dweet.objects.all()
            dweet = get_object_or_404(dweet_qs, pk=dweet_id)
            #dweet = Dweet.objects.get(pk=dweet_id)
            comment = Comments.objects.create(comment = comment , commented_user = self.request.user)
            comment.dweet.add(dweet)
            comment.save()            

            cmt = {}
            cmt['id'] = comment.id
            cmt['username'] = comment.commented_user.username
            cmt['dweet'] = dweet.dweet_text            
            cmt['comment'] = comment.comment 
            cmt['commented_at'] = comment.commented_at

            return Response(cmt)
        else:
            return Response(serializer.errors, status = status.HTTP_BAD_REQUEST)

