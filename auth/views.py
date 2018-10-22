"""
Provides token based authentication service
"""

from rest_framework import viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Create your views here.
class LoginService(viewsets.ViewSet):
    """
    performs user authentication
    """

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """
        Create request's 'Authorization: Token' and other user details  
        and sends reponse as JSON      

        It sets cookie for client future request
        
        ex: Token 401f7ac837da42b97f613d789819ff93537bee6a        
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)
        
        response = Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                })

        response.set_cookie('authtoken', token.key)
        response.set_cookie('authuser_id', user.pk)
        response.set_cookie('authemail', user.email)
        response.set_cookie('authuname', user.username)

        return response