from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from .serializers import DweetSerializer
from .serializers import ReactionSerializer
from .serializers import ReDweetSerializer


from .models import Dweet
from .models import DweetRelation
from .models import Comments
from .models import Reaction

from .permissions import PostOwnDweet
from .permissions import ReactOnDweet

from userprofile.models import UserProfile

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

# Create your views here.
class DweetViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given dweet

    list:
    Return a list of all dweets

    create:
    Create a new dweet
    """
    
    authentication_classes = (TokenAuthentication, )
    permission_classes = (PostOwnDweet, IsAuthenticated, )

    serializer_class = DweetSerializer
    
    filter_backends = (filters.SearchFilter, )
    search_fields = ('dweet_text',)

    def get_queryset(self):
        """
        Return Dweet QuerySet for filtering based on user id
        """

        queryset = Dweet.objects.select_related().all().order_by('-id',)
        uid = self.request.query_params.get('uid', None)

        if uid is not None:
            user = UserProfile.objects.only('id').filter(pk=uid)
            queryset = queryset.filter(dweeted_user__in=user)            

        return queryset    

    def perform_create(self, serializer):
        """
        Update requested user object to serializer user object
        """        

        serializer.save(user=self.request.user)

class ReDweetViewSet(viewsets.ModelViewSet):    
    """
    create:
    Create a redweet
    """

    http_method_names = ['post']

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, ReactOnDweet, )

    serializer_class = ReDweetSerializer
    queryset = DweetRelation.objects.all()

    def create(self, request):
        """
        Creates new dweet for the user
        """

        data = request.data
        serializer = ReDweetSerializer(data)

        user= request.user

        if serializer.is_valid:            
            dweet_id = serializer.data.get('dweet_id')            
            alldweets = Dweet.objects.only('id').select_related().all()
            dwt = get_object_or_404(alldweets, pk=dweet_id)
            DweetRelation.objects.create(dweet=dwt, user=user)
            return Response({'message':'Reweeted'})
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ReactionViewSet(viewsets.ViewSet):
    """
    create:
    Create a reaction to a given dweet
    """

    http_method_names = ['post']

    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    serializer_class = ReactionSerializer
    queryset = Reaction.objects.all()


    def create(self, request):
        """
        Creates new reaction for the user
        """

        reaction = request.data
        serializer = ReactionSerializer(reaction)

        user= request.user

        if serializer.is_valid:            
            dweet_id = serializer.data.get('dweet_id')
            reaction = serializer.data.get('reaction')
                        
            dweet_exists = Dweet.objects.filter(pk=dweet_id).exists()
            if dweet_exists:
                dweet = Dweet.objects.get(pk=dweet_id)
            else:
                return Response(status = status.HTTP_400_BAD_REQUEST)

            #already_reacted = dweet.reactions.filter(reaction=reaction, reacted_user=user).exists()

            dweet.reactions.create(reaction = reaction ,reacted_user = user )
            dweet.save()
            return Response({'message':'reacted'})
            """
            if already_reacted:
                
                #This not following api norm. But I felt appropirate to remove when request comes again.
                
                dweet.reactions.filter(reaction=reaction, reacted_user=user).delete()
                return Response({'message':'undoing reaction'})
            else:                
                dweet.reactions.create(reaction = reaction ,reacted_user = user )
                dweet.save()
                return Response({'message':'reacted'})
            """
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)