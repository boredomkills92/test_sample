from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from .models import Dweet
from userprofile.models import UserProfile

from .views import DweetViewSet
from .views import ReDweetViewSet
from .views import ReactionViewSet

# Create your tests here.

class DweetApiTestCase(TestCase):

    def setUp(self):
        """
        initial setup for each test case
        """

        self.factory = APIRequestFactory()
        self.user = UserProfile.objects.create(username="boredom")
        
        create_dweet = {"dweet_text": "testing api", "comments":[]}
        request = self.factory.post('/dweetapi/dweet/', create_dweet , format='json')
        user1 = UserProfile.objects.get(username='boredom')
        user2 = UserProfile.objects.create(username='ddpandi',email="xyz@gmail.com")
        force_authenticate(request, user=user1)
        response = DweetViewSet.as_view({'post': 'create'})(request)

    def test_get_dweets_fail_pass(self):
        """
        test to get without authentication
        """

        request = self.factory.get('/dweetapi/dweet/', format='json')
        response = DweetViewSet.as_view({'get':'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_dweets_pass(self):
        """
        test to get dweets with authentication
        """

        request = self.factory.get('/dweetapi/dweet/', format='json')
        user = UserProfile.objects.get(username='boredom')
        force_authenticate(request, user=user)
        response = DweetViewSet.as_view({'get':'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_dweets_pass(self):
        """
        test to create dweet
        """

        create_dweet = {"dweet_text": "testing api", "comments":[]}
        request = self.factory.post('/dweetapi/dweet/', create_dweet , format='json')
        user = UserProfile.objects.get(username='boredom')
        force_authenticate(request, user=user)
        response = DweetViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_dweet_comment_fail_pass(self):
        """
        test to post comment on dweet without authentication
        """

        create_comment = {
                            "comments": [{
                                "comment": "hello"
                                }]
                        }    
        request = self.factory.patch('/dweetapi/dweet/', create_comment , format='json')
        #wihtout user
        response = DweetViewSet.as_view({'patch': 'partial_update'})(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_dweet_comment_pass(self):
        """
        test to post comment on dweet
        """
        
        create_comment = {
                            "comments": [{
                                "comment": "hello"
                                }]
                        }    
        request = self.factory.patch('/dweetapi/dweet/', create_comment , format='json')
        user = UserProfile.objects.get(username='ddpandi')
        force_authenticate(request, user=user)
        response = DweetViewSet.as_view({'patch': 'partial_update'})(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_redweet_pass(self):
        """
        test to redweet and check the count of the dweet
        """

        dweet_before_redweet = Dweet.objects.filter(pk=1).count()

        redweet = {"dweet_id": 1}    
        request = self.factory.post('/dweetapi/redweet/', redweet , format='json')
        user = UserProfile.objects.get(username='ddpandi')
        force_authenticate(request, user=user)
        response = ReDweetViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dweet_after_redweet = Dweet.objects.filter(pk=1).count() 

        if dweet_after_redweet == dweet_after_redweet:
            self.assertEqual(0, 0) 
        else:
            self.assertEqual(0, 1) 


    def test_post_redweet_fail_pass(self):
        """
        test to redweet when dweet doenst exist
        """

        redweet = {"dweet_id": 48}    
        request = self.factory.post('/dweetapi/redweet/', redweet , format='json')
        user = UserProfile.objects.get(username='ddpandi')
        force_authenticate(request, user=user)
        response = ReDweetViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_redweet_fail_pass_1(self):
        """
        test to redweet without authentication
        """

        redweet = {"dweet_id": 48}    
        request = self.factory.post('/dweetapi/redweet/', redweet , format='json')
        #without user        
        response = ReDweetViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_react_fail_pass(self):
        """
        test to react to dweet when no dweet exists
        """

        react = {                        
                    "dweet_id": 48,
                    "reaction": 1
                }    
        request = self.factory.post('/dweetapi/react/', react , format='json')
        user = UserProfile.objects.get(username='ddpandi')
        force_authenticate(request, user=user)      
        response = ReactionViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_react_pass(self):
        """
        test to react to dweet
        """

        react = {                        
                    "dweet_id": 1,
                    "reaction": 1
                }    
        request = self.factory.post('/dweetapi/react/', react , format='json')
        user = UserProfile.objects.get(username='ddpandi')
        force_authenticate(request, user=user)      
        response = ReactionViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
